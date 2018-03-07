import sqlite3
import os
import pandas as pd
from wordcloud import WordCloud
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
        query = "SELECT text.course_id, text.course_resp FROM text JOIN courses ON \
        text.course_id = courses.course_id WHERE courses.dept = " + "'"\
         + args_from_ui['dept'] + "'" + ' AND courses.course_number = "' + args_from_ui['course_num']\
          + '";'
        evals_df = pd.read_sql_query(query, db)
        evals = list(evals_df['course_resp'])
    elif len(args_from_ui) == 4:
        query = 'SELECT text.course_id, text.course_resp, text.inst_resp FROM text JOIN \
        courses JOIN profs ON text.course_id = courses.course_id AND text.course_id = \
        profs.course_id WHERE courses.dept = ' + "'" + args_from_ui['dept'] + "'" + ' AND \
        courses.course_number = ' + "'" + args_from_ui['course_num'] + "'" + ' AND profs.fn = \
        ' + "'" + args_from_ui['prof_fn'] + "'" + ' AND profs.ln = ' + "'" + args_from_ui['prof_ln'] + "';"

        evals_df = pd.read_sql_query(query, db)
        evals = list(evals_df['course_resp']) + list(evals_df['inst_resp'])
    else:
        query = 'SELECT text.course_id, text.inst_resp FROM text JOIN profs ON \
        text.course_id = profs.course_id WHERE profs.fn = ' + "'" + args_from_ui['prof_fn']\
        + "'" + ' AND profs.ln = ' + "'" + args_from_ui['prof_ln'] + "';"
        evals_df = pd.read_sql_query(query, db)
        evals = list(evals_df)

    clean = ' '.join([x for x in evals if x != None])

    wordcloud = WordCloud(width = 600, height = 300).generate(clean)

    return wordcloud
