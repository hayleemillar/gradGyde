import os
import csv
from .db_helper import create_aoc, create_class
from .models import SemesterType

def parse_aocs(file_path):
    with open(file_path, 'r') as file:
        aocs = csv.reader(file, delimiter="\t")
        aoc_info = []
        tags = []
        amounts = []
        for line in aocs:
            if line[0] != "Name":
                aoc_type = line[1].lower()
                if aoc_type == "joint":
                    aoc_type = "double"
                aoc_info = [line[0], aoc_type, int(line[2], 10)]
                tags = []
                amounts = []
                count = 3
                while count < len(line) and line[count] != "":
                    combined = line[count].split("(")
                    cur_tag = combined[0]
                    cur_amount = int(combined[1].split(")")[0], 10)
                    tags.append(cur_tag)
                    amounts.append(cur_amount)
                    count += 1
                create_aoc(aoc_info, tags, amounts)

def parse_class(file_path):
    with open(file_path, 'r') as file:
        classes = csv.reader(file, delimiter="\t")
        class_info = []
        tags = []
        for line in classes:
            period = line[0].split(" ")
            if period[0].lower() == "spring":
                term = SemesterType.SPRING
            elif period[0].lower() == "fall":
                term = SemesterType.FALL
            elif period[0].lower() == "summer":
                term = SemesterType.SUMMER
            elif period[0].lower() == "isp":
                term = SemesterType.ISP
            if line[1] == "Term":
                credit = 1
            else:
                credit = .5
            class_info = [line[2], term, int(period[1], 10), credit]
            tags = []
            count = 3
            while count < len(line) and line[count] != "":
                tags.append(line[count])
                count += 1
            create_class(class_info, tags)

def parse():
    aoc_file = os.getcwd() + "/gradGyde/tsv_resources/aocs.tsv"
    parse_aocs(aoc_file)
    class_file = os.getcwd() + "/gradGyde/tsv_resources/classes.tsv"
    parse_class(class_file)
