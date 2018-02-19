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

def main():
    df = pd.read_json('C:/Users/alex/Desktop/evals_json_version_4_part2', convert_dates = False).head()
    df2 = df.copy().fillna(0)

    for row in df2.iterrows():
        if row[1].The_Instructor:
            instructor_score = compute_numerical_score(row[1].The_Instructor)
            df.loc[row[0], 'instructor_score'] = instructor_score
        if row[1].The_Assignments:
            assignments_score = compute_numerical_score(row[1].The_Assignments)
            df.loc[row[0], 'assignments_score'] = assignments_score
        if row[1].The_Tests:
            tests_score = compute_numerical_score(row[1].The_Tests)
            df.loc[row[0], 'tests_score'] = tests_score
        if row[1].Overall:
            overall_score = compute_numerical_score(row[1].Overall)
            df.loc[row[0], 'overall_score'] = overall_score

def compute_numerical_score(data):
    print(data)
    scores = []
    denominator = []

    for line in data:
        p = [int(a) for a in re.findall('([0-9][0-9]?[0-9]?)%', line)]
        print(p)
        if len(p) == 6:
        # first element is N/A percentage; don't factor it into weighted score/possible score
            weighted_score = p[1]+p[2]*2+p[3]*3+p[4]*4+p[5]*5
            possible_score = sum(p[1:])*5

        if len(p) == 5:
            weighted_score = p[0]+p[1]*2+p[2]*3+p[3]*4+p[4]*5
            possible_score = sum(p)*5


        scores.append(weighted_score)
        denominator.append(possible_score)

    return sum(scores) / sum(denominator)


if __name__ == '__main__':
    main()
