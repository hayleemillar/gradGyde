import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlite3 import Connection as SQLite3Connection
from gradGyde import db
from .models import*

class DatabaseHelper():
    def Make_aoc(self, name, passed_type, year):
        try:
            new_aoc =Aocs(aoc_name=name,
                         aoc_type=passed_type,
                         aoc_year=year)
            db.session.add(new_aoc)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not create AOC! " + str(error))

    def Make_class(self, name, semester, year, credit):
        try:
            new_class= Classes(class_name=name,
                              class_semester=semester,
                              class_year=year,
                              credit_type=credit)
            db.session.add(new_class)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not create Class! " + str(error))

    def Make_user(self, email, name, year, u_type):
        try:
            if self.Get_user(email) is None:
                new_user = Users(user_email=email,
                               user_name=name,
                               year_started=year,
                               user_type=u_type)
                db.session.add(new_user)
                db.session.commit()
        except Exception as error:
            raise Exception("Could not create User! " + str(error))

    def Make_tag(self, name):
        try:
            new_tag=Tags(tag_name=name)
            db.session.add(new_tag)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not create Tag! " + str(error))

    def Make_requirement(self, aoc, tag, required):
        try:
            new_req=Requirements(aoc_id=aoc.aoc_id,
                                 tag_id=tag.tag_id,
                                 num_req=required)
            db.session.add(new_req)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not create Requirement! " + str(error))

    def Assign_prereqs(self, prereq, chosen):
        try:
            new_prereq=Prereqs(prereq_tag_id=prereq.tag_id,
                               chosen_tag_id=chosen.tag_id)
            db.session.add(new_prereq)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not assign Prereq! " + str(error))

    def Assign_tags(self, class_assigned, tag):
        try:
            new_type=ClassTags(class_id=class_assigned.class_id,
                               tag_id=tag.tag_id)
            db.session.add(new_type)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not assign Tag! " + str(error))

    def Assign_aoc(self, aoc, user):
        try:
            new_major=PrefferedAocs(aoc_id=aoc.aoc_id,
                                    user_id=user.user_id)
            db.session.add(new_major)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not assign AOC! " + str(error))

    def Take_class(self, class_taken, student):
        try:
            new_pass=ClassTaken(student_id=student.user_id,
                                class_id=class_taken.class_id)
            db.session.add(new_pass)
            db.session.commit()
        except Exception as error:
            raise Exception("Could not take Class! " + str(error))

    def Create_class(self, name, semester, year, credit, tags):
        self.Make_class(name, semester, year, credit)
        created_class=Classes.query.filter_by(class_name=name
                                              ).filter_by(class_semester=semester
                                              ).filter_by(class_year=year
                                              ).filter_by(credit_type=credit
                                              ).first()
        for tag in tags:
            da_tag = self.Get_tag(tag)
            if da_tag is not None:
                self.Assign_tags(created_class, da_tag)

    def Create_aoc(self, name, passed_type, year, tags, amounts):
        #Tags and Amounts are lists
        try:
            self.Make_aoc(name, passed_type, year)
            aoc=self.Get_aoc(name, passed_type)
            for i in range(len(tags)):
                self.Make_tag(tags[i])
                temp_tag = self.Get_tag(tags[i])
                self.Make_requirement(aoc, temp_tag, amounts[i])

        except Exception as error:
            raise Exception("Could not create AOC! "+str(error))

    def Get_user(self, email):
        user_query=Users.query.filter_by(user_email=email
            ).first()
        return user_query

    def Get_aoc(self, name, passed_type, year=datetime.date.today().year):
        aoc_query=Aocs.query.filter_by(aoc_name=name
                                         ).filter_by(aoc_type=passed_type
                                         ).filter(Aocs.aoc_year<=year
                                         ).first()
        return aoc_query

    def Get_aoc_by_id(self, id):
        aoc_query=Aocs.query.filter_by(aoc_id=id
                                         ).first()
        return aoc_query

    def Get_aocs_by_type(self, type):
        aocs_query=Aocs.query.filter_by(aoc_type=type).all()
        return aocs_query

    def Get_preffered_aocs(self, user, type):
        pref_aocs_query=PrefferedAocs.query.filter_by(user_id=user.user_id).all()
        pref_aocs=[]
        #add check for size and pass general studies if there are no prefered aocs
        for item in pref_aocs_query:
            aoc=self.Get_aoc_by_id(item.aoc_id)
            if aoc is not None:
                pref_aocs.append(aoc)
        return pref_aocs

    def Get_class(self, c_name):
        class_query=Classes.query.filter_by(class_name=c_name
                                            ).first()
        return class_query

    def Get_class_by_id(self, c_id):
        class_query=Classes.query.filter_by(class_id=c_id
                                            ).first()
        return class_query

    def Get_classes_taken(self, user):
        class_taken_query=ClassTaken.query.filter_by(student_id=user.user_id
                                                     ).all()
        classes_taken =[]
        for class_taken in class_taken_query:
            da_class=self.Get_class_by_id(class_taken.class_id)
            if da_class is not None:
                classes_taken.append(da_class)
        return classes_taken


    def Get_tag(self, text):
        tag_query=Tags.query.filter_by(tag_name=text
                                       ).first()
        return tag_query

    def Get_tag_by_id(self, t_id):
        tag_query=Tags.query.filter_by(tag_id=t_id
                                       ).first()
        return tag_query


    def Db_helper_test(self):
        #Make_tag list
        tags=[]
        amounts=[]
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
        self.Create_aoc("Computer Science (Regular)", "Divisonal", 2018, tags, amounts)
        comp_sci=self.Get_aoc("Computer Science (Regular)", "Divisonal")
        print(comp_sci)
        print(self.Get_aocs_by_type("Divisonal"))
        for tag in tags:
            print(self.Get_tag(tag))
        #Test class
        self.Create_class("Introduction to Programming With Python",
                         SemesterType.FALL, 2018, 1, [tags[0]])
        da_class=self.Get_class("Introduction to Programming With Python")
        print(da_class)
        #Test user
        self.Make_user("harry.potter97@ncf.edu", "Harry", 1997, UserType.STUDENT)
        student = self.Get_user("harry.potter97@ncf.edu")
        print(student)
        #set preferred AOCS
        self.Assign_aoc(comp_sci.aoc_id, student.user_id)
        print(self.Get_preffered_aocs(student, "Divisonal"))
        #set taken class
        self.Take_class(da_class, student)
        print(self.Get_classes_taken(student))
