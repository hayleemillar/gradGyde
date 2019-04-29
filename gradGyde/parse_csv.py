import sqlite3
import os
import csv
from .db_helper import create_aoc

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
                aoc_info = [line[0], aoc_type,int(line[2], 10)]
                tags = []
                amounts = []
                count = 3
                while count < len(line) and line[count] != "":
                    combined = line[count].split("(")
                    curTag = combined[0]
                    curAmount = int(combined[1].split(")")[0], 10)
                    tags.append(curTag)
                    amounts.append(curAmount)
                    count += 1
                create_aoc(aoc_info, tags, amounts)

def parse_class(file_path):
    with open(file_path, 'r') as file:
        classes = csv.reader(file, delimiter="\t")
        class_info = []
        tags = []
        for line in classes:
            if line[0] != "Name":
                class_info = [line[0], line[1], int(line[2], 10), int(line[3], 10)]
                tags = []
                count = 4
                while count < len(line) and line[count] != "":
                    tags.append(line[count])
                    count += 1
                create_class(class_info, tags)

def parse():
    aoc_file = os.getcwd() + "/gradGyde/tsv_resources/aocs.tsv"
    parse_aocs(aoc_file)
    # class_file = os.getcwd() + "/gradGyde/tsv_resources/classes.tsv"
    # parse_class(class_file)