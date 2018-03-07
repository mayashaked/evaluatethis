import courses
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
'''
get the necessary data given args from ui
this assumes that you can search by prof, dept, or course number
if you search by prof, you don't want info about a specific course
if you search by dept, you don't want info about a specific course or prof
'''

def graph_it(args_from_ui):
    if "prof_fn" in args_from_ui and "prof_ln" in args_from_ui and len(args_from_ui) == 2:
        prof_graph(args_from_ui)
    if "dept" in args_from_ui and "course_num" in args_from_ui and len(args_from_ui) == 2:
        course_graph(args_from_ui)
    else:
        course_prof_graph(args_from_ui)


def get_small_df(dataframe, prof_or_course):
    current_year = 2018
    timespan = 5
    if prof_or_course == "prof":
        dataframe = dataframe.groupby(['course']).mean()
    if prof_or_course == "course":
        dataframe = dataframe.groupby(['fn', 'ln']).mean()
    while dataframe.shape[0] > 10:
        timespan -= 1
        dataframe = dataframe[dataframe.year > current_year - timespan]

    return dataframe, current_year - timespan

def time_lists(small_df, dept_df, dept):

    lows = small_df.low_time
    dept_low = dept_df.low_time.mean()
    lows = lows.append(pd.Series({dept:dept_low}))
    print(dept_low)

    avgs = small_df.avg_time
    dept_avg = dept_df.avg_time.mean()
    avgs = avgs.append(pd.Series({dept:dept_avg}))
    print(dept_avg)

    highs = small_df.high_time
    dept_high = dept_df.high_time.mean()
    highs = highs.append(pd.Series({dept:dept_high}))
    print(dept_high)

    return lows, avgs, highs


def prof_graph(args_from_ui):
    '''
    If the user searches by professor only, this code will produce a graph comparing
    the time demands of every course the professor has taught to the department average
    time demands.
    '''
    prof_df, dept_df, dept = courses.find_courses(args_from_ui)
    title = "Comparison of the time demands made by " + args_from_ui['prof_fn'] + ' ' + args_from_ui['prof_ln'] + " to the departmental average"
    small_df, year = get_small_df(prof_df, "prof")
    lows, avgs, highs = time_lists(small_df, dept_df, dept)
    n = lows.shape[0]
    ind = np.arange(n)
    width = 0.35
    plt.figure(figsize = (10, 7))
    p1 = plt.bar(ind, lows, width, color='#d62728')
    p2 = plt.bar(ind, avgs, width,
             bottom=lows, color = '#f442cb')
    p3 = plt.bar(ind, avgs, width,
             bottom=avgs, color = '#63cbe8')
    plt.ylabel('Amount of time spent')
    plt.title(title)
    xnames = list(prof_df[prof_df.year > year].course.unique())
    xnames.append(dept)
    plt.xticks(ind, xnames, rotation = 20, fontsize = 6, ha = 'right')
    plt.legend((p1[0], p2[0], p3[0]), ('Low', 'Average', 'High'))
    plt.tight_layout()
    plt.show()


def course_graph(args_from_ui):
    '''
    If the user searches by course and department, this code will produce a graph that compares the time 
    demands made by each professor who taught the course compared to the department average 
    time demands. If the course is crosslisted, this may also include the average time demands of the other department(s).
    '''
    course_df, dept_df = courses.find_courses(args_from_ui)
    title = "Time demands made by instructors of " + args_from_ui['dept'] + " " + args_from_ui['course_num'] + " w/ departmental average"
    dept = args_from_ui['dept']
    small_df, year = get_small_df(course_df, "course")
    lows, avgs, highs = time_lists(small_df, dept_df, dept)
    n = lows.shape[0]
    ind = np.arange(n)
    width = 0.35
    plt.figure(figsize = (10, 7))
    p1 = plt.bar(ind, lows, width, color='#d62728')
    p2 = plt.bar(ind, avgs, width,
             bottom=lows, color = '#f442cb')
    p3 = plt.bar(ind, avgs, width,
             bottom=avgs, color = '#63cbe8')
    plt.ylabel('Amount of time spent')
    plt.title(title)
    fns = list(course_df[course_df.year > year].fn.unique())
    lns = list(course_df[course_df.year > year].ln.unique())
    names = zip(fns, lns)
    xnames = []
    for name in names:
        xnames.append(name[0] + " " + name[1])
    xnames.append(dept)
    plt.xticks(ind, xnames, rotation = 20, fontsize = 6, ha = 'right')
    plt.legend((p1[0], p2[0], p3[0]), ('Low', 'Average', 'High'))
    plt.tight_layout()
    plt.show()



def course_prof_graph(args_from_ui):
    '''
    If the user searches by course and professor, this code will produce a graph that compares the time 
    demands made by this professor averaged over every time they taught the course, the time demands made by
    other professors who  have taught this course, departmental average time demands, and this professors average
    time demands.
    '''
    course_and_prof_df, dept_df, course_df, prof_df = courses.find_courses(args_from_ui)



