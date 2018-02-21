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
 'the assignments', 'weaknesses?', 'strengths?', 'anyone interested in the topic',
 'written comments', 'which least?'}

AGREE_CATEGORIES = {'overall', 'the tests', 'the instructor', 'the assignments',
 'the readings', 'the homework assignments'}

AGREE_DISAGREE_INDICATORS = \
{'  n/a strongly disagree disagree neutral agree strongly agree',
 '  none little some a lot extremely vigorously',
 '  1 2 3 4 5',
 '  na no gains a little gain moderate gain good gain great gain',
 '  na 1-strongly disagree 2-disgree 3-neutral 4-agree 5-strongly agree',
 '  a-strongly agree b-agree c-neutral d-disagree e-strongly disagree'}

YES_NO = ['Would you recommend this class to another student?',
'Overall, would you say you had a good instructor?']

def main(evals_file, all_question_file, course_q, instructor_q, agree_disagree_q, file):

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

    agree_disagree_qs = []
    with open(agree_disagree_q, encoding = 'ISO-8859-1') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                agree_disagree_qs.append(row[0])

    eval_list = iterate(evals, question_list, course_qs, instructor_qs, agree_disagree_qs)
    write_to_json(eval_list, file)


def iterate(evals, question_list, course_qs, instructor_qs, agree_disagree_qs):
    '''
    Parse all of the evaluation text to locate all the desired features and extract them.

    Inputs:
        evaluation list, full list of questions, sub-lists of various types of q's
    Returns:
        list of dictionaries where each holds the information from one evaluation
    '''

    # compile regular expressions to find info from header rows
    instructor_re = re.compile("Instructor\(s\): ?(.+)")
    course_info_re = re.compile('([A-Z]{4}) ([0-9]{5}): ?(.*)')
    num_responses_re = re.compile('esponses: ?([0-9]*)')
    identical_courses_re = re.compile('Identical Courses: ?(.+)')
    section_year_re = re.compile('Section ([0-9][0-9]?) - ([a-zA-z]+) ([0-9]{4})')
    eval_list = []
    unique_id = 15000

    for e in evals[15000:]:
        e_list = e.split('\n') # splits evaluation into list of lines
        in_question = False
        in_num_question = False
        answers = []
        response_dict = {'unique_id' : unique_id}
        unique_id += 1

        for header_line in e_list[:10]: # deal seperately with header lines to avoid conflicts

            if course_info_re.match(header_line):
                course_info_match = course_info_re.match(header_line)
                response_dict['dept'] = course_info_match.group(1)
                response_dict['course_number'] = course_info_match.group(2)
                response_dict['course'] = course_info_match.group(3)

            if instructor_re.match(header_line):
                prof = instructor_re.match(header_line)
                response_dict['instructors'] = prof.group(1).split('; ')

            if num_responses_re.search(header_line):
                num_responses = num_responses_re.search(header_line)
                response_dict['num_responses'] = num_responses.group(1)

            if identical_courses_re.match(header_line):
                identical_courses = identical_courses_re.match(header_line)
                response_dict['identical_courses'] = identical_courses.group(1)

            if section_year_re.match(header_line):
                section_year = section_year_re.match(header_line)
                response_dict['section'] = section_year.group(1)
                response_dict['term'] = section_year.group(2)
                response_dict['year'] = section_year.group(3)

        responses_found = 0
        for i, line in enumerate(e_list):
            
            # Uses an on/off algorithm to extract responses to different types of questions
            # "in_question" is True whenever we are within the responses to a question
            # "in_num_question" further specifies that the question has numerical (agree...disagree) responses

            if in_question and stopping_cond(line, question_list, responses_found, num_responses):
                response_dict[q].extend(answers)
                in_question = False
                in_num_question = False

            if in_question:
                if in_num_question:
                    m = re.match('(.+) ([0-9][0-9]?[0-9]?% [0-9][0-9]?[0-9]?% [0-9][0-9]?[0-9]?% [0-9][0-9]?[0-9]?% [0-9][0-9]?[0-9]?% ?[0-9]?[0-9]?[0-9]?%?)', line)
                    if m:
                        answers.append(m.group(0))
                else:
                    answers.append(line)
                    responses_found += 1

            for l in course_qs:
                if l.lower() in line.lower():
                    q = 'course_responses'
                    if not q in response_dict:
                        response_dict[q] = []
                    in_question = True
                    answers = []
                    responses_found = 0
                    break

            for l in instructor_qs:
                if l.lower() in line.lower() or line.lower() in {'weaknesses?', 'strengths?'}:
                    q = 'instructor_responses'
                    if not q in response_dict:
                        response_dict[q] = []
                    in_question = True
                    answers = []
                    responses_found = 0
                    break

            if line in {'Why?', 'Please explain:', 'In what way?'} and e_list[i-5] == YES_NO[0]:
                q = 'course_responses'
                if not q in response_dict:
                    response_dict[q] = []
                in_question = True
                answers = []
                responses_found = 0

            if line in {'Why?', 'Please explain:', 'In what way?'} and e_list[i-5] == YES_NO[1]:
                q = 'instructor_responses'
                if not q in response_dict:
                    response_dict[q] = []
                in_question = True
                answers = []
                responses_found = 0

            if line.lower() in AGREE_DISAGREE_INDICATORS:
                if e_list[i-1].lower() in AGREE_CATEGORIES:
                    q = e_list[i-1].replace(' ', '_')
                    if q == 'The_Homework_Assignments':
                        q = 'The_Assignments'
                    response_dict[q] = []
                    in_question = True
                    in_num_question = True
                    answers = []
                if e_list[i-1].lower() == 'explain' and "rate instructor's ability" in e_list[i+1].lower():
                    # Deals with a formating corner case in some language evaluations
                    q = 'The_Instructor'
                    in_question = True
                    in_num_question = True
                    answers = []
                responses_found = 0


            # extracts the time info and yes/no answers, works independently of the mechanism above
            if re.match('How many hours per week (outside of attending required sessions )?did you spend on this course?', line) \
            or re.match('Hours / week?', line):
                try:
                    time_stats = [re.search('Answer ([0-9]\.?[0-9]?)', l).group(1) for l in e_list[i+1:i+4]]
                    response_dict['low_time'] = time_stats[0]
                    response_dict['avg_time'] = time_stats[1]
                    response_dict['high_time'] = time_stats[2]
                except:
                    pass

            if line in YES_NO and e_list[i+1] == 'Yes' and e_list[i+3] == 'No':
                try:
                    yes = re.match('([0-9][0-9]?) / [0-9][0-9]?[0-9]?%', e_list[i+2]).group(1)
                    no = re.match('([0-9][0-9]?) / [0-9][0-9]?[0-9]?%', e_list[i+4]).group(1)
                    if 'recommend' in line:
                        response_dict['recommend'] = (yes, no)
                    else:
                        response_dict['good_instructor'] = (yes, no)
                except:
                    pass


        eval_list.append(response_dict)
    return eval_list


def stopping_cond(line, question_list, responses_found, num_responses):
    '''
    This is a collection of situations where the question has ended and
    "in_question" should be turned off.

    Returns:
        boolean
    '''
    if '©' in line:
        return True

    if num_responses != 0 and responses_found == num_responses:
        # Don't trust response number if it says zero
        return True

    if re.search('[0-9][0-9]? / [0-9][0-9]?[0-9]?%', line):
        return True

    if line.lower() in EXACT_MATCH_ONLY:
        return True

    for q in question_list:
        if q.lower() in line.lower():
            return True

    return False


def write_to_json(eval_list, file):

    with open(file, 'w', encoding = 'ISO-8859-1') as outfile:
        json.dump(eval_list, outfile)


if __name__ == '__main__':
    main('C:/Users/alex/Desktop/unique_evals.csv', 'C:/Users/alex/Desktop/manually_cleaned_eval_questions.csv',
        'C:/Users/alex/Desktop/course_quality_questions.csv', 'C:/Users/alex/Desktop/instructor_quality_questions.csv',
        'C:/Users/alex/Desktop/agree-disagree_questions.csv', 'C:/Users/alex/Desktop/evals_json_version_4_part2')