# code to create sql query to find courses that match the inputs
# can use pa2 code

# need to think more about website design- what search fields will there be?
# course and professor- dropdown or box to type?
# do we want to return multiple results with links like the current eval website or gather the info for just one course?
# can we do course comparisons?

import sqlite3
import os

DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'evaluations/reevaluations.db')


db = sqlite3.connect(DATABASE_FILENAME)

def find_by_dept():
	query_string = "SELECT courses.dept, courses.course, evals.over_score, evals.prof_score, courses.year \
	FROM courses JOIN profs JOIN evals ON profs.course_id = courses.course_id AND \
	profs.course_id = evals.course_id WHERE courses.year < 2004;"
	return query_string

def find_by_course_name:
	

