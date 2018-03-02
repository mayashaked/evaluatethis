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

def testing_function(args):
    db = sqlite3.connect(DATABASE_FILENAME)
    c = db.cursor()
    query_string = query_string_gen(args)
    r = db.execute(query_string)
    return r.fetchall()    


def table_join_string(args, query_string):
    query_string += " FROM evals JOIN courses on evals.course_id = courses.course_id"

    if "dept" in args:
        query_string += " JOIN crosslists on courses.course_id = crosslists.course_id"
    if "prof_fn" in args or "prof_ln" in args:
        query_string += " JOIN profs on evals.course_id = profs.course_id"

    return query_string



def query_string_gen(args):
    query_string = "SELECT " + ALL_EVAL_COLS
    query_string += ", courses.dept, courses.course, courses.course_number, profs.fn, profs.ln"
    query_string = table_join_string(args, query_string)
    query_string += " WHERE"

    #all the possible arguments
    query_list = []
    if "prof_ln" in args:
        query_list.append(" profs.ln = " + "'" + args["prof_ln"] + "'")
    if "prof_fn" in args:
        query_list.append(" profs.fn = " + "'" + args["prof_fn"] + "'")
    if "course_name" in args:
        query_list.append(" courses.course_name = " + "'" + args["course_name"] + "'")
    if "dept" in args:
        query_list.append(" (courses.dept = " + "'" + args["dept"] + "'" + " OR crosslists.crosslist = " + "'" + args["dept"] + "'" ")")

    for arg in query_list:
        query_string += arg
        query_string += " AND"

    query_string = query_string[:-4]
    query_string += ";"

    return query_string



