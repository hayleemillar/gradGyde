# pylint: disable=E1101
import datetime
import json
from . import SESSION
from .models import (Aocs,
                     Users,
                     PrefferedAocs,
                     Classes,
                     ClassTaken,
                     Tags,
                     ClassTags,
                     Prereqs,
                     Requirements)

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

def make_user(email, name, da_year, u_type):
    if get_user(email) is None:
        newuser = Users(user_email=email,
                        user_name=name,
                        year_started=da_year,
                        user_type=u_type)
        SESSION.add(newuser)
        SESSION.commit()

def update_user(email, name, da_year):
    user = get_user(email)
    if get_user(email) is not None:
        user.user_name = name
        user.year_started = da_year
        SESSION.commit()


def make_tag(name):
    new_tag = Tags(tag_name=name)
    SESSION.add(new_tag)
    SESSION.commit()


def make_requirement(da_aoc_id, da_tag_id, required):
    new_req = Requirements(aoc_id=da_aoc_id,
                           tag_id=da_tag_id,
                           num_req=required)
    SESSION.add(new_req)
    SESSION.commit()


def assign_prereqs(prereq, chosen):
    #Chosen is the tag with a prereq
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
        if not tag_exists(tag):
            make_tag(tag)
        da_tag = get_tag(tag)
        make_requirement(aoc.aoc_id, da_tag.tag_id, amounts[tags.index(tag)])


def get_user(email):
    user_query = Users.query.filter_by(user_email=email).first()
    return user_query


def get_aoc(name, passed_type, year=datetime.date.today().year):
    aoc_query = Aocs.query.filter_by(aoc_name=name).filter_by(
        aoc_type=passed_type).filter(Aocs.aoc_year <= year).order_by(
            Aocs.aoc_id.desc()).first()
    return aoc_query


def get_aoc_by_id(a_id):
    aoc_query = Aocs.query.filter_by(aoc_id=a_id).first()
    return aoc_query


def get_aocs_by_type(pref_type):
    aocs_query = Aocs.query.filter_by(aoc_type=pref_type).all()
    return aocs_query

def get_aocs(pref_type, name, da_year):
    filters = []
    if da_year is not None:
        filters.append(Aocs.aoc_year >= da_year)
    if name is not None:
        filters.append(Aocs.aoc_name == name)
    filters.append(Aocs.aoc_type == pref_type)
    print(filters)
    return SESSION.query(Aocs).filter(*filters).all()

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

def tag_exists(text):
    tag_query = Tags.query.filter_by(tag_name=text).first()
    if tag_query is None:
        return False
    return True

def get_classes(name, da_year, semester):
    filters = []
    if semester is not None:
        filters.append(Classes.class_semester == semester)
    if da_year is not None:
        filters.append(Classes.class_year == da_year)
    if name is not None:
        filters.append(Classes.class_name == name)
    class_query = SESSION.query(Classes).filter(*filters).all()
    return class_query



def get_classes_taken(user, semester=None, da_year=None, da_tag_id=None, da_name=None):
    filters = []
    #filters is the list of all filters we want to have
    if semester is not None:
        filters.append(Classes.class_semester == semester)
    if da_year is not None:
        filters.append(Classes.class_year >= da_year)
    if da_name is not None:
        filters.append(Classes.class_name == da_name)
    if da_tag_id is not None:
        class_taken_query = SESSION.query(ClassTaken, Classes, ClassTags).filter_by(
            student_id=user.user_id).join(
                Classes).filter(
                    *filters).join(
                        ClassTags).filter(
                            ClassTags.tag_id == da_tag_id).all()
    else:
        class_taken_query = SESSION.query(ClassTaken, Classes,).filter_by(
            student_id=user.user_id).join(
                Classes).filter(*filters).all()
    classes_taken = []
    for class_taken in class_taken_query:
        da_class = get_class_by_id(class_taken.Classes.class_id)
        if da_class is not None:
            classes_taken.append(da_class)
    return classes_taken

def get_potential_classes(da_tag_id, da_year):
    #Takes in a tag_id and a year as input
    #Outputs a list of class objects that fit the req.
    class_query = SESSION.query(ClassTags, Classes).filter(
        ClassTags.tag_id == da_tag_id).join(
            Classes).filter(Classes.class_year >= da_year).all()
    potential_courses = []
    for course in class_query:
        potential_courses.append(course.Classes)
    return potential_courses

def get_class_tags(da_class_id):
    #This function takes a class_id from the database as input
    #And outputs a list of class tags
    #Get a Query object with class_tags joined on tags where class_id=da_class_id
    class_tags = SESSION.query(ClassTags, Tags).filter_by(
        class_id=da_class_id).join(Tags).all()
    class_tag_list = []
    for class_tag in class_tags:
        class_tag_list.append(class_tag.Tags)
    return class_tag_list

def get_prereqs(chosen_id):
    #Takes the chosen tag's id as an input
    #and outputs a list of associated prereq objects
    return Prereqs.query.filter_by(chosen_tag_id=chosen_id).all()

def get_requirements(da_aoc_id):
    #Takes an aoc id as input, outputs a list of requirement objects that match it
    req_query = Requirements.query.filter_by(aoc_id=da_aoc_id).all()
    return req_query

def get_requirements_with_tag(da_aoc_id):
    #Same as above, but returns a list of result objects with requirements joined to their tag
    req_query = SESSION.query(Requirements, Tags).filter_by(aoc_id=da_aoc_id).join(Tags).all()
    return req_query

def check_classes_taken(user_id, class_list):
    #Takes a list of classes as inputs
    #outputs a list of classes a student has taken
    class_id_list = []
    for each_class in class_list:
        class_id_list.append(each_class.class_id)
    class_taken_query = SESSION.query(ClassTaken, Classes,).filter_by(
        student_id=user_id).filter(
            ClassTaken.class_id.in_(class_id_list)).join(Classes).all()
    classes_taken = []
    for class_taken in class_taken_query:
        da_class = get_class_by_id(class_taken.Classes.class_id)
        if da_class is not None:
            classes_taken.append(da_class)
    return classes_taken

def check_class_taken(user_id, da_class_id):
    query = ClassTaken.query.filter_by(student_id=user_id).filter_by(class_id=da_class_id).all()
    if query:
        return True
    return False

def check_aoc_pref(user_id, aoc_id):
    query = PrefferedAocs.query.filter_by(aoc_id=aoc_id).filter_by(user_id=user_id).first()
    if query:
        return True
    return False

def get_classes_taken_json(classes_taken):
    if classes_taken is not None:
        classes = {}
        class_index = 0
        print(classes_taken)
        for course in classes_taken:
            class_key = 'class'+str(class_index)
            class_info = {'name' : course.class_name,
                          'semester' : course.class_semester.value,
                          'year' : course.class_year,
                          'id' : course.class_id}
            class_index = class_index+1
            classes[class_key] = class_info
        return json.dumps(classes)
    return None

def search_classes_json(user, classes_taken):
    if classes_taken is not None:
        classes = {}
        class_index = 0
        print(classes_taken)
        for course in classes_taken:
            class_key = 'class'+str(class_index)
            class_info = {'name' : course.class_name,
                          'semester' : course.class_semester.value,
                          'year' : course.class_year,
                          'id' : course.class_id}
            taken = check_class_taken(user.user_id, course.class_id)
            class_info['taken'] = taken
            class_index = class_index+1
            classes[class_key] = class_info
        return json.dumps(classes)
    return None


def get_classes_json(classes_fulfilling, user):
    classes = {}
    class_index = 0
    for course in classes_fulfilling:
        class_key = 'class'+str(class_index)
        class_info = {'id' : course.class_id,
                      'name' : course.class_name}
        taken = check_class_taken(user.user_id, course.class_id)
        class_info['taken'] = taken
        class_index = class_index+1
        classes[class_key] = class_info
    return classes

def get_requirements_json(requirements, user, da_year=None):
    req_index = 0
    reqs = {}
    for req in requirements:
        json_req_key = "req"+str(req_index)
        req_info = {'id' : req.Requirements.req_id,
                    'name' : req.Tags.tag_name,
                    'amount' : req.Requirements.num_req}
        if da_year is not None:
            classes_fulfilling = get_potential_classes(req.Tags.tag_id, da_year)
        else:
            classes_fulfilling = get_potential_classes(req.Tags.tag_id, user.year_started)
        classes_taken = check_classes_taken(user.user_id, classes_fulfilling)
        fulfilled = False
        if len(classes_taken) >= req.Requirements.num_req:
            fulfilled = True
        req_info['fulfilled'] = fulfilled
        #Now, for classes
        classes = get_classes_json(classes_fulfilling, user)
        req_index = req_index+1
        req_info['classes'] = classes
        reqs[json_req_key] = req_info
    return reqs

def get_aoc_json(user, aoc_type):
    #First, get the list of aocs
    json_base = {}
    aoc_list = get_preffered_aocs(user, aoc_type)
    aoc_index = 0
    for aoc in aoc_list:
        json_aoc_key = "aoc"+str(aoc_index)
        aoc_info = {'id' : aoc.aoc_id,
                    'name' : aoc.aoc_name,
                    'year' : aoc.aoc_year,
                    'type' : aoc.aoc_type}
        requirements = get_requirements_with_tag(aoc.aoc_id)
        reqs = get_requirements_json(requirements, user)
        aoc_index = aoc_index+1
        aoc_info['requirements'] = reqs
        json_base[json_aoc_key] = aoc_info
    return json.dumps(json_base)

def search_aoc_json(user, aoc_type, da_name, da_year):
    #First, get the list of aocs
    json_base = {}
    aoc_list = get_aocs(aoc_type, da_name, da_year)
    aoc_index = 0
    for aoc in aoc_list:
        json_aoc_key = "aoc"+str(aoc_index)
        aoc_info = {'id' : aoc.aoc_id,
                    'name' : aoc.aoc_name,
                    'year' : aoc.aoc_year,
                    'type' : aoc.aoc_type}
        taken = check_aoc_pref(user.user_id, aoc.aoc_id)
        aoc_info['assigned'] = taken
        requirements = get_requirements_with_tag(aoc.aoc_id)
        reqs = get_requirements_json(requirements, user, da_year=da_year)
        aoc_index = aoc_index+1
        aoc_info['requirements'] = reqs
        json_base[json_aoc_key] = aoc_info
    return json.dumps(json_base)

def get_aoc_list_json(aoc_list):
    #Takes in a list of aoc's as input and outputs a json of the names and ids
    json_base = {}
    aoc_index = 0
    for aoc in aoc_list:
        json_aoc_key = "aoc"+str(aoc_index)
        aoc_info = {'name' : aoc.aoc_name,
                    'id' : aoc.aoc_id}
        aoc_index = aoc_index+1
        json_base[json_aoc_key] = aoc_info
    return json.dumps(json_base)

def get_lacs_json(user):
    json_base = {}
    lac_index = 0
    lac = get_aocs_by_type('lac')[0]
    lac_list = get_requirements_with_tag(lac.aoc_id)
    for req in lac_list:
        json_lac_key = "LAC"+str(lac_index)
        lac_info = {'name' : req.Tags.tag_name}
        classes_fulfilling = get_potential_classes(req.Tags.tag_id, user.year_started)
        classes_taken = check_classes_taken(user.user_id, classes_fulfilling)
        fulfilled = False
        if len(classes_taken) >= req.Requirements.num_req:
            fulfilled = True
        lac_info['fulfilled'] = fulfilled
        classes = get_classes_taken(user, da_tag_id=req.Tags.tag_id)
        courses = []
        for da_class in classes:
            courses.append(da_class.class_name)
        lac_info['courses'] = courses
        json_base[json_lac_key] = lac_info
        lac_index = lac_index+1
    return json_base

def get_all_classes():
    class_query = Classes.query.all()
    return class_query

def get_all_classes_by_year(da_year):
    class_query = Classes.query.filter(Classes.class_year >= da_year).all()
    return class_query

#Delete functions
def merge_and_delete(to_delete):
    item = SESSION.merge(to_delete)
    SESSION.delete(item)
    SESSION.commit()

def delete_user(user):
    #Delete dependencies in ClassTaken and PrefAoc
    classes_taken = ClassTaken.query.filter_by(student_id=user.user_id).all()
    for classes in classes_taken:
        merge_and_delete(classes)
    pref_aocs_query = PrefferedAocs.query.filter_by(user_id=user.user_id).all()
    for pref_aoc in pref_aocs_query:
        merge_and_delete(pref_aoc)
    merge_and_delete(user)

def delete_class_taken(user_id, class_id):
    classes_taken = ClassTaken.query.filter_by(student_id=user_id
                                               ).filter_by(class_id=class_id).all()
    for class_taken in classes_taken:
        merge_and_delete(class_taken)

def delete_tag(tag):
    #Delete dependancies
    class_tags = ClassTags.query.filter_by(tag_id=tag.tag_id).all()
    for class_tag in class_tags:
        merge_and_delete(class_tag)
    reqs = Requirements.query.filter_by(tag_id=tag.tag_id).all()
    for req in reqs:
        merge_and_delete(req)
    merge_and_delete(tag)

def delete_class(da_class):
    class_tags = ClassTags.query.filter_by(class_id=da_class.class_id).all()
    for class_tag in class_tags:
        merge_and_delete(class_tag)
    classes_taken = ClassTaken.query.filter_by(class_id=da_class.class_id).all()
    for class_taken in classes_taken:
        merge_and_delete(class_taken)
    merge_and_delete(da_class)

def delete_class_tag(da_tag_id, da_class_id):
    class_tags = ClassTags.query.filter_by(tag_id=da_tag_id
                                           ).filter_by(class_id=da_class_id).all()
    for class_tag in class_tags:
        merge_and_delete(class_tag)

def delete_prereq(da_prereq_id, da_chosen_id):
    prereqs = Prereqs.query.filter_by(prereq_tag_id=da_prereq_id
                                      ).filter_by(chosen_tag_id=da_chosen_id).all()
    for prereq in prereqs:
        merge_and_delete(prereq)

def delete_requirement(requirement):
    merge_and_delete(requirement)

def delete_pref_aoc(user_id, aoc_id):
    pref_aocs = PrefferedAocs.query.filter_by(user_id=user_id).filter_by(aoc_id=aoc_id).first()
    merge_and_delete(pref_aocs)

def delete_aoc(aoc):
    pref_aocs_query = PrefferedAocs.query.filter_by(aoc_id=aoc.aoc_id).all()
    for pref_aoc in pref_aocs_query:
        merge_and_delete(pref_aoc)
    reqs = Requirements.query.filter_by(aoc_id=aoc.aoc_id).all()
    for req in reqs:
        merge_and_delete(req)
    merge_and_delete(aoc)
