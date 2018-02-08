#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      alex
#
# Created:     07/02/2018
# Copyright:   (c) alex 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import csv
import sys
import re

def main(evals_file, question_file):

    evals = []
    with open(evals_file) as f:
        reader = csv.reader(f)
        for row in reader:
            evals.append(row[0])

    question_list = []
    with open(question_file) as f:
        reader = csv.reader(f)
        for row in reader:
            question_list.append(row)

    instructor = re.compile("\nInstructor\(s\): (.*)\n")

    for e in evals:
        e_list = e.split('\n')
        i = instructor.match(e_list[4])
        for line in e_list:
            if line in question_list:
                question = line
                response_dict[question] = []
            if line not in question_list:
                if len(response_dict) > 0:
                    response_dict[question].append(line)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
