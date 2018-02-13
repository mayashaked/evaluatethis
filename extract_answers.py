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

def main(evals_file, all_question_file, course_q, instructor_q):
    #import all evals
    csv.field_size_limit(sys.maxsize)
    evals = []
    with open(evals_file, encoding = 'ISO-8859-1') as f:
        reader = csv.reader(f)
        for row in reader:
            evals.append(row[0])

    #import list of questions from a text file
    #list of questions is made with some wild trickery in another file
    question_list = []
    with open(all_question_file, encoding = 'ISO-8859-1') as f:
        reader = csv.reader(f)
        for row in reader:
            question_list.append(row)

    course_qs = []
    with open(course_q, encoding = 'ISO-8859-1') as f:
        reader = csv.reader(f)
        for row in reader:
            course_qs.append(row[0])

    instructor_qs = []
    with open(instructor_q, encoding = 'ISO-8859-1') as f:
        reader = csv.reader(f)
        for row in reader:
            instructor_qs.append(row[0])


    #compile regular expression to search for instructor name
    instructor = re.compile("\nInstructor\(s\): (.*)\n")

    for e in evals:
        num_responses = int(e.split('\n')[7][-2:])
        in_question = False
        answers = []
        response_dict = {}
        e_list = e.split('\n') #splits evaluations into lines

        prof = instructor.match(e_list[4]) #the name of the instructor is always on the fourth line of the evaluation
        response_dict['instructor'] = prof

        for i, line in enumerate(e_list):

            if stopping_cond(line):
                response_dict[q].append(answers)
                in_question = False

            if in_question:
                answers.append(line)

            for l in course_qs:
                if l in line:
                    q = 'course'
                    in_question = True
                    answers = []
                    responses_found = 0
                    break

            for l in instructor_qs:
                if l in line:
                    q = 'instructor'
                    in_question = True
                    answers = []
                    responses_found = 0
                    break

            # extracts the time info, works independently
            if 'How many hours per week did you' in line:
                time = []
                time.append(e.split('\n')[i+1:i+4])
                response_dict['time_stats'] = time


        eval_list.append(response_dict)
        return eval_list
    
def stopping_cond():
    if responses_found == num_responses:
        return True

    if 


    #writes to json
    '''
    with open('eval_list', 'w') as outfile:
    json.dump(eval_list, outfile)
    '''


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
