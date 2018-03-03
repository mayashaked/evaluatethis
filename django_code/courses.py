# code to create sql query to find courses that match the inputs

import sqlite3
import os
import pandas as pd
from wordcloud import WordCloud
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

# Use this filename for the database
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'reevaluations.db')


def get_wc(args_from_ui):
    db = sqlite3.connect(DATABASE_FILENAME)
    query = create_query(args_from_ui)
    evals_df = pd.read_sql_query(query, db)
    evals_df = evals_df.dropna(axis = 1, how = 'all')
    all_ids = list(evals_df['course_id'])
    if len(args_from_ui) == 2 and "dept" in args_from_ui:
        query = 'SELECT course_resp FROM text WHERE '
        for _id in all_ids:
            query += 'course_id = ' + str(_id) + ' OR ' 
        query = query[:-4] + ';'
    elif len(args_from_ui) == 2 and "dept" not in args_from_ui:
        query = 'SELECT inst_resp FROM text WHERE '
        for _id in all_ids:
            query += 'course_id = ' + str(_id) + ' OR '
        query = query[:-4] + ';'
    elif len(args_from_ui) == 4:
        query = 'SELECT course_resp, inst_resp FROM text WHERE '
        for _id in all_ids:
            query += 'course_id = ' + str(_id) + ' OR '
        query = query[:-4]

    df = pd.read_sql_query(query, db)
    evals = list(df['course_resp'])
    clean = ''
    for eval in evals:
        eval = eval.lower()
        eval = eval.strip('"@#$%^&*)(_+=][}{:;.,')
        clean += eval + ' '

    wordcloud = WordCloud(stopwords = stopwords.words("english"), width = 500, height = 100).generate(clean)

    return wordcloud


def find_courses(args_from_ui):
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
    if not args_from_ui:
        return pd.DataFrame()

    db = sqlite3.connect(DATABASE_FILENAME)
    query = create_query(args_from_ui)
    evals_df = pd.read_sql_query(query, db)
    evals_df = evals_df.dropna(axis = 1, how = 'all')

    return evals_df


def create_query(args_from_ui):
    '''
    Takes a dictionary containing search criteria and returns a
    search query

    Inputs:
        args_from_ui (dict): search criteria
        c (sqlite3 cursor object): cursor object for the database

    Outputs:
        (string): SQL search query
        arg_array (list of strings and ints): argument array
    '''
    if len(args_from_ui) == 2:
        if 'dept' in args_from_ui and 'course_num' in args_from_ui:
        # searching by course
            query_string = "SELECT evals.* FROM courses JOIN evals JOIN \
                crosslists ON courses.course_id = evals.course_id AND \
                courses.course_id = crosslists.course_id WHERE courses.dept = '"\
                + args_from_ui['dept'] + "' AND courses.course_number = '" + \
                args_from_ui['course_num'] + "';"
        elif 'prof_fn' in args_from_ui and 'prof_ln' in args_from_ui:
            query_string = "SELECT evals.* FROM courses JOIN profs JOIN evals \
                ON courses.course_id = profs.course_id AND courses.course_id =\
                evals.course_id WHERE profs.fn = '" + args_from_ui['prof_fn'] +\
                "' AND profs.ln = '" + args_from_ui['prof_ln'] + "';"
    elif len(args_from_ui) == 4: #searching by course and professor
         query_string = "SELECT evals.* FROM courses JOIN profs JOIN evals JOIN\
            crosslists ON courses.course_id = evals.course_id AND \
            courses.course_id = crosslists.course_id AND courses.course_id = \
            profs.course_id WHERE courses.dept = '" + args_from_ui['dept'] + \
            "' AND courses.course_number = '" + args_from_ui['course_num'] + \
            "' AND profs.fn = '" + args_from_ui['prof_fn'] + \
            "' AND profs.ln = '" + args_from_ui['prof_ln'] + "';"
    
    return query_string


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
