#-------------------------------------------------------------------------------
# Name:        Get Questions
# Purpose:     Loads evaluations csv file and searches for lines that might be
#              questions/prompts in the evaluation. It's critical to have an
#              accurate list of 'questions' so we can extract the responses
#              and data we need later. Note that this heuristic of looking for
#              question marks is imperfect, so some intuition and manual work
#              went into cleaning/massaging the final question lists.
#
# Author:      Alex Maiorella
#
# Created:     02/06/2018
#-------------------------------------------------------------------------------
import csv
import sys
import re

def get_questions(csv_path):
    '''
    Finds questions in the raw evaluation text by looking for lines ending with
    question marks, then filtering them by frequency to eliminate most cases of
    student responses ending with a question. Takes a bit of time to run on
    full evals csv.
    Inputs:
        path to csv of all evaluation test
    '''
    csv.field_size_limit(sys.maxsize)
    evaluations = []
    print(csv_path)
    with open(csv_path) as f:
        reader = csv.reader(f)
        for row in reader:
            evaluations.append(row)

    all_lines = []

    for e in evaluations:
        # Each 'line' (question or response) in the text is separated by '\n'
        lines = e[0].split('\n')
        all_lines.extend(lines)

    question_canidates = []
    for line in all_lines:
        if '?' in line:
            question = re.match('.*\?', line).group(0)
            question_canidates.append(question)

    unique_canidates = list(set(question_canidates))
    filtered_canidates = []

    # Filter questions to weed out random student responses. (e.g. "huh?")
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
            get_questions('unique_evals.csv') # For convenience
        except:
            print('Arguement is path to evaluations csv file')
