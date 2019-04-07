import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlite3 import Connection as SQLite3Connection
from gradGyde import db
from .models import*

class DatabaseHelper():
    def MakeAoc(self, name, passed_type, year):
        try:
            new_aoc = Aocs(aoc_name = name, aoc_type=passed_type, aoc_year=year)
            db.session.add(new_aoc)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not create AOC! " + str(error))

    def MakeClass(self, name, semester, year, credit):
        try:
            new_class = Classes(class_name = name, class_semester=semester, class_year=year, credit_type=credit)
            db.session.add(new_class)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not create Class! " + str(error))

    def MakeUser(self, email, name, year, u_type):
        try:
            new_user = Users(user_email = email, user_name=name, year_started=year, user_type=u_type)
            db.session.add(new_user)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not create User! " + str(error))

    def MakeTag(self, name):
        try:
            new_tag = Tags(tag_name=name)
            db.session.add(new_tag)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not create Tag! " + str(error))

    def MakeRequirement(self, aoc, tag, required):
        try:
            new_req = Requirements(aoc_id = aoc, tag_id=tag, num_req=required)
            db.session.add(new_req)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not create Requirement! " + str(error))

    def AssignPrereqs(self, prereq, chosen):
        try:
            new_prereq = Prereqs(prereq_tag_id = prereq, chosen_tag_id=chosen)
            db.session.add(new_prereq)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not assign Prereq! " + str(error))

    def AssignTag(self, class_assigned, tag):
        try:
            new_type = ClassTags(class_id = class_assigned, tag_id=tag)
            db.session.add(new_type)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not assign Tag! " + str(error))

    def AssignAoc(self, aoc, user):
        try:
            new_major = PrefferedAocs(aoc_id = aoc, user_id=user)
            db.session.add(new_major)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not assign AOC! " + str(error))

    def TakeClass(self, class_taken, student):
        try:
            new_pass = ClassTaken(student_id = class_taken, class_id=student)
            db.session.add(new_pass)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not take Class! " + str(error))

    def CreateClass(self, name, semester, year, credit, tags):
        self.MakeClass(name,semester,year,credit)
        created_class = Classes.query.filter_by(class_name = name
            ).filter_by(class_semester=semester
            ).filter_by(class_year=year
            ).filter_by(credit_type=credit
            ).first()
        for tag in tags:
            self.AssignTag(created_class.class_id, self.GetTag(tag).tag_id)

    def CreateAoc(self, name, passed_type, year, tags, amounts):
        #Tags and Amounts are lists
        try:
            self.MakeAoc(name, passed_type, year)
            aoc = self.GetAoc(name, passed_type)
            for i in range(len(tags)):
                self.MakeTag(tags[i])
                temp_tag = self.GetTag(i)
                # self.MakeRequirement(aoc, temp_tag, amounts[i])
        except Exception as error:
            raise Exception("Could not create AOC! "+str(error))

    def GetUser(self, email):
        user_query = Users.query.filter_by(user_email=email).first()
        return user_query

    def GetAoc(self, name, type, year=datetime.date.today().year):
        aoc_query = Aocs.query.filter_by(aoc_name=name).filter_by(aoc_type=type).filter(year<=year).first()
        return aoc_query

    def GetAocById(self, id, type):
        aoc_query = Aocs.query.filter_by(aoc_id=id).filter_by(aoc_type=type).first()
        return aoc_query

    def GetAocs(self, name, type):
        aocs_query = Aocs.query.filter_by(aoc_name=name).filter_by(aoc_type=type).all()
        return aocs_query

    def GetAocsByType(self, type):
        aocs_query = Aocs.query.filter_by(aoc_type=type).all()
        return aocs_query

    def GetPrefferedAocs(self, user, type):
        pref_aocs_query = PrefferedAocs.query.filter_by(user_id=user.user_id).all()
        pref_aocs = []
        for item in pref_aocs_query:
            aoc = self.GetAocById(item.aoc_id, type)
            if aoc is not None:
                pref_aocs.append(aoc)
        return pref_aocs

    def GetClassById(self, id):
        class_query = Classes.query.filter_by(class_id=id).first()
        return class_query

    def GetClassesTaken(self, user):
        class_taken_query = ClassTaken.query.filter_by(student_id=user.user_id).all()
        classes_taken = []
        for class_taken in class_taken_query:
            da_class = self.GetClassById(class_taken.class_id)
            if da_class is not None:
                classes_taken.append(da_class)
        return classes_taken


    def GetTag(self, text):
        tag_query = Tags.query.filter_by(tag_name=text).first()
        return tag_query

    def GetTagById(self, id):
        tag_query = Tags.query.filter_by(tag_id=id).first()
        return tag_query


    def DBHelperTest(self):
        #MakeTag list
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
        #Create the AOC
        self.CreateAoc("Computer Science (Regular)", "Divisonal", 2018, tags, amounts)
        print(self.GetAoc("Computer Science (Regular)", "Divisonal"))
        print(self.GetAocsByType("Divisonal"))
        

