#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      alex
#
# Created:     06/02/2018
# Copyright:   (c) alex 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import csv

def get_questions(csv_path):
    evaluations = []

    with open(csv_path) as f:
        reader = csv.reader(f)
        for row in reader:
            evaluations.append(row)

    all_lines = []

    for e in evaluations:
        lines = e.split('\n')
        all_lines.extend(lines)

    question_canidates = []
    for line in all_lines:
        if '?' in line:
            question_canidates.append(line)

    unique_canidates = set(question_canidates)
    filtered_canidates = []

    for q in unique_canidates:
        if question_canidates.count(q) >= 3:
            filtered_canidates.append(q)






if __name__ == '__main__':
    get_questions(sys.argv[1])
