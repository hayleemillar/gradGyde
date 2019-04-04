# pylint: disable=too-few-public-methods
from flask_sqlalchemy import SQLAlchemy
from gradGyde import db
from .enums import SemesterTypeEnum, UserTypeEnum



class Aocs(db.Model):
    aoc_id = db.Column(db.Integer, primary_key=True)
    aoc_name = db.Column(db.String, nullable=False)
    aoc_type = db.Column(db.String, nullable=False)
    aoc_year = db.Column(db.Integer, nullable=False)
    requirements = db.relationship('Requirements',
                                   backref=db.backref('Aocs', uselist=False))

    def __repr__(self):
        return '<AOC: %r>' %self.aoc_name

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String, unique=True, nullable=False)
    user_name = db.Column(db.String, nullable=False)
    pref_aoc = db.Column(db.Integer, db.ForeignKey(Aocs.aoc_id),
                         nullable=False)
    pref_slash = db.Column(db.Integer, db.ForeignKey(Aocs.aoc_id),
                           nullable=True)
    pref_double = db.Column(db.Integer, db.ForeignKey(Aocs.aoc_id),
                            nullable=True)
    year_started = db.Column(db.Integer, nullable=False)
    user_type = db.Column(db.Enum(UserTypeEnum), nullable=False)
    aoc = db.relationship('Aocs', foreign_keys=[pref_aoc])
    slash = db.relationship('Aocs', foreign_keys=[pref_slash])
    double = db.relationship('Aocs', foreign_keys=[pref_double])
    classes_taken = db.relationship('Classes_taken',
                                    backref=db.backref('Users', uselist=False))

    def __repr__(self):
        return '<User: %r>' %self.user_name

class Classes(db.Model):
    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String, nullable=False)
    class_semester = db.Column(db.Enum(SemesterTypeEnum),
                               nullable=False)
    class_year = db.Column(db.Integer, nullable=False)
    credit_type = db.Column(db.Float, nullable=False)

    class_tags = db.relationship('Class_tags',
                                 backref=db.backref('Classes', uselist=False))
    classes_taken = db.relationship('Classes_taken',
                                    backref=db.backref('Classes', uselist=False))

    def __repr__(self):
        return '<Class %r>' %self.class_name

class Classes_taken(db.Model):
    class_taken_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(Users.user_id),
                           nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey(Classes.class_id),
                         nullable=False)


class Tags(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String, nullable=False)

    class_tags = db.relationship('Class_tags',
                                 backref=db.backref('Tags', uselist=False))
    requirements = db.relationship('Requirements',
                                   backref=db.backref('Tags', uselist=False))

    def __repr__(self):
        return '<Tag: %r>' %self.tag_name

class Class_tags(db.Model):
    class_tag_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey(Classes.class_id),
                         nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey(Tags.tag_id),
                       nullable=False)

class Prereqs(db.Model):
    prereq_id = db.Column(db.Integer, primary_key=True)
    prereq_tag_id = db.Column(db.Integer, db.ForeignKey(Tags.tag_id),
                              nullable=False)
    chosen_tag_id = db.Column(db.Integer, db.ForeignKey(Tags.tag_id),
                              nullable=False)
    prereq = db.relationship("Tags", foreign_keys=[prereq_tag_id])
    chosen = db.relationship("Tags", foreign_keys=[chosen_tag_id])



class Requirements(db.Model):
    req_id = db.Column(db.Integer, primary_key=True)
    aoc_id = db.Column(db.Integer, db.ForeignKey(Aocs.aoc_id),
                       nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey(Tags.tag_id),
                       nullable=False)
    num_req = db.Column(db.Integer, nullable=False)

def init_database():
    db.create_all()
