from .db_helper import (assign_aoc,
                        create_class,
                        create_aoc,
                        get_all_classes,
                        get_all_classes_by_year,
                        get_aoc,
                        get_aocs_by_type,
                        get_class,
                        get_classes_taken,
                        get_class_tags,
                        get_potential_classes,
                        get_preffered_aocs,
                        get_tag,
                        get_user,
                        make_user,
                        take_class)
from .models import (SemesterType,
                     UserType)

def db_helper_test():
    #make_tag list
    print("Making tags...")
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
    print("Printing tags...")
    print(tags)
    print("Printing tag amounts...")
    print(amounts)

    #create the AOC
    print("Creating aoc")
    aoc_info = ["Computer Science (Regular)", "Divisonal", 2018]
    create_aoc(aoc_info, tags, amounts)
    print("Getting aoc...")
    comp_sci = get_aoc("Computer Science (Regular)", "Divisonal")
    print(comp_sci)
    print("Getting aoc by type...")
    print(get_aocs_by_type("Divisonal"))
    print("Getting tags...")
    for tag in tags:
        print(get_tag(tag))

    #Test class
    print("Creating a class...")
    class_info = ["Introduction to Programming With Python", SemesterType.FALL, 2018, 1]
    create_class(class_info, [tags[0], tags[1]])
    print("Getting the class I made...")
    da_class = get_class("Introduction to Programming With Python")
    print(da_class)

    #Test user
    print("Making user...")
    make_user("harry.potter97@ncf.edu", "Harry", 1997, UserType.STUDENT)
    print("Getting user...")
    student = get_user("harry.potter97@ncf.edu")
    print(student)

    #set preferred AOCS
    print("Setting preffered aoc...")
    assign_aoc(comp_sci, student)
    print("Getting preffered aoc...")
    print(get_preffered_aocs(student, "Divisonal"))

    #test getting class tags
    print("Getting class tags...")
    da_class_tags = get_class_tags(da_class.class_id)
    print(da_class_tags)

    #set taken class
    print("Creating classes for testing get_classes_taken...")
    take_class(da_class, student)
    class_info = ["Test 1", SemesterType.FALL, 2019, 1]
    create_class(class_info, [tags[0], tags[3]])
    class1 = get_class("Test 1")
    take_class(class1, student)
    class_info = ["Test 2", SemesterType.FALL, 2017, 1]
    create_class(class_info, [tags[0], tags[3]])
    class2 = get_class("Test 2")
    take_class(class2, student)
    class_info = ["Test 3", SemesterType.SPRING, 2018, 1]
    create_class(class_info, [tags[0], tags[1]])
    class3 = get_class("Test 3")
    take_class(class3, student)
    #test get_taken_classes
    take_class(da_class, student)
    print("Testing get_classes_taken without params...")
    print(get_classes_taken(student))
    print("Testing get_classes_taken with Semester...")
    print(get_classes_taken(student, semester=SemesterType.FALL))
    print("Testing get_classes_taken with Year...")
    print(get_classes_taken(student, da_year=2018))
    print("Testing get_classes_taken with Name...")
    print(get_classes_taken(student, da_name="Test 3"))
    print("Testing get_classes_taken with Tag ID...")
    print(get_classes_taken(student, da_tag_id=get_tag(tags[1]).tag_id))
    print("Testing with all 4 params")
    print(get_classes_taken(student, semester=SemesterType.SPRING,
                            da_year=2018, 
                            da_tag_id=get_tag(tags[1]).tag_id,
                            da_name="Test 3"))
    print("Testing get_all_classes...")
    class_info = ["All test", SemesterType.FALL, 2014, 1]
    create_class(class_info, [tags[0], tags[3]])
    print(get_all_classes())
    print("Testing get_all_classes_by_year... All test should not be present...")
    print(get_all_classes_by_year(2017))

    #Testing potential courses
    print("Getting potential classes...")
    print(get_potential_classes_by_tag(get_tag(tags[0]).tag_id, 2014))



