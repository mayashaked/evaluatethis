# code to create sql query to find courses that match the inputs
#make sure to actually use crosslists in sql query
import sqlite3
import os
import pandas as pd
from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from statistics import mode

# Use this filename for the database
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'reevaluations.db')



def get_wc(args_from_ui):

    if not args_from_ui:
        return pd.DataFrame()

    db = sqlite3.connect(DATABASE_FILENAME)
    if "dept" in args_from_ui and len(args_from_ui) == 2:
        query = 'SELECT text.course_id, text.course_resp FROM text JOIN courses ON \
        text.course_id = courses.course_id WHERE courses.dept = "' + args_from_ui['dept'] +\
        '" AND courses.course_number = "' + args_from_ui['course_num'] + '";'
        evals_df = pd.read_sql_query(query, db)
        evals = list(evals_df['course_resp'])
    elif len(args_from_ui) == 4:
        query = 'SELECT text.course_id, text.course_resp, text.inst_resp FROM text JOIN \
        courses JOIN profs ON text.course_id = courses.course_id AND text.course_id = \
        profs.course_id WHERE courses.dept = "' + args_from_ui['dept'] + '" AND \
        courses.course_number = "' + args_from_ui['course_num'] + '" AND profs.fn = \
        "' + args_from_ui[prof_fn] + '" AND profs.ln = "' + args_from_ui[prof_ln] + '";'
        evals_df = pd.read_sql_query(query, db)
        evals = list(evals_df['course_resp']) + list(evals_df['inst_resp'])
    else:
        query = 'SELECT text.course_id, text.inst_resp FROM text JOIN profs ON \
        text.course_id = profs.course_id WHERE profs.fn = ' + args_from_ui[prof_fn]\
        + ' AND profs.ln = ' + args_from_ui[prof_ln] + ';'
        evals_df = pd.read_sql_query(query, db)
        evals = list(evals_df)
    
    clean = ' '.join([x for x in evals if x != None])

    wordcloud = WordCloud(width = 600, height = 300).generate(clean)

    return wordcloud




def find_courses(args):

    '''
    Takes a dictionary containing search criteria and returns courses
    that match the criteria.  The dictionary will contain some of the
    following fields:

      - dept is a string
      - course_num is a string
      - prof_fn is a string
      - prof_ln is a string

    Returns a pair: list of attribute names in order and a list
    containing query results.
    '''
    if not args:
        return pd.DataFrame()

    db = sqlite3.connect(DATABASE_FILENAME)

    if len(args) == 2:

        if 'dept' in args and 'course_num' in args:
            dept = dept_query()
            course = course_query()
            dept_df = pd.read_sql_query(dept.format(args['dept'], args['dept']), db)
            course_df = pd.read_sql_query(course.format(args['dept'], args['dept'], args['course_num']), db)
            return dept_df, course_df

        elif 'prof_fn' in args and 'prof_ln' in args:
            prof = prof_query()
            dept = dept_query()
            print('here')
            primary_dept = get_profs_primary_dept(args, db)
            print(primary_dept)
            dept_df = pd.read_sql_query(dept.format(primary_dept, primary_dept), db)
            prof_df = pd.read_sql_query(prof.format(args['prof_fn'], args['prof_ln']), db)
            return dept_df, prof_df

    elif len(args) == 4:
        dept = dept_query()
        prof = prof_query()
        course = course_query()
        course_and_prof = course_and_prof_query()
        dept_df = pd.read_sql_query(dept.format(args['dept'], args['dept']), db)
        prof_df = pd.read_sql_query(prof.format(args['prof_fn'], args['prof_ln']), db)
        course_df = pd.read_sql_query(course.format(args['dept'], args['dept'], args['course_num']), db)
        course_and_prof_df = pd.read_sql_query(course_and_prof.format(args['dept'], args['dept'], args['course_num'], args['prof_fn'], args['prof_ln']), db)
        return dept_df, course_df, prof_df, course_and_prof_df


def course_and_prof_query():

    course_and_prof = "SELECT evals.*, course, fn, ln \
                       FROM courses JOIN profs JOIN evals JOIN crosslists \
                       ON courses.course_id = evals.course_id \
                       AND courses.course_id = crosslists.course_id \
                       AND courses.course_id = profs.course_id \
                       WHERE (courses.dept = '{}' or crosslists.crosslist = '{}') \
                       AND courses.course_number = '{}' \
                       AND profs.fn = '{}' \
                       AND profs.ln = '{}';"

    return course_and_prof

def course_query():

    course = "SELECT evals.*, course, fn, ln \
              FROM courses JOIN profs JOIN evals JOIN crosslists \
              ON courses.course_id = evals.course_id \
              AND courses.course_id = crosslists.course_id \
              AND courses.course_id = profs.course_id \
              WHERE (courses.dept = '{}' or crosslists.crosslist = '{}') \
              AND courses.course_number = '{}';"

    return course

def prof_query():

    prof = "SELECT evals.*, course, fn, ln \
            FROM courses JOIN profs JOIN evals JOIN crosslists \
            ON courses.course_id = evals.course_id \
            AND courses.course_id = crosslists.course_id \
            AND courses.course_id = profs.course_id \
            WHERE profs.fn = '{}' \
            AND profs.ln = '{}';"

    return prof

def dept_query():

    dept =   "SELECT evals.*, course, fn, ln \
              FROM courses JOIN profs JOIN evals JOIN crosslists \
              ON courses.course_id = evals.course_id \
              AND courses.course_id = crosslists.course_id \
              AND courses.course_id = profs.course_id \
              WHERE (courses.dept = '{}' or crosslists.crosslist = '{}');"

    return dept

def get_header(cursor):
    '''
    Given a cursor object, returns the appropriate header (column names)
    '''
    desc = cursor.description
    header = ()

    for i in desc:
        header = header + (clean_header(i[0]),)

    return list(header)


def clean_header(s):
    '''
    Removes table name from header
    '''
    for i, _ in enumerate(s):
        if s[i] == ".":
            s = s[i + 1:]
            break

    return s

def get_profs_primary_dept(args, db):

    cursor = db.cursor()
    depts = cursor.execute('SELECT dept FROM courses JOIN profs ON \
        profs.course_id = courses.course_id WHERE profs.fn = ? \
        and profs.ln = ?', [args['prof_fn'], args['prof_ln']])
    
    try:
        return mode([a[0] for a in depts])
        return depts[0]
    except:
        return ''


