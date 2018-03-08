#-------------------------------------------------------------------------------
# Name:        gen_wordcloud
#
# Purpose:     Generates a wordcloud from written responses to questions about 
#			   the professor, the course, or both, depending on what was 
#			   searched for
#
# Author:      Maya Shaked
#
# Created:     03/04/2018
#-------------------------------------------------------------------------------
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
    '''
    Takes a dictionary containing search criteria and returns a 
    wordcloud based on the text responses for the matching
    criteria

      - dept is a string
      - course_num is a string
      - prof_fn is a string
      - prof_ln is a string

    Doesn't return anything,  but rather saves the Wordcloud object 
    into the 'static' folder
    '''
    if not args_from_ui:
        return

    db = sqlite3.connect(DATABASE_FILENAME)
    if 'dept' in args_from_ui and 'course_num' in args_from_ui and len(args_from_ui) == 2:
        query = 'SELECT text.course_id, text.course_resp FROM text JOIN courses ON \
        text.course_id = courses.course_id WHERE courses.dept = "' + args_from_ui['dept'] +\
        '" AND courses.course_number = "' + args_from_ui['course_num'] + '";'
        evals_df = pd.read_sql_query(query, db)
        evals = list(evals_df['course_resp'])
    elif 'dept' in args_from_ui and 'course_name' in args_from_ui and len(args_from_ui) == 2:
        query = 'SELECT text.course_id, text.course_resp FROM text JOIN courses ON \
        text.course_id = courses.course_id WHERE courses.dept = "' + args_from_ui['dept'] +\
        '" AND courses.course = "' + args_from_ui['course_name'] + '";'
        evals_df = pd.read_sql_query(query, db)
        evals = list(evals_df['course_resp'])
    elif len(args_from_ui) == 4:
        if 'course_num' in args_from_ui:
            query = "SELECT text.course_id, course_resp, inst_resp FROM text JOIN \
            courses JOIN profs ON text.course_id = courses.course_id AND text.course_id = \
            profs.course_id WHERE courses.dept = '{}' AND \
            courses.course_number = '{}' AND profs.fn = \
            '{}' AND profs.ln = '{}';".format(args_from_ui['dept'], \
            args_from_ui['course_num'], args_from_ui['prof_fn'], args_from_ui['prof_ln'])
        elif 'course_name' in args_from_ui:
            query = "SELECT text.course_id, course_resp, inst_resp FROM text JOIN \
            courses JOIN profs ON text.course_id = courses.course_id AND text.course_id = \
            profs.course_id WHERE courses.dept = '{}' AND \
            courses.course = '{}' AND profs.fn = \
            '{}' AND profs.ln = '{}';".format(args_from_ui['dept'], \
            args_from_ui['course_name'], args_from_ui['prof_fn'], args_from_ui['prof_ln'])
        evals_df = pd.read_sql_query(query, db)
        evals = list(evals_df['course_resp']) + list(evals_df['inst_resp'])
    else:
        query = "SELECT text.course_id, text.inst_resp FROM text JOIN profs ON \
        text.course_id = profs.course_id WHERE profs.fn = '{}' \
        AND profs.ln = '{}';".format(args_from_ui['prof_fn'], args_from_ui['prof_ln'])
        evals_df = pd.read_sql_query(query, db)
        evals = list(evals_df['inst_resp'])

    clean = ' '.join([x for x in evals if x != None])

    wc = WordCloud(width = 600, height = 300).generate(clean)

    plt.figure(figsize = (10, 5))
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig('./static/images/wordcloud.png')
    plt.close()
    
    pass
