from .db_helper import (assign_aoc,
                        create_class,
                        create_aoc,
                        get_aoc,
                        get_aocs_by_type,
                        get_class,
                        get_classes_taken,
                        get_preffered_aocs,
                        get_tag,
                        get_user,
                        make_user,
                        take_class)
from .models import (SemesterType,
                     UserType)

def db_helper_test():
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
    create_aoc(aoc_info, tags, amounts)
    comp_sci = get_aoc("Computer Science (Regular)", "Divisonal")
    print(comp_sci)
    print(get_aocs_by_type("Divisonal"))
    for tag in tags:
        print(get_tag(tag))
    #Test class
    class_info = ["Introduction to Programming With Python", SemesterType.FALL, 2018, 1]
    create_class(class_info, [tags[0]])
    da_class = get_class("Introduction to Programming With Python")
    print(da_class)
    #Test user
    make_user("harry.potter97@ncf.edu", "Harry", 1997, UserType.STUDENT)
    student = get_user("harry.potter97@ncf.edu")
    print(student)
    #set preferred AOCS
    assign_aoc(comp_sci, student)
    print(get_preffered_aocs(student, "Divisonal"))
    #set taken class
    take_class(da_class, student)
    print(get_classes_taken(student))
