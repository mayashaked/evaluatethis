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
import json 

def main(evals_file, question_file):
    #import all evals
    csv.field_size_limit(sys.maxsize)
    evals = []
    with open(evals_file) as f:
        reader = csv.reader(f)
        for row in reader:
            evals.append(row[0])

    #import list of questions from a text file
    #list of questions is made with some wild trickery in another file
    question_list = []
    with open(question_file) as f:
        reader = csv.reader(f)
        for row in reader:
            question_list.append(row)

    eval_list = []

    #compile regular expression to search for instructor name
    instructor = re.compile("\nInstructor\(s\): (.*)\n")

    for e in evals:
        response_dict = {}
        e_list = e.split('\n') #splits evaluations into lines

        prof = instructor.match(e_list[4]) #the name of the instructor is always on the fourth line of the evaluation
        response_dict['instructor'] = prof

        for i, line in enumerate(e_list):

            # extracts the time demands info, should work well
            if 'How many hours per week did you' in line:
                time = []
                time.append(e.split('\n')[i+1:i+4])
                response_dict['time_stats'] = time

            try:
                q = re.match('.*\?', line).group(0)
                if q in question_list:
                    response_dict[q] = []
                    # insert some clever shit here


            except:
                pass

            if line in question_list:
                question = line
                print(question)
                response_dict[question] = []

            if line not in question_list:
                if len(response_dict) > 0:
                    response_dict[question].append(line)

        eval_list.append(response_dict)

    


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
