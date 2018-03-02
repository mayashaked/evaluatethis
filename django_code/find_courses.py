# code to create sql query to find courses that match the inputs
# can use pa2 code

# need to think more about website design- what search fields will there be?
# course and professor- dropdown or box to type?
# do we want to return multiple results with links like the current eval website or gather the info for just one course?
# can we do course comparisons?

import sqlite3
import os
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'reevaluations.db')

ALL_EVAL_COLS = "evals.course_id,\
evals.prof_score, \
evals.ass_score, \
evals.over_score, \
evals.test_score, \
evals.num_responses, \
evals.low_time, \
evals.avg_time, \
evals.high_time, \
evals.num_recommend, \
num_dont_recommend, \
evals.inst_sentiment, \
evals.course_sentiment, \
evals.read_score, \
evals.good_inst, \
evals.bad_inst"

def testing_function():
    db = sqlite3.connect(DATABASE_FILENAME)
    return db

def query_string_gen(args):
    query_string = "SELECT " + ALL_EVAL_COLS
    if "dept" in args and len(args) == 1:
        query_string += " FROM courses JOIN evals JOIN crosslists ON courses.course_id = evals.course_id AND\
        courses.course_id = crosslists.course_id WHERE courses.dept = ? OR crosslists.crosslist = ?" 

    if "prof_ln" in args and len(args) == 1:
        query_string += query_string += " FROM courses JOIN profs JOIN evals ON courses.course_id = profs.course_id \
        AND courses.course_id = evals.course_id WHERE profs.ln = ?"

    if "prof_fn" in args and len(args) == 1:
        query_string += query_string += " FROM courses JOIN profs JOIN evals ON courses.course_id = profs.course_id \
        AND courses.course_id = evals.course_id WHERE profs.fn = ?"

    if "course_name" in args and len(args) == 1:
        query_string += query_string += " FROM courses JOIN profs JOIN evals ON courses.course_id = profs.course_id \
        AND courses.course_id = evals.course_id WHERE courses.course_name LIKE ?"

    


    return query_string

#def find_by_course_name:


