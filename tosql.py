#-------------------------------------------------------------------------------
# Name:        tosql
# Purpose:     creates 'courses', 'profs', 'crosslists', and 'evals' SQL tables from our json data
#
# Author:      Maya Shaked
#
# Created:     21/02/2018
#-------------------------------------------------------------------------------


import pandas as pd
import sqlite3
import aggregate_numerical_data as agg_num

EVALS_PART_1 = 'evals_json_version_5_part1'
EVALS_PART_2 = 'evals_json_version_5_part2'
SQL_DB_PATH = 'test2.db'

db = sqlite3.connect(SQL_DB_PATH)
j1 = pd.read_json(EVALS_PART_1, convert_dates = False)
j2 = pd.read_json(EVALS_PART_2, convert_dates = False)

j = pd.concat([j1, j2])

agg_num.add_score_cols(j)

j = j.where((pd.notnull(j)), None)
j = j.set_index('unique_id')


def gen_courses(j, db):

    courses = j[['course', 'course_number', 'dept', 'section', 'term', 'year']]

    sqldbcourses = courses.to_sql('courses', con = db, flavor = 'sqlite', index = True, index_label = 'course_id')

    pass

def gen_profs(j, db):


    profs = []
    for ind, row in j.iterrows():
        if type(row['instructors']) == list:
            for prof in row['instructors']:
                prof.lower()
                fullname = prof.split(', ')
                profs.append([ind, fullname[0], fullname[-1]])

    profs = pd.DataFrame(profs)
    profs = profs.rename(columns = {0 : 'course_id', 1: "fn", 2 : "ln"})
    sqldbprofs = profs.to_sql('profs', con = db, flavor = 'sqlite', index = False)

    pass

def gen_crosslists(j, db):

    crosslists = []
    for ind, row in j.iterrows():
        if type(row['identical_courses']) == str:
            x = row['identical_courses'].split(', ')
            for course in x:
                crosslists.append([ind, course])
                
    crosslists = pd.DataFrame(crosslists)
    crosslists = crosslists.rename(columns = {0 : 'course_id', 1 : 'crosslist'})
    sqldbcrosslists = crosslists.to_sql('crosslists', con = db, flavor = 'sqlite', index = False)

    pass

def gen_evals(j, db):

    evals = []
    for ind, row in j.iterrows():
        eval = [ind, 'NA', 'NA', 'NA', 'NA', 'NA', 0, 'NA', 'NA']
        if type(row['instructor_score']) == float:
            eval[1] = float(row['instructor_score'])
        if type(row['assignments_score']) == float:
            eval[2] = float(row['assignments_score'])
        if type(row['overall_score']) == float:
            eval[3] = float(row['overall_score'])
        if type(row['readings_score']) == float:
            eval[4] = float(row['readings_score'])
        if type(row['tests_score']) == float:
            eval[5] = float(row['tests_score'])
        eval[6] = row['num_responses']
        if type(row['recommend']) == list:
            eval[7] = int(row['recommend'][0])
            eval[8] = int(row['recommend'][1])


        evals.append(eval)

    evals = pd.DataFrame(evals)

    evals = evals.rename(columns = {0 : 'course_id', 1 : 'prof_score', 2 : 'ass_score', 3 : 'over_score' , 4 : 'read_score', 5 : 'test_score', 6 : 'num_responses', 7 : 'num_recommend', 8 : 'num_dont_recommend'})

    sqldbevals = evals.to_sql('evals', con = db, flavor = 'sqlite', index = False)

    pass


gen_courses(j, db)
gen_profs(j, db)
gen_crosslists(j, db)
gen_evals(j, db)

