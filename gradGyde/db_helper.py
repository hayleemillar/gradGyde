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
            if self.GetUser(email) is None:
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
            new_req = Requirements(aoc_id = aoc.aoc_id, tag_id=tag.tag_id, num_req=required)
            db.session.add(new_req)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not create Requirement! " + str(error))

    def AssignPrereqs(self, prereq, chosen):
        try:
            new_prereq = Prereqs(prereq_tag_id = prereq.tag_id, chosen_tag_id=chosen.tag_id)
            db.session.add(new_prereq)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not assign Prereq! " + str(error))

    def AssignTag(self, class_assigned, tag):
        try:
            new_type = ClassTags(class_id = class_assigned.class_id, tag_id=tag.tag_id)
            db.session.add(new_type)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not assign Tag! " + str(error))

    def AssignAoc(self, aoc, user):
        try:
            new_major = PrefferedAocs(aoc_id = aoc.aoc_id, user_id=user.user_id)
            db.session.add(new_major)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not assign AOC! " + str(error))

    def TakeClass(self, class_taken, student):
        try:
            new_pass = ClassTaken(student_id = student.user_id, class_id=class_taken.class_id)
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
            da_tag = self.GetTag(tag)
            if da_tag is not None:
                self.AssignTag(created_class, da_tag)

    def CreateAoc(self, name, passed_type, year, tags, amounts):
        #Tags and Amounts are lists
        try:
            self.MakeAoc(name, passed_type, year)
            aoc = self.GetAoc(name, passed_type)
            for i in range(len(tags)):
                self.MakeTag(tags[i])
                temp_tag = self.GetTag(tags[i])
                self.MakeRequirement(aoc, temp_tag, amounts[i])

        except Exception as error:
            raise Exception("Could not create AOC! "+str(error))

    def GetUser(self, email):
        user_query = Users.query.filter_by(user_email=email
            ).first()
        return user_query

    def GetAoc(self, name, passed_type, year=datetime.date.today().year):
        aoc_query = Aocs.query.filter_by(aoc_name=name).filter_by(aoc_type=passed_type).filter(Aocs.aoc_year<=year
            ).first()
        return aoc_query

    def GetAocById(self, id):
        aoc_query = Aocs.query.filter_by(aoc_id=id
            ).first()
        return aoc_query

    def GetAocsByType(self, type):
        aocs_query = Aocs.query.filter_by(aoc_type=type).all()
        return aocs_query

    def GetPrefferedAocs(self, user, type):
        pref_aocs_query = PrefferedAocs.query.filter_by(user_id=user.user_id).all()
        pref_aocs = []
        #add check for size and pass general studies if there are no prefered aocs
        for item in pref_aocs_query:
            aoc = self.GetAocById(item.aoc_id)
            if aoc is not None:
                pref_aocs.append(aoc)
        return pref_aocs

    def GetClass(self, c_name):
        class_query = Classes.query.filter_by(class_name=c_name
            ).first()
        return class_query

    def GetClassById(self, c_id):
        class_query = Classes.query.filter_by(class_id=c_id
            ).first()
        return class_query

    def GetClassesTaken(self, user):
        class_taken_query = ClassTaken.query.filter_by(student_id=user.user_id
            ).all()
        classes_taken = []
        for class_taken in class_taken_query:
            da_class = self.GetClassById(class_taken.class_id)
            if da_class is not None:
                classes_taken.append(da_class)
        return classes_taken


    def GetTag(self, text):
        tag_query = Tags.query.filter_by(tag_name=text
            ).first()
        return tag_query

    def GetTagById(self, t_id):
        tag_query = Tags.query.filter_by(tag_id=t_id
            ).first()
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
        comp_sci = self.GetAoc("Computer Science (Regular)", "Divisonal")
        print(comp_sci)
        print(self.GetAocsByType("Divisonal"))
        for tag in tags:
            print(self.GetTag(tag))
        #Test class
        self.CreateClass("Introduction to Programming With Python", SemesterType.FALL, 2018, 1, [tags[0]])
        da_class = self.GetClass("Introduction to Programming With Python")
        print(da_class)
        #Test user
        self.MakeUser("harry.potter97@ncf.edu", "Harry", 1997, UserType.STUDENT)
        student = self.GetUser("harry.potter97@ncf.edu")
        print(student)
        #set preferred AOCS
        self.AssignAoc(comp_sci.aoc_id, student.user_id)
        print(self.GetPrefferedAocs(student, "Divisonal"))
        #set taken class
        self.TakeClass(da_class, student)
        print(self.GetClassesTaken(student))



        

