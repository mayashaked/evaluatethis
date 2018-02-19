import pandas as pd
import sqlite3
import aggregate_numerical_data as agg_num

db = sqlite3.connect('test.db')
j1 = pd.read_json('evals_json_version_4_part1', convert_dates = False)
j2 = pd.read_json('evals_json_version_4_part2', convert_dates = False)

j = pd.concat([j1, j2])
j = agg_num.add_score_cols(j)

j = j.where((pd.notnull(j)), None)
j = j.set_index('unique_id')



courses = j[['course', 'course_number', 'dept', 'section', 'term', 'year']]

sqldbcourses = courses.to_sql('courses', con = db, flavor = 'sqlite', index = True, index_label = 'course_id')


profs = []
for ind, row in j.iterrows():
    if type(row['instructors']) == list:
        for prof in row['instructors']:
            prof.lower()
            ln, fn = prof.split(' ,')
            profs.append([ind, fn, ln])

profs = pd.DataFrame(profs)
profs = profs.rename(columns = {0 : 'course_id', 1: "fn", 2 : "ln"})
sqldbprofs = profs.to_sql('profs', con = db, flavor = 'sqlite', index = False)

crosslists = []
for ind, row in j.iterrows():
    if type(row['identical_courses']) == list:
        for crosslist in row['identical_courses']:
            crosslists.append([ind, crosslist])

crosslists = pd.DataFrame(crosslists)
crosslists = crosslists.rename(columns = {0 : 'course_id', 1 : 'crosslist'})
sqldbcrosslists = crosslists.to_sql('crosslists', con = db, flavor = 'sqlite', index = False)


evals = []
for ind, row in j.iterrows():
    eval = [ind, 'NA', 'NA', 'NA', 'NA', 'NA']
    if type(row['instructor_score']) float:
        eval[1] = row['instructor_score']
    if type(row['assignments_score']) == float:
        eval[2] = row['assignments_score']
    if type(row['overall_score']) == float:
        eval[3] = row['overall_score']
    if type(row['readings_score']) == float:
        eval[4] = row['readings_score']
    if type(row['tests_score']) == float:
        eval[5] = row['tests_score']
    evals.append(eval)
evals = pd.DataFrame(evals)

evals = evals.rename(columns = {0 : 'course_id', 1 : 'prof_score', 2 : 'ass_score' : 3 : 'over_score' , 4 : 'read_score', 5 : 'test_score'})

sqldbevals = evals.to_sql('evals', con = db, flavor = 'sqlite', index = False)
