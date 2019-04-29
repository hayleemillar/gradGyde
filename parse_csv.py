import sqlite3
import os
# import sys
# sys.path.append()
import csv
from gradGyde.db_helper import create_aoc

def parse_aocs(file_path):
    with open(file_path, 'r') as file:
        aocs = csv.reader(file, delimiter="\t")
        aoc_info = []
        tags = []
        amounts = []
        for line in aocs:
            if line[0] != "Name":
                aoc_info = [line[0],line[1],int(line[2],10)]
                tags = []
                amounts = []
                count = 3
                while count < len(line) and line[count] != "":
                    combined = line[count].split("(")
                    curTag = combined[0]
                    curAmount = int(combined[1].split(")")[0],10)
                    tags.append(curTag)
                    amounts.append(curAmount)
                    count += 1
                create_aoc(aoc_info,tags,amounts)
        

def main():
    aoc_file = os.getcwd() + "/aocs.tsv"
    parse_aocs(aoc_file)

    
if __name__ == '__main__':
    main()
