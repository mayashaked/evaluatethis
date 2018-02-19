import pandas as pd
import sqlite3

db = sqlite3.connect('test.db')
j1 = pd.read_json('evals_json_version_3_part1', convert_dates = False)
j2 = pd.read_json('evals_json_version_3_part2', convert_dates = False)
j = pd.concat([j1, j2])
j = j.set_index('unique_id')

courses = j[['course', 'course_number', 'dept', 'section', 'term', 'year']]
sqldbcourses = courses.to_sql('courses', con = db, flavor = 'sqlite', index = True, index_label = 'course_id')

profs = []
for ind, row in j.iterrows():
	if type(row['instructors']) == list:
		for prof in row['instructor(s)']:
			ln, fn = prof.split(' ,')
			name = fn + ' ' + ln
			profs.append([ind, name])

profs = pd.DataFrame(profs)
profs = profs.rename(columns = {0 : 'course_id', 1: "prof"})
sqldbprofs = profs.to_sql('profs', con = db, flavor = 'sqlite', index = False)

crosslists = []
for ind, row in j.iterrows():
	if type(row['identical_courses']) == list:
		for crosslist in row['identical_courses']:
			crosslists.append([ind, crosslist])
			
crosslists = pd.DataFrame(crosslists)
crosslists = crosslists.rename(columns = {0: 'course_id', 1 : 'crosslist'})
sqldbcrosslists = crosslists.to_sql('crosslists', con = db, flavor = 'sqlite', index = False)
