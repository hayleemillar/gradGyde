import datetime, os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import (SemesterType,
                     UserType,
                     Aocs,
                     Users,
                     PrefferedAocs,
                     Classes,
                     ClassTaken,
                     Tags,
                     ClassTags,
                     Prereqs,
                     Requirements)


ENGINE = create_engine('sqlite:///gradGyde\\gradGyde.db')
SESSION_MAKER = sessionmaker(bind=ENGINE)
SESSION = SESSION_MAKER()

class DatabaseHelper():
    @classmethod
    def __make_aoc(cls, name, passed_type, year):
        try:
            new_aoc = Aocs(aoc_name=name,
                           aoc_type=passed_type,
                           aoc_year=year)
            SESSION.add(new_aoc)
            SESSION.commit()
        except Exception as error:
            raise Exception("Could not create AOC! " + str(error))

    @classmethod
    def __make_class(cls, name, semester, year, credit):
        try:
            new_class = Classes(class_name=name,
                                class_semester=semester,
                                class_year=year,
                                credit_type=credit)
            SESSION.add(new_class)
            SESSION.commit()
        except Exception as error:
            raise Exception("Could not create Class! " + str(error))

    @classmethod
    def make_user(cls, email, name, year, u_type):
        try:
            if cls.get_user(email) is None:
                new_user = Users(user_email=email,
                                 user_name=name,
                                 year_started=year,
                                 user_type=u_type)
                SESSION.add(new_user)
                SESSION.commit()
        except Exception as error:
            raise Exception("Could not create User! " + str(error))

    @classmethod
    def __make_tag(cls, name):
        try:
            new_tag = Tags(tag_name=name)
            SESSION.add(new_tag)
            SESSION.commit()
        except Exception as error:
            raise Exception("Could not create Tag! " + str(error))

    @classmethod
    def __make_requirement(cls, aoc, tag, required):
        try:
            new_req = Requirements(aoc_id=aoc.aoc_id,
                                   tag_id=tag.tag_id,
                                   num_req=required)
            SESSION.add(new_req)
            SESSION.commit()
        except Exception as error:
            raise Exception("Could not create Requirement! " + str(error))

    @classmethod
    def __assign_prereqs(cls, prereq, chosen):
        try:
            new_prereq = Prereqs(prereq_tag_id=prereq.tag_id,
                                 chosen_tag_id=chosen.tag_id)
            SESSION.add(new_prereq)
            SESSION.commit()
        except Exception as error:
            raise Exception("Could not assign Prereq! " + str(error))

    @classmethod
    def __assign_tags(cls, class_assigned, tag):
        try:
            new_type = ClassTags(class_id=class_assigned.class_id,
                                 tag_id=tag.tag_id)
            SESSION.add(new_type)
            SESSION.commit()
        except Exception as error:
            raise Exception("Could not assign Tag! " + str(error))

    @classmethod
    def assign_aoc(cls, aoc, user):
        try:
            new_major = PrefferedAocs(aoc_id=aoc.aoc_id,
                                      user_id=user.user_id)
            SESSION.add(new_major)
            SESSION.commit()
        except Exception as error:
            raise Exception("Could not assign AOC! " + str(error))

    @classmethod
    def take_class(cls, class_taken, student):
        try:
            new_pass = ClassTaken(student_id=student.user_id,
                                  class_id=class_taken.class_id)
            SESSION.add(new_pass)
            SESSION.commit()
        except Exception as error:
            raise Exception("Could not take Class! " + str(error))

    @classmethod
    def create_class(cls, class_info, tags):
        cls.__make_class(class_info[0], class_info[1], class_info[2], class_info[3])
        new_class = Classes.query.filter_by(class_name=class_info[0]
                                            ).filter_by(class_semester=class_info[1]
                                                        ).filter_by(class_year=class_info[2]
                                                                    ).first()
        for tag in tags:
            da_tag = cls.get_tag(tag)
            if da_tag is not None:
                cls.__assign_tags(new_class, da_tag)

    @classmethod
    def create_aoc(cls, aoc_info, tags, amounts):
        #Tags and Amounts are lists
        try:
            cls.__make_aoc(aoc_info[0], aoc_info[1], aoc_info[2])
            aoc = cls.get_aoc(aoc_info[0], aoc_info[1])
            for tag in tags:
                cls.__make_tag(tag)
                da_tag = cls.get_tag(tag)
                cls.__make_requirement(aoc, da_tag, amounts[tags.index(tag)])

        except Exception as error:
            raise Exception("Could not create AOC! "+str(error))

    @classmethod
    def get_user(cls, email):
        user_query = Users.query.filter_by(user_email=email).first()
        return user_query

    @classmethod
    def get_aoc(cls, name, passed_type, year=datetime.date.today().year):
        aoc_query = Aocs.query.filter_by(aoc_name=name
                                        ).filter_by(aoc_type=passed_type
                                                    ).filter(Aocs.aoc_year <= year
                                                            ).first()
        return aoc_query

    @classmethod
    def __get_aoc_by_id(cls, a_id):
        aoc_query = Aocs.query.filter_by(aoc_id=a_id).first()
        return aoc_query

    @classmethod
    def get_aocs_by_type(cls, pref_type):
        aocs_query = Aocs.query.filter_by(aoc_type=pref_type).all()
        return aocs_query

    @classmethod
    def get_preffered_aocs(cls, user, pref_type):
        pref_aocs_query = PrefferedAocs.query.filter_by(user_id=user.user_id).all()
        pref_aocs = []
        #add check for size and pass general studies if there are no prefered aocs
        for item in pref_aocs_query:
            aoc = cls.__get_aoc_by_id(item.aoc_id)
            if aoc is not None and aoc.aoc_type == pref_type:
                pref_aocs.append(aoc)
        return pref_aocs

    @classmethod
    def get_class(cls, c_name):
        class_query = Classes.query.filter_by(class_name=c_name).first()
        return class_query

    @classmethod
    def __get_class_by_id(cls, c_id):
        class_query = Classes.query.filter_by(class_id=c_id).first()
        return class_query

    @classmethod
    def get_classes_taken(cls, user):
        class_taken_query = ClassTaken.query.filter_by(student_id=user.user_id).all()
        classes_taken = []
        for class_taken in class_taken_query:
            da_class = cls.__get_class_by_id(class_taken.class_id)
            if da_class is not None:
                classes_taken.append(da_class)
        return classes_taken

    @classmethod
    def get_tag(cls, text):
        tag_query = Tags.query.filter_by(tag_name=text).first()
        return tag_query

    @classmethod
    def __get_tag_by_id(cls, t_id):
        tag_query = Tags.query.filter_by(tag_id=t_id).first()
        return tag_query


    def db_helper_test(self):
        #make_tag list
        tags = []
        amounts = []
        tags.append("CS Introductory Course")
        amounts.append(1)
        tags.append("Object Oriented Programming With Java")
        amounts.append(1)
        tags.append("Object Oriented Design In Java")
        amounts.append(1)
        tags.append("Software Engineering")
        amounts.append(1)
        tags.append("Discrete Mathematics")
        amounts.append(1)
        tags.append("Data Structures in Java")
        amounts.append(1)
        tags.append("Algorithms")
        amounts.append(1)
        tags.append("Programming Languages")
        amounts.append(1)
        tags.append("Systems")
        amounts.append(2)
        tags.append("Theory")
        amounts.append(1)
        tags.append("AI")
        amounts.append(1)
        tags.append("Applications")
        amounts.append(2)
        tags.append("Math")
        amounts.append(2)
        print(tags)
        print(amounts)
        #create the AOC
        aoc_info = ["Computer Science (Regular)", "Divisonal", 2018]
        self.create_aoc(aoc_info, tags, amounts)
        comp_sci = self.get_aoc("Computer Science (Regular)", "Divisonal")
        print(comp_sci)
        print(self.get_aocs_by_type("Divisonal"))
        for tag in tags:
            print(self.get_tag(tag))
        #Test class
        class_info = ["Introduction to Programming With Python", SemesterType.FALL, 2018, 1]
        self.create_class(class_info, [tags[0]])
        da_class = self.get_class("Introduction to Programming With Python")
        print(da_class)
        #Test user
        self.make_user("harry.potter97@ncf.edu", "Harry", 1997, UserType.STUDENT)
        student = self.get_user("harry.potter97@ncf.edu")
        print(student)
        #set preferred AOCS
        self.assign_aoc(comp_sci, student)
        print(self.get_preffered_aocs(student, "Divisonal"))
        #set taken class
        self.take_class(da_class, student)
        print(self.get_classes_taken(student))

# DBHELPER = DatabaseHelper()
# DBHELPER.db_helper_test()
