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

EXACT_MATCH_ONLY = {'overall', 'explain', 'the content material', 'useful?',
 'exams', 'the tests', 'the textbook', 'this course', 'the homework assignments',
 'very useful', 'labs', 'level', 'the instructor','texts?', 'additional comments'
 'the assignments', 'weaknesses?', 'strengths?', 'anyone interested in the topic', 'written comments', 'which least?'}

def main(evals_file, all_question_file, course_q, instructor_q, file):

    csv.field_size_limit(sys.maxsize)

    evals = []
    with open(evals_file, encoding = 'ISO-8859-1') as f:
        reader = csv.reader(f)
        for row in reader:
            evals.append(row[0])

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

    eval_list = iterate(evals, question_list, course_qs, instructor_qs)
    write_to_json(eval_list, file)


def iterate(evals, question_list, course_qs, instructor_qs):

    #compile regular expression to search for instructor name
    instructor_re = re.compile("Instructor\(s\): ?(.*)")
    course_info_re = re.compile('([A-Z]{4}) ([0-9]{5}): ?(.*)')
    num_responses_re = re.compile('esponses: ?([0-9]*)')
    eval_list = []

    for e in evals:
        e_list = e.split('\n') #splits evaluations into lines
        in_question = False
        answers = []
        response_dict = {}
        
        for header_line in e_list[:10]: # deal seperately with header rows to avoid conflicts

            if course_info_re.match(header_line):
                course_info_match = course_info_re.match(header_line)
                response_dict['dept'] = course_info_match.group(1)
                response_dict['course_number'] = course_info_match.group(2)
                response_dict['course'] = course_info_match.group(3)

            if instructor_re.match(header_line):
                prof = instructor_re.match(header_line)
                response_dict['instructor(s)'] = prof.group(1).split('; ')

            if num_responses_re.search(header_line):
                num_responses = num_responses_re.search(header_line)
                response_dict['num_responses'] = num_responses.group(1)


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
                if l in line or line.lower() in ['weaknesses?', 'strengths?']:
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
    if '©' in line:
        return True

    if num_responses != 0 and responses_found == num_responses: # Don't trust response number if it says zero
        return True

    if re.search('[0-9][0-9]? / [0-9][0-9]?%', line):
        return True

    if line.lower() in EXACT_MATCH_ONLY:
        return True

    for q in question_list:
        if q.lower() in line.lower():
            '''if q != line and 'Strengths' not in line and 'Weaknesses' not in line:
                                                    print((q,line))'''
            return True

    return False


def write_to_json(eval_list, file):
    
    with open(file, 'w', encoding = 'ISO-8859-1') as outfile:
        json.dump(eval_list, outfile)
    


if __name__ == '__main__':
    main('/home/alexmaiorella/Downloads/unique_evals.csv', '/home/alexmaiorella/Downloads/manually_cleaned_eval_questions.csv', 
        '/home/alexmaiorella/Downloads/course_quality_questions.csv', '/home/alexmaiorella/Downloads/instructor_quality_questions.csv',
        '/home/alexmaiorella/Downloads/evals_json_version_1')
