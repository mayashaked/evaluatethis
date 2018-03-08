#-------------------------------------------------------------------------------
# Name:        Courses
# Purpose:     Queries the sql database and build Pandas DataFrames to provide
#              all information needed on webpage.
#
# Author:      Alex Maiorella, Lily Li, Maya Shaked, Sam Hoffman
#
# Created:     03/04/2018
#-------------------------------------------------------------------------------
import sqlite3
import os
import pandas as pd
import csv
from statistics import mode

# Use this filename for the database
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'reevaluations.db')

def find_courses(args):
    '''
    Takes a dictionary containing search criteria and returns courses
    that match the criteria.  The dictionary will contain some of the
    following fields:

      - dept is a string
      - course_num is a string
      - prof_fn is a string
      - prof_ln is a string
      - rank is one of {'avg_time', 'prof_score'}

    Returns pandas dataframes containing information necesssary for graphs/data
    visualizations
    '''
    if not args:
        return [pd.DataFrame()]

    db = sqlite3.connect(DATABASE_FILENAME)

    if len(args) == 1:
        return [format_rank(pd.read_sql_query(rank_depts().format(args['rank']), db))]


    if len(args) == 2:

        if 'dept' in args and 'course_num' in args:
            dept = dept_query()
            course = course_num_query()
            dept_df = pd.read_sql_query(dept.format(args['dept'], args['dept']), db)
            course_df = pd.read_sql_query(course.format(args['dept'], args['dept'], args['course_num']), db)
            return course_df, dept_df

        elif 'dept' in args and 'course_name' in args:
            dept = dept_query()
            course = course_name_query()
            dept_df = pd.read_sql_query(dept.format(args['dept'], args['dept']), db)
            course_df = pd.read_sql_query(course.format(args['dept'], args['dept'], args['course_name']), db)
            return course_df, dept_df

        elif 'prof_fn' in args and 'prof_ln' in args:
            prof = prof_query()
            dept = dept_query()
            primary_dept = get_profs_primary_dept(args, db)
            dept_df = pd.read_sql_query(dept.format(primary_dept, primary_dept), db)
            prof_df = pd.read_sql_query(prof.format(args['prof_fn'], args['prof_ln']), db)
            return prof_df, dept_df, primary_dept

    elif len(args) == 4:

        dept = dept_query()
        prof = prof_query()
        if 'course_num' in args:
          course = course_num_query()
          course_num_and_prof = course_num_and_prof_query()
          course_df = pd.read_sql_query(course.format(args['dept'], args['dept'], args['course_num']), db)
          course_and_prof_df = pd.read_sql_query(course_num_and_prof.format(args['dept'], args['dept'], args['course_num'], args['prof_fn'], args['prof_ln']), db)
        elif 'course_name' in args:
          course = course_name_query()
          course_name_and_prof = course_name_and_prof_query()
          course_df = pd.read_sql_query(course.format(args['dept'], args['dept'], args['course_name']), db)
          course_and_prof_df = pd.read_sql_query(course_name_and_prof.format(args['dept'], args['dept'], args['course_name'], args['prof_fn'], args['prof_ln']), db)
        dept_df = pd.read_sql_query(dept.format(args['dept'], args['dept']), db)
        prof_df = pd.read_sql_query(prof.format(args['prof_fn'], args['prof_ln']), db)
        return course_and_prof_df, dept_df, course_df, prof_df


def course_num_and_prof_query():
    '''
    Query for eval data from specified course & professor
    '''
    course_num_and_prof = "SELECT evals.*, course, year, fn, ln \
                       FROM courses JOIN profs JOIN evals JOIN crosslists \
                       ON courses.course_id = evals.course_id \
                       AND courses.course_id = crosslists.course_id \
                       AND courses.course_id = profs.course_id \
                       WHERE (courses.dept = '{}' or crosslists.crosslist = '{}') \
                       AND courses.course_number = '{}' \
                       AND profs.fn = '{}' \
                       AND profs.ln = '{}';"

    return course_num_and_prof


def course_name_and_prof_query():
    '''
    Query for eval data from specified course & professor
    '''
    course_name_and_prof = "SELECT evals.*, course, year, fn, ln \
                       FROM courses JOIN profs JOIN evals JOIN crosslists \
                       ON courses.course_id = evals.course_id \
                       AND courses.course_id = crosslists.course_id \
                       AND courses.course_id = profs.course_id \
                       WHERE (courses.dept = '{}' or crosslists.crosslist = '{}') \
                       AND courses.course = '{}' \
                       AND profs.fn = '{}' \
                       AND profs.ln = '{}';"

    return course_name_and_prof


def course_num_query():
    '''
    Query for eval data from specified course number
    '''
    course = "SELECT evals.*, course, year, fn, ln \
              FROM courses JOIN profs JOIN evals JOIN crosslists \
              ON courses.course_id = evals.course_id \
              AND courses.course_id = crosslists.course_id \
              AND courses.course_id = profs.course_id \
              WHERE (courses.dept = '{}' or crosslists.crosslist = '{}') \
              AND courses.course_number = '{}';"

    return course


def course_name_query():
    '''
    Query for eval data from specified course
    '''
    course = "SELECT evals.*, course, year, fn, ln \
              FROM courses JOIN profs JOIN evals JOIN crosslists \
              ON courses.course_id = evals.course_id \
              AND courses.course_id = crosslists.course_id \
              AND courses.course_id = profs.course_id \
              WHERE (courses.dept = '{}' or crosslists.crosslist = '{}') \
              AND courses.course = '{}';"

    return course


def prof_query():
    '''
    Query for eval data from specified professor
    '''
    prof = "SELECT evals.*, course, year, fn, ln \
            FROM courses JOIN profs JOIN evals \
            ON courses.course_id = evals.course_id \
            AND courses.course_id = profs.course_id \
            WHERE profs.fn = '{}' \
            AND profs.ln = '{}';"

    return prof


def dept_query():
    '''
    Query for eval data from specified department
    '''
    dept =   "SELECT evals.*, course, year, fn, ln \
              FROM courses JOIN profs JOIN evals JOIN crosslists \
              ON courses.course_id = evals.course_id \
              AND courses.course_id = crosslists.course_id \
              AND courses.course_id = profs.course_id \
              WHERE (courses.dept = '{}' or crosslists.crosslist = '{}');"

    return dept


def rank_depts():
    '''
    Query to rank departments by time or professor quality
    '''
    rank_dep =  "SELECT dept AS 'Department Code', \
                ROUND(AVG(avg_time), 2) AS 'Average Time', \
                ROUND(AVG(prof_score), 2) AS 'Average Professor Score' \
                FROM courses JOIN evals \
                ON courses.course_id = evals.course_id \
                GROUP BY dept HAVING AVG(avg_time) > .1 \
                AND COUNT(*) > 10 ORDER BY AVG({}) DESC;"

    return rank_dep


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
    '''
    Query database to find which dept a professor usually teaches under.
    '''
    cursor = db.cursor()
    depts = cursor.execute('SELECT dept FROM courses JOIN profs ON \
        profs.course_id = courses.course_id WHERE profs.fn = ? \
        and profs.ln = ?', [args['prof_fn'], args['prof_ln']])

    try:
        return mode([a[0] for a in depts])
        return depts[0]
    except:
        return ''

def format_rank(df):
    '''
    Change formating to display full dept name
    '''
    depts = os.path.join(os.path.dirname(__file__), 'res', 'depts.csv')
    dept_dict = {}
    with open(depts, encoding = 'iso-8859-1') as f:
        reader = csv.reader(f)
        for l in reader:
            if l:
                dept_dict[l[0]] = l[1]

    full_dept = pd.Series([dept_dict[d] for d in df.loc[:,'Department Code']], name = 'Department Name')

    new_df = pd.concat([full_dept, df], axis = 1)
    return new_df.loc[:,['Department Code', 'Department Name', 'Average Time', 'Average Professor Score']]
