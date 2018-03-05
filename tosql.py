import pandas as pd
import sqlite3
import aggregate_numerical_data as agg_num
from nltk.corpus import stopwords
import dyadic_partitioning as dy

EVALS_PART_1 = 'evals_json_version_5_part1'
EVALS_PART_2 = 'evals_json_version_5_part2'
SQL_DB_PATH = 'reevaluations.db'
STOPWORDS = stopwords("english") + ['class', 'classes', 'professor', 'professors' 'course', 'courses', 'ta', 'tas']


def pre_process(sql_db_path, evals_part_1, evals_part_2)

    db = sqlite3.connect(sql_db_path)
    j1 = pd.read_json(evals_part_1, convert_dates = False)
    j2 = pd.read_json(evals_part_2, convert_dates = False)

    j = pd.concat([j1, j2])
    j = j.set_index('unique_id')

    #aggregate numerical scores re: tests, instructor, readings, assignments, as 
    #well as sentiment analysis scores

    j = agg_num.add_score_cols(j)
    j = dy.go(j, level = 10, lambda_ = 3)

    j['year'] = j['year'].fillna(-1).astype(int)
    j['section'] = j['section'].fillna(-1).astype(int)
    j['course_number'] = j['course_number'].fillna(-1).astype(int)
    j['num_responses'] = j['num_responses'].fillna(-1).astype(int)
    j['low_time'] = j['low_time'].fillna(-1).astype(float)
    j['avg_time'] = j['avg_time'].fillna(-1).astype(float)
    j['high_time'] = j['high_time'].fillna(-1).astype(float)


    j = j.where(j != -1, None)

    return db, j



def gen_courses(j, db):

    courses = j[['course', 'course_number', 'dept', 'section', 'term', 'year']]

    sqldbcourses = courses.to_sql('courses', con = db, flavor = 'sqlite', index = True, index_label = 'course_id')

    pass

def gen_profs(j, db):


    profs = []
    for ind, row in j.iterrows():
        if type(row['instructors']) == list:
            for prof in row['instructors']:
                fullname = prof.split(', ')
                profs.append([ind, fullname[0], fullname[-1]])
        else:
            profs.append([ind, None, None])

    profs = pd.DataFrame(profs)
    profs = profs.rename(columns = {0 : 'course_id', 1: "ln", 2 : "fn"})
    sqldbprofs = profs.to_sql('profs', con = db, flavor = 'sqlite', index = False)

    pass

def gen_crosslists(j, db):

    crosslists = []
    for ind, row in j.iterrows():
        if type(row['identical_courses']) == str:
            x = row['identical_courses'].split(', ')
            for course in x:
                crosslists.append([ind, course])
        else:
            crosslists.append([ind, None])
                
    crosslists = pd.DataFrame(crosslists)
    crosslists = crosslists.rename(columns = {0 : 'course_id', 1 : 'crosslist'})
    sqldbcrosslists = crosslists.to_sql('crosslists', con = db, flavor = 'sqlite', index = False)

    pass

def gen_evals(j, db):

    evals = []
    for ind, row in j.iterrows():
        eval = [ind, None, None, None, None, 0, None, None, None, None, None, None, None, None, None, None, None, None]
        eval[1] = row['instructor_score']
        eval[2] = row['assignments_score']
        eval[3] = row['overall_score']
        eval[4] = row['tests_score']
        eval[5] = row['num_responses']
        eval[6] = row['low_time']
        eval[7] = row['avg_time']
       eval[8] = row['high_time']
        if type(row['recommend']) == list:
            eval[9] = int(row['recommend'][0])
            eval[10] = int(row['recommend'][1])
        eval[11] = row['inst_sentiment']
        eval[12] = row['course_sentiment']
        eval[13] = row['readings_score_col']
        if type(row['good_instructor']) == list:
            eval[14] = int(row['good_instructor'][0])
            eval[15] = int(row['good_instructor'][1])
        eval[16] = row['would_recommend_inst']
        eval[17] = row['would_recommend']


        evals.append(eval)

    evals = pd.DataFrame(evals)

    evals = evals.rename(columns = {0 : 'course_id', 1 : 'prof_score', 2 : 'ass_score', \
        3 : 'over_score' , 4 : 'test_score', 5 : 'num_responses', \
        6 : 'low_time', 7 : 'avg_time', 8 : 'high_time', 9 : 'num_recommend', \
        10 : 'num_dont_recommend', 11 : 'inst_sentiment', 12 : 'course_sentiment',
        13 : 'read_score', 14 : 'good_inst', 15 : 'bad_inst'})

    sqldbevals = evals.to_sql('evals', con = db, flavor = 'sqlite', index = False)

    pass

def gen_text(j, db):
    j = j[['course_responses', 'instructor_responses']]

    all_responses = []
    for ind, row in j.iterrows():
        resps = [ind, None, None]
        if type(row['course_responses']) == list and len(row['course_responses']) > 0:
            course_resps = ''
            for course_resp in row['course_responses']:
                course_resps += course_resp + ' '
            resps[1] = course_resps
        if type(row['instructor_responses']) == list and len(row['instructor_responses']) > 0:
            inst_resps = ''
            for inst_resp in row['instructor_responses']:
                inst_resps += inst_resp + ' '
            resps[2] = inst_resps
        allresponses.append(resps)

    alltext = []

    #pre-clean all text responses so we can quickly make a wordcloud later
    for [ind, courseresp, instresp] in all_responses:
        text = [ind, None, None]
        if coureresp != None:
            resp = courseresp.lower()
            resp = resp.strip('`~!@#$%^&*)(_+=][}{":;><,.?')
            resplist = resp.split()
            resplist = [x for x in resplist if x not in STOPWORDS]
            resp = (' ').join(resplist)
            text[1] = resp
        if instresp != None:
            resp = instresp.lower()
            resp = resp.strip('`~!@#$%^&*)(_+=][}{":;><,.?')
            resplist = resp.split()
            resplist = [x for x in resplist if x not in STOPWORDS]
            resp = (' ').join(resplist)
            text[2] = resp
        alltext.append(text)



    alltext = pd.DataFrame(text)

    alltext = alltext.rename(columns = {0 : 'course_id', 1 : 'course_resp', 2 : 'inst_resp'})

    sqldbtext = alltext.to_sql('text', con = db, flavor = 'sqlite', index = False)

    pass


if __name__ == "__main__":
    db, j = pre_process(SQL_DB_PATH, EVALS_PART_1, EVALS_PART_2)
    gen_courses(j, db)
    gen_profs(j, db)
    gen_crosslists(j, db)
    gen_evals(j, db)
    gen_text(j, db)
