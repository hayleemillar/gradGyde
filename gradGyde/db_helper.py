import datetime
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import (Aocs,
                     Users,
                     PrefferedAocs,
                     Classes,
                     ClassTaken,
                     Tags,
                     ClassTags,
                     Prereqs,
                     Requirements)


DIRPATH = os.path.abspath(__file__)
ENGINEPATH = 'sqlite:///'+DIRPATH[:len(DIRPATH)-12]+'gradGyde.db'
ENGINE = create_engine(ENGINEPATH)
SESSION_MAKER = sessionmaker(bind=ENGINE)
SESSION = SESSION_MAKER()


def make_aoc(name, passed_type, year):
    new_aoc = Aocs(aoc_name=name,
                   aoc_type=passed_type,
                   aoc_year=year)
    SESSION.add(new_aoc)
    SESSION.commit()


def make_class(name, semester, year, credit):
    new_class = Classes(class_name=name,
                        class_semester=semester,
                        class_year=year,
                        credit_type=credit)
    SESSION.add(new_class)
    SESSION.commit()


def make_user(email, name, year, u_type):
    if get_user(email) is None:
        new_user = Users(user_email=email,
                         user_name=name,
                         year_started=year,
                         user_type=u_type)
        SESSION.add(new_user)
        SESSION.commit()


def make_tag(name):
    new_tag = Tags(tag_name=name)
    SESSION.add(new_tag)
    SESSION.commit()


def make_requirement(aoc, tag, required):
    new_req = Requirements(aoc_id=aoc.aoc_id,
                           tag_id=tag.tag_id,
                           num_req=required)
    SESSION.add(new_req)
    SESSION.commit()


def assign_prereqs(prereq, chosen):
    new_prereq = Prereqs(prereq_tag_id=prereq.tag_id,
                         chosen_tag_id=chosen.tag_id)
    SESSION.add(new_prereq)
    SESSION.commit()


def assign_tags(class_assigned, tag):
    new_type = ClassTags(class_id=class_assigned.class_id,
                         tag_id=tag.tag_id)
    SESSION.add(new_type)
    SESSION.commit()


def assign_aoc(aoc, user):
    new_major = PrefferedAocs(aoc_id=aoc.aoc_id,
                              user_id=user.user_id)
    SESSION.add(new_major)
    SESSION.commit()


def take_class(class_taken, student):
    new_pass = ClassTaken(student_id=student.user_id,
                          class_id=class_taken.class_id)
    SESSION.add(new_pass)
    SESSION.commit()


def create_class(class_info, tags):
    make_class(class_info[0], class_info[1], class_info[2], class_info[3])
    new_class = Classes.query.filter_by(class_name=class_info[0]).filter_by(
        class_semester=class_info[1]).filter_by(class_year=class_info[2]).first()
    for tag in tags:
        da_tag = get_tag(tag)
        if da_tag is not None:
            assign_tags(new_class, da_tag)


def create_aoc(aoc_info, tags, amounts):
    # Tags and Amounts are lists
    make_aoc(aoc_info[0], aoc_info[1], aoc_info[2])
    aoc = get_aoc(aoc_info[0], aoc_info[1])
    for tag in tags:
        make_tag(tag)
        da_tag = get_tag(tag)
        make_requirement(aoc, da_tag, amounts[tags.index(tag)])


def get_user(email):
    user_query = Users.query.filter_by(user_email=email).first()
    return user_query


def get_aoc(name, passed_type, year=datetime.date.today().year):
    aoc_query = Aocs.query.filter_by(aoc_name=name).filter_by(
        aoc_type=passed_type).filter(Aocs.aoc_year <= year).first()
    return aoc_query


def get_aoc_by_id(a_id):
    aoc_query = Aocs.query.filter_by(aoc_id=a_id).first()
    return aoc_query


def get_aocs_by_type(pref_type):
    aocs_query = Aocs.query.filter_by(aoc_type=pref_type).all()
    return aocs_query


def get_preffered_aocs(user, pref_type):
    pref_aocs_query = PrefferedAocs.query.filter_by(user_id=user.user_id).all()
    pref_aocs = []
    # add check for size and pass general studies if there are no prefered aocs
    for item in pref_aocs_query:
        aoc = get_aoc_by_id(item.aoc_id)
        if aoc is not None and aoc.aoc_type == pref_type:
            pref_aocs.append(aoc)
    return pref_aocs


def get_class(c_name):
    class_query = Classes.query.filter_by(class_name=c_name).first()
    return class_query


def get_class_by_id(c_id):
    class_query = Classes.query.filter_by(class_id=c_id).first()
    return class_query

def get_tag(text):
    tag_query = Tags.query.filter_by(tag_name=text).first()
    return tag_query


def get_tag_by_id(t_id):
    tag_query = Tags.query.filter_by(tag_id=t_id).first()
    return tag_query

#1.0 Tasks:

#1: Get a list of courses taken by a student that is filterable
#By semester, year, tag, and name
def get_classes_taken(user, semester=None, da_year=None, da_tag_id=None, da_name=None):
    #Old version of query:
    #class_taken_query = ClassTaken.query.filter_by(
    #student_id=user.user_id).all()
    filters = []
    #filters is the list of all filters we want to have
    if semester is not None:
        filters.append(Classes.class_semester == semester)
    if da_year is not None:
        filters.append(Classes.class_year >= da_year)
    if da_name is not None:
        filters.append(Classes.class_name == da_name)
    if da_tag_id is not None:
        class_taken_query = SESSION.query(ClassTaken, Classes, ClassTags
                                          ).filter_by(student_id=user.user_id
                                          ).join(Classes
                                          ).filter(*filters
                                          ).join(ClassTags
                                          ).filter(ClassTags.tag_id == da_tag_id
                                          ).all()
    else:
        class_taken_query = SESSION.query(ClassTaken, Classes,
                                          ).filter_by(student_id=user.user_id
                                          ).join(Classes
                                          ).filter(*filters
                                          ).all()
    classes_taken = []
    for class_taken in class_taken_query:
        da_class = get_class_by_id(class_taken.Classes.class_id)
        if da_class is not None:
            classes_taken.append(da_class)
    return classes_taken

#2: Get a list of potential courses a student could take, based on
#Associated tag and year. Year >= Student's start year

#3: Get a list of all tags associated with a course
def get_class_tags(da_class_id):
    #This function takes a class_id from the database as input
    #And outputs a list of course tag names
    #Get a Query object with class_tags joined on tags where class_id=da_class_id
    class_tags = SESSION.query(ClassTags, Tags
                                  ).filter_by(class_id=da_class_id
                                  ).join(Tags).all()
    class_tag_list = []
    for class_tag in class_tags:
        class_tag_list.append(class_tag.Tags.tag_name)
    return class_tag_list

#4: Given a prereq and year, get all the classes that fulfill the prereq 

#5: Get the requirments for an AOC

#6: Get the potential courses a student could take that fulfill those reqs

#7: Of the potential courses above, get the ones a student has taken

#8: Stuff all this into a json

#9: Get all this for a student's preffered AOC of all 3 types

#10: Get a list of all courses or course names for Haylee to display.
#Should this be limited to ones the student could have taken?