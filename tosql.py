import pandas as pd
import sqlite3
from sqlalchemy import create_engine

db = sqlite3.connect('test.db')
j = pd.read_json('evals_json_version_1')

courses = j[['course', 'course_number', 'dept', 'num_responses']]
sqldbcourses = courses.to_sql('courses', con = db, flavor = 'sqlite', index = True, index_label = 'course_id')

profs = []
for ind, row in j.iterrows():
	for prof in row['instructor(s)']:
		profs.append([ind, prof])

profs = pd.DataFrame(profs)
profs = profs.rename(columns = {0 : 'course_id', 1: "prof"})
sqldbprofs = profs.to_sql('profs', con = db, flavor = 'sqlite', index = False)
