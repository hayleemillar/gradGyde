#pylint: disable=R0915
from .db_helper import (assign_aoc,
                        assign_prereqs,
                        check_class_taken,
                        check_classes_taken,
                        create_class,
                        create_aoc,
                        delete_aoc,
                        delete_class,
                        delete_class_tag,
                        delete_class_taken,
                        delete_prereq,
                        delete_requirement,
                        delete_tag,
                        delete_user,
                        get_all_classes,
                        get_all_classes_by_year,
                        get_aoc,
                        get_aoc_json,
                        get_aocs_by_type,
                        get_class,
                        get_classes_taken,
                        get_class_tags,
                        get_potential_classes,
                        get_preffered_aocs,
                        get_prereqs,
                        get_requirements,
                        get_requirements_with_tag,
                        get_tag,
                        get_tag_by_id,
                        get_user,
                        make_requirement,
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
    aoc_info = ["Computer Science (2)", "aoc", 2018]
    create_aoc(aoc_info, tags, amounts)
    print("Getting aoc...")
    comp_sci = get_aoc("Computer Science (2)", "aoc")
    print(comp_sci)
    print("Getting aoc by type...")
    print(get_aocs_by_type("aoc"))
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
    print(get_preffered_aocs(student, "aoc"))

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
    print(get_potential_classes(get_tag(tags[0]).tag_id, 2014))

    #Testing prereqs
    print("Making prereq...")
    assign_prereqs(get_tag(tags[0]), get_tag(tags[1]))
    print(get_tag_by_id(get_prereqs(get_tag(tags[1]).tag_id)[0].prereq_tag_id))

    #Testing requirements
    print("Making requirement...")
    make_requirement(comp_sci.aoc_id, get_tag(tags[0]).tag_id, amounts[1])
    print(get_requirements(comp_sci.aoc_id))
    print(get_requirements_with_tag(comp_sci.aoc_id))

    #testing check class taken
    print("Checking check_classes_taken... This should be true")
    print(check_class_taken(student.user_id, class3.class_id))
    print("This should be false")
    class_info = ["Taken is False", SemesterType.SUMMER, 2099, 3]
    create_class(class_info, tags[0])
    false_class = get_class("Taken is False")
    print(check_class_taken(student.user_id, false_class.class_id))

    #Testing get classes tgae are taken
    print("Checking classes taken that fulfill requirement")
    print(check_classes_taken(student.user_id,
                              get_potential_classes(get_tag(tags[1]).tag_id, 2014)))

    #Testing get_aoc_json
    print("Getting the aoc json...")
    print(get_aoc_json(student, "aoc"))

    #Testing delete
    # print("Testing delete class taken. Test 3 should be gone...")
    # delete_class_taken(student.user_id, class3.class_id)
    # print(get_classes_taken(student))

    # print("Testing delete tag...")
    # delete_tag(get_tag(tags[3]))
    # print(get_tag(tags[3]))

    # print("Testing delete class...")
    # delete_class(false_class)
    # print(get_class("Taken is False"))

    # print("Testing delete class_tag. Test 2 should be gone...")
    # delete_class_tag(class2.class_id, get_tag(tags[0]).tag_id)
    # print(get_class_tags(class2.class_id))

    # print("Testing delete prereq")
    # delete_prereq(get_tag(tags[0]).tag_id, get_tag(tags[1]).tag_id)
    # print(get_prereqs(get_tag(tags[1]).tag_id))

    # print("Testing delete requirement... Requirement 3 should be gone")
    # delete_requirement(get_requirements(comp_sci.aoc_id)[2])
    # print(get_requirements(comp_sci.aoc_id))

    # print("Testing delete aoc...")
    # delete_aoc(comp_sci)
    # print(get_aoc("Computer Science (Regular)", "aoc"))

    # print("Testing delete user...")
    # delete_user(student)
    # print(get_user("harry.potter97@ncf.edu"))
