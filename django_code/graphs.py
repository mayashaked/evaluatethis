DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'reevaluations.db')

'''
get the necessary data given args from ui
this assumes that you can search by prof, dept, or course number
if you search by prof, you don't want info about a specific course
if you search by dept, you don't want info about a specific course or prof
'''
def get_data(args_from_ui, df):
    '''
    get the necessary data given args from ui
    this assumes that you can search by prof, dept, or course number
    if you search by prof, you don't want info about a specific course
    if you search by dept, you don't want info about a specific course or prof
    '''
    if prof in args_from_ui and len(args_from_ui) == 1:
        data = prof_query(args_from_ui['prof_name'])
    if dept in args_from_ui and len(args_from_ui) == 1:
        data = dept_query(args_from_ui["dept"])
    else:
        data = query(args_from_ui)        
    return data

def time_comparison(lows, avgs, highs, graph_type, course_name, dept, prof):
    '''
    graph_type options: time comparison (time), prof score comparison (prof)
    lows, avgs, highs are tuples of those values for each group    
    '''
    if graph_type == "time":
        title = 'Comparison of time spent on this course to other related courses'
    if graph_type == "prof":
        title = "Comparison of this professor's time demands to other related professors"
    n = len(lows)
    ind = np.arange(n)
    width = 0.35
    p1 = plt.bar(ind, lows, width, color='#d62728')
    p2 = plt.bar(ind, avgs, width,
             bottom=lows, color = '#f442cb')
    p3 = plt.bar(ind, avgs, width,
             bottom=avgs, color = '#63cbe8')
    plt.ylabel('Amount of time spent')
    plt.title(title)
    if graph_type == "time":
        plt.xticks(ind, (course_name, course_name + ' over time', dept, prof))
    if graph_type == "prof":
        plt.xticks(ind, (prof, prof + ' over time', dept))
    plt.legend((p1[0], p2[0], p3[0]), ('Low', 'Average', 'High'))
    plt.show()
    

def sql_to_inputs(database_filename, args_from_ui):
    db = sqlite3.connect(DATABASE_FILENAME)
    query = create_query(args_from_ui)
    evals_df = pd.read_sql_query(query, db)
    evals_df = evals_df.dropna(axis = 1, how = 'all')
    return evals_df

def create_query(args_from_ui):
    if prof_fn in args_from_ui and prof_ln in args_from_ui:
        proftup = (args_from_ui['prof_fn'], args_from_ui['prof_ln'])
        query = prof_query_gen(proftup)
    return query

def prof_query_gen(profname):
    '''
    profname entered as tuple of (firstname, lastname)
    '''
    query_string = "SELECT evals.low_time, evals.avg_time, evals.high_time, profs.fn, profs.ln, courses.dept \
    FROM evals JOIN profs ON evals.course_id = profs.course_id JOIN courses on evals.course_id = courses.course_id \
    WHERE profs.fn = " + profname[0] + "AND profs.ln = " + profname[1] + ";"
    
        