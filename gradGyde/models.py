# pylint: disable=too-few-public-methods
import enum
from gradGyde import db

class SemesterType(enum.Enum):
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    ISP = "isp"

class UserType(enum.Enum):
    STUDENT = "student"
    PROFESSOR = "professor"
    ADMIN = "administrator"

class Aocs(db.Model):
    aoc_id = db.Column(db.Integer, primary_key=True)
    aoc_name = db.Column(db.String, nullable=False)
    aoc_type = db.Column(db.String, nullable=False)
    aoc_year = db.Column(db.Integer, nullable=False)
    pref_aoc = db.relationship('PrefferedAocs',
                               backref=db.backref('Aocs'), uselist=False)
    requirements = db.relationship('Requirements',
                                   backref=db.backref('Aocs', uselist=False))

    def __repr__(self):
        return '<AOC: %r>' %self.aoc_name

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String, unique=True, nullable=False)
    user_name = db.Column(db.String, nullable=False)
    year_started = db.Column(db.Integer, nullable=False)
    user_type = db.Column(db.Enum(UserType), nullable=False)
    class_taken = db.relationship('ClassTaken',
                                  backref=db.backref('Users', uselist=False))
    pref_aoc = db.relationship('PrefferedAocs',
                               backref=db.backref('Users'), uselist=False)

    def __repr__(self):
        return '<User: %r>' %self.user_name

class PrefferedAocs(db.Model):
    pref_aoc_id = db.Column(db.Integer, primary_key=True)
    aoc_id = db.Column(db.Integer, db.ForeignKey(Aocs.aoc_id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.user_id), nullable=False)

class Classes(db.Model):
    class_id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String, nullable=False)
    class_semester = db.Column(db.Enum(SemesterType),
                               nullable=False)
    class_year = db.Column(db.Integer, nullable=False)
    credit_type = db.Column(db.Float, nullable=False)

    class_tags = db.relationship('ClassTags',
                                 backref=db.backref('Classes', uselist=False))
    class_taken = db.relationship('ClassTaken',
                                  backref=db.backref('Classes', uselist=False))

    def __repr__(self):
        return '<Class %r>' %self.class_name

class ClassTaken(db.Model):
    class_taken_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(Users.user_id),
                           nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey(Classes.class_id),
                         nullable=False)

class Tags(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String, nullable=False)

    class_tags = db.relationship('ClassTags',
                                 backref=db.backref('Tags', uselist=False))
    requirements = db.relationship('Requirements',
                                   backref=db.backref('Tags', uselist=False))

    def __repr__(self):
        return '<Tag: %r>' %self.tag_name

class ClassTags(db.Model):
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
