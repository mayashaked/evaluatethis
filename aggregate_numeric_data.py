#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      alex
#
# Created:     18/02/2018
# Copyright:   (c) alex 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# The goal here is to reduce agree/disagree type data of the following form into
# a single float representing a score for the intructor/course overall/
# assignments.

###################################################################

# 'N/A|Strongly Disagree|Disagree|Neutral|Agree|Stongly Agree'
# 'Presented clear lectures. 5% 0% 0% 0% 21% 73%'
# 'Held my attention and made this course interesting. 0% 0% 0% 5% 47% 47%'
# 'Stimulated and facilitated questions and discussions. 0% 0% 0% 5% 21% 73%'
# 'Responded well to student questions. 0% 0% 0% 0% 10% 89%'
# 'Was available outside of class. 33% 0% 0% 5% 16% 44%'
# 'Was helpful during office hours. 50% 0% 0% 0% 11% 38%'
# 'Motivated independent thinking. 0% 0% 0% 5% 31% 63%',
# 'Made me want to take another course from him or her. 0% 0% 0% 15% 15% 68%'

###################################################################
import re
import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def add_score_cols(df):

    sia = SentimentIntensityAnalyzer()

    # initialize new columns, 'concat' them later
    # we find this approach runs faster than adding values to df 1 at a time
    emp = list([np.nan for a in range(len(df))])
    inst_sentiment_col = pd.Series(emp, name = 'inst_sentiment')
    assignments_score_col = pd.Series(emp, name = 'assignments_score')
    readings_score_col = pd.Series(emp, name = 'readings_score_col')
    instructor_score_col = pd.Series(emp, name = 'instructor_score')
    tests_score_col = pd.Series(emp, name = 'tests_score')
    course_sentiment_col = pd.Series(emp, name = 'course_sentiment')
    overall_score_col = pd.Series(emp, name = 'overall_score')

    for row in df.iterrows():

        # The following complication is neccesary because some physics
        # evaluations have agree...disagree rather than vice versa
        reverse_order = False
        if row[1].dept == 'PHYS':
            reverse_order = True
        if row[1].dept == 'PHSC':
            reverse_order = 'maybe'

        if type(row[1].The_Instructor) == list:
            instructor_score = compute_numerical_score(row[1].The_Instructor, reverse_order)
            instructor_score_col[row[0]] = instructor_score
        if type(row[1].The_Assignments) == list:
            assignments_score = compute_numerical_score(row[1].The_Assignments, reverse_order)
            assignments_score_col[row[0]] = assignments_score
        if type(row[1].The_Tests) == list:
            tests_score = compute_numerical_score(row[1].The_Tests, reverse_order)
            tests_score_col[row[0]] = tests_score
        if type(row[1].Overall) == list:
            overall_score = compute_numerical_score(row[1].Overall, reverse_order)
            overall_score_col[row[0]] = overall_score
        if type(row[1].The_Readings) == list:
            readings_score = compute_numerical_score(row[1].The_Readings, reverse_order)
            readings_score_col[row[0]] = readings_score

        if type(row[1].course_responses) == list:
            length = len(row[1].course_responses)
            if length >= 1:
                course_sentiment = round((np.mean([sia.polarity_scores(c)['compound'] for c in row[1].course_responses]) + 1)*50, 2)
                course_sentiment_col[row[0]] = round(weight_sent_scores(course_sentiment, length, 'course'), 1)

        if type(row[1].instructor_responses) == list:
            length = len(row[1].instructor_responses)
            if length >= 1:
                inst_sentiment = round((np.mean([sia.polarity_scores(c)['compound'] for c in row[1].instructor_responses]) + 1)*50, 2)
                inst_sentiment_col[row[0]] = round(weight_sent_scores(inst_sentiment, length, 'inst'), 1)

    return pd.concat([df, inst_sentiment_col, assignments_score_col, overall_score_col, \
            instructor_score_col, tests_score_col, course_sentiment_col], axis = 1)


def compute_numerical_score(data, reverse_order):

    scores = []
    denominator = []

    for line in data:
        p = [int(a) for a in re.findall('([0-9][0-9]?[0-9]?)%', line)]
        if reverse_order == True:
            p.reverse()

        if len(p) == 6:
        # first element is N/A percentage; don't factor it into weighted score/possible score
            weighted_score = p[1]+p[2]*2+p[3]*3+p[4]*4+p[5]*5
            possible_score = sum(p[1:])*5

        elif len(p) == 5:
            weighted_score = p[0]+p[1]*2+p[2]*3+p[3]*4+p[4]*5
            possible_score = sum(p)*5

        else:
            return np.nan

        scores.append(weighted_score)
        denominator.append(possible_score)

    if sum(denominator) == 0 or not data:
        return np.nan

    score = round(sum(scores) / sum(denominator) * 100, 1)

    # Make an educated guess that the order should be reversed, then recalculate
    if score <= 50 and reverse_order == 'maybe':
        return compute_numerical_score(data, True)

    return score

def weight_sent_scores(raw_score, num_responses, category):

    average = {'inst' : 75, 'course' : 62.5}

    if num_responses in range(1,5):
        normalized_raw_score = raw_score - average[category]
        adjusted = normalized_raw_score * (1 - .15 * (5 - num_responses))
        return adjusted + average[category]

    return raw_score

if __name__ == '__main__':
    main(df)
