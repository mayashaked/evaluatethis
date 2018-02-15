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

EXACT_MATCH_ONLY = ['overall', 'explain', 'the content material', 'useful?',
 'exams', 'the tests', 'the textbook', 'this course', 'the homework assignments',
 'very useful', 'labs', 'level', 'the instructor', 'Useful?', 'Texts?', 'the assignments', 'Weaknesses?', 'Strengths?']

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
            question_list.append(row[0])

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
    instructor = re.compile("Instructor\(s\): (.*)")
    eval_list = []

    for e in evals[:500]:
        num_responses = int(e.split('\n')[7][-2:])
        in_question = False
        answers = []
        response_dict = {}
        e_list = e.split('\n') #splits evaluations into lines

        prof = instructor.match(e_list[5]) #the name of the instructor is always on the fourth line of the evaluation
        response_dict['instructor(s)'] = None
        if prof:
            response_dict['instructor(s)'] = prof.group(1).split('; ')
        course_info_match = re.match('([A-Z]{4}) ([0-9]{5}): (.*)', e_list[3])
        response_dict['responses'] = num_responses
        response_dict['dept'] = course_info_match.group(1)
        response_dict['course_number'] = course_info_match.group(2)
        response_dict['course'] = course_info_match.group(3)

        responses_found = 0
        for i, line in enumerate(e_list):
            if in_question and stopping_cond(line, question_list, responses_found, num_responses):
                response_dict[q].extend(answers)
                in_question = False

            if in_question:
                answers.append(line)
                responses_found += 1

            for l in course_qs:
                if l in line:
                    q = 'course_responses'
                    response_dict[q] = []
                    in_question = True
                    answers = []
                    responses_found = 0
                    break

            for l in instructor_qs:
                if l in line or line in ['Weaknesses?', 'Strengths?']:
                    q = 'instructor_responses'
                    response_dict[q] = []
                    in_question = True
                    answers = []
                    responses_found = 0
                    break

            # extracts the time info, works independently
            if 'How many hours per week did you' in line:
                try:
                    time = []
                    time.extend([re.search('Answer ([0-9]\.?[0-9]?)', l).group(1) for l in e_list[i+1:i+4]])
                    response_dict['time_stats'] = time
                except:
                    pass

        eval_list.append(response_dict)
    return eval_list

def stopping_cond(line, question_list, responses_found, num_responses):
    if responses_found == num_responses:
        return True

    if re.search('[0-9][0-9]? / [0-9][0-9]?%', line):
        return True

    if line in EXACT_MATCH_ONLY:
        return True

    for q in question_list:
        if q in line:
            if q != line:
                print((q,line))

    return False

    #writes to json
    '''
    with open('eval_list', 'w') as outfile:
    json.dump(eval_list, outfile)
    '''


if __name__ == '__main__':
    try:
        main('C:/Users/alex/Desktop/unique_evals.csv', 'C:/Users/alex/Desktop/manually_cleaned_eval_questions.csv', 'C:/Users/alex/Desktop/course_quality_questions.csv', 'C:/Users/alex/Desktop/instructor_quality_questions.csv')
    except:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
