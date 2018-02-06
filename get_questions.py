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
import sys
import re

def get_questions(csv_path):

    csv.field_size_limit(sys.maxsize)
    evaluations = []

    with open(csv_path, encoding = 'utf8') as f:
        reader = csv.reader(f)
        for row in reader:
            evaluations.append(row)

    all_lines = []

    for e in evaluations:
        lines = e[0].split('\n')
        all_lines.extend(lines)

    question_canidates = []
    for line in all_lines:
        if '?' in line:
            question = re.match('.*\?', line)[0]
            question_canidates.append(question)

    unique_canidates = set(question_canidates)
    filtered_canidates = []

    for q in unique_canidates:
        if question_canidates.count(q) >= 3:
            filtered_canidates.append(q)


    with open('eval_questions.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows([[q] for q in filtered_canidates])

if __name__ == '__main__':
    try:
        get_questions(sys.argv[1])
    except:
        try:
            get_questions('C:/Users/alex/Desktop/unique_evals.csv')
        except:
            print('Arguement is path to evaluations csv file')
