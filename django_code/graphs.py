import courses
import pandas as pd
'''
get the necessary data given args from ui
this assumes that you can search by prof, dept, or course number
if you search by prof, you don't want info about a specific course
if you search by dept, you don't want info about a specific course or prof
'''

def graph_it(args_from_ui):
    if prof_fn in args_from_ui and prof_ln in args_from_ui and len(args_from_ui) == 2:
        prof_graph(args_from_ui)
    if dept in args_from_ui and course_num in args_from_ui and len(args_from_ui) == 2:
        course_graph(args_from_ui)
    else:
        course_prof_graph(args_from_ui)


def prof_graph(args_from_ui):
    '''
    If the user searches by professor only, this code will produce a graph comparing
    the time demands of every course the professor has taught to the department average
    time demands.
    ders = class in turkish, i ran out of names, sorry
    '''
    df = courses.find_courses(args_from_ui)
    title = "Comparison of the time demands made by " + args_from_ui['prof_fn'] + ' ' args_from_ui['prof_ln'] + "to the departmental average"
    course_df = df[df.course == ders].groupby(['course']).mean()







def course_graph(args_from_ui):
    '''
    If the user searches by course and department, this code will produce a graph that compares the time 
    demands made by each professor who taught the course compared to the department average 
    time demands. If the course is crosslisted, this may also include the average time demands of the other department(s).
    '''
    df = courses.find_courses(args_from_ui)

def course_prof_graph(args_from_ui):
    '''
    If the user searches by course and professor, this code will produce a graph that compares the time 
    demands made by this professor averaged over every time they taught the course, the time demands made by
    other professors who  have taught this course, departmental average time demands, and this professors average
    time demands.
    '''
    df = courses.find_courses(args_from_ui)




def time_comparison(lows, avgs, highs, graph_type, course_name, dept, prof):
    '''
    graph_type options: time comparison (time), prof score comparison (prof)
    lows, avgs, highs are tuples of those values for each group    
    you can search for course and professor, just professor, just course
    '''
    if graph_type == "course_and_prof" or if graph_type == "course":
        
    if graph_type == "prof":
        title = "Comparison of this professor's time demands to other related professors"
    n = len(lows)
    ind = np.arange(n)
    width = 0.35
    plt.figure(figsize = (10, 5))
    p1 = plt.bar(ind, lows, width, color='#d62728')
    p2 = plt.bar(ind, avgs, width,
             bottom=lows, color = '#f442cb')
    p3 = plt.bar(ind, avgs, width,
             bottom=avgs, color = '#63cbe8')
    plt.ylabel('Amount of time spent')
    plt.title(title)
    if graph_type == "course_and_prof":
        plt.xticks(ind, (course_name + , course_name + ' over time', dept, prof))
    if graph_type == "prof":
        plt.xticks(ind, (prof, prof + ' over time', dept))

    plt.legend((p1[0], p2[0], p3[0]), ('Low', 'Average', 'High'))
    plt.show()
    
