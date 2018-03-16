#-------------------------------------------------------------------------------
# Name:        Graphs
# Purpose:     Builds graphs that display the time demands of the course, professor, or
#              professor that the user searched for. 
#
# Author:      Alex Maiorella, Lily Li, Maya Shaked, Sam Hoffman
#
# Created:     03/04/2018
#-------------------------------------------------------------------------------
import courses
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
'''
get the necessary data given args from ui
this assumes that you can search by prof, dept, or course number
if you search by prof, you don't want info about a specific course
if you search by dept, you don't want info about a specific course or prof
'''

def graph_it(args_from_ui):
    '''
    Given arguments from the user, calls the appropriate graphing function to create a time
    comparison graph. 
    '''
    if len(args_from_ui) == 2:
        if "prof_fn" in args_from_ui and "prof_ln" in args_from_ui:
            prof_graph(args_from_ui)
        elif "dept" in args_from_ui:
            course_graph(args_from_ui)
    else:
        course_prof_graph(args_from_ui)


def get_small_df(dataframe, prof_or_course):
    '''
    Drops successive years until the number of bars in the graph will be no more than 10. 
    '''
    current_year = 2018
    timespan = 5
    if prof_or_course == "prof":
        while dataframe.course.unique().shape[0] > 10:
            timespan -= 1
            if timespan == 1:
                break
            dataframe = dataframe[dataframe.year >= current_year - timespan]
        dataframe = dataframe.groupby(['course']).mean()

    if prof_or_course == "course":
        dataframe['prof_name'] = dataframe['fn'].astype('str') + ' ' + dataframe['ln']
        while dataframe.prof_name.unique().shape[0] > 10:
            timespan -= 1
            if timespan == 1:
                break
            dataframe = dataframe[dataframe.year >= current_year - timespan]
        dataframe = dataframe.groupby(['prof_name']).mean()

    return dataframe, current_year - timespan

def time_lists(small_df, dept_df, dept):
    '''
    Creates lists of low, average, and high time demands for courses and departments. 
    '''

    lows = small_df.low_time
    dept_low = dept_df.low_time.mean()
    lows = lows.append(pd.Series({dept:dept_low}))

    avgs = small_df.avg_time
    dept_avg = dept_df.avg_time.mean()
    avgs = avgs.append(pd.Series({dept:dept_avg}))

    highs = small_df.high_time
    dept_high = dept_df.high_time.mean()
    highs = highs.append(pd.Series({dept:dept_high}))

    return lows, avgs, highs

def time_graph(lows, avgs, highs, title):
    '''
    Given lists of low, average, and high amounts of time spent on classes, 
    creates graphs that compare the times to each other and to the department
    average. 
    '''
    n = lows.shape[0]
    ind = np.arange(n)
    width = 0.2
    plt.figure(figsize = (20, 7))
    p1 = plt.bar(ind, lows, width, color='#d62728')
    p2 = plt.bar(ind, avgs, width,
             bottom=lows, color = '#f442cb')
    p3 = plt.bar(ind, avgs, width,
             bottom=avgs, color = '#63cbe8')
    plt.ylabel('Amount of time spent', fontsize = 15)
    plt.title(title)
    xnames = list(lows.axes[0])
    plt.xticks(ind, xnames, rotation = 10, fontsize = 10, ha = 'left')
    plt.legend((p1[0], p2[0], p3[0]), ('Low', 'Average', 'High'))
    plt.tight_layout()
    return plt
    plt.savefig('./static/images/graph.png')


def prof_graph(args_from_ui):
    '''
    If the user searches by professor only, this code will produce a graph comparing
    the time demands of every course the professor has taught to the department average
    time demands.
    '''
    prof_df, dept_df, dept = courses.find_courses(args_from_ui)
    title = "Comparison of the time demands made by " + args_from_ui['prof_fn'] + ' ' + args_from_ui['prof_ln'] + " to the departmental average"
    small_df, year = get_small_df(prof_df, "prof")
    if 'high_time' in small_df:
        small_df = small_df.sort_values(by = 'high_time', axis = 0, ascending = False)
    lows, avgs, highs = time_lists(small_df, dept_df, dept)
    graph = time_graph(lows, avgs, highs, title)
    plt.savefig('./static/images/graph.png')


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
    if 'high_time' in small_df:
        small_df = small_df.sort_values(by = 'high_time', axis = 0, ascending = False)
    lows, avgs, highs = time_lists(small_df, dept_df, dept)
    graph = time_graph(lows, avgs, highs, title)
    plt.savefig('./static/images/graph.png')


def course_prof_graph(args_from_ui):
    '''
    If the user searches by course and professor, this code will produce a graph that compares the time 
    demands made by this professor averaged over every time they taught the course, the time demands made by
    other professors who  have taught this course, departmental average time demands, and this professor's average
    time demands.
    '''
    course_and_prof_df, dept_df, course_df, prof_df = courses.find_courses(args_from_ui)
    dept = args_from_ui['dept']
    course = dept + " " + args_from_ui['course_num']
    prof = args_from_ui['prof_fn'] + " " + args_from_ui['prof_ln']
    course_and_prof = prof + " and " + course
    title = "Time demands for " + course + ' taught by ' + prof + ' with related time demands'
    lows = pd.Series({course_and_prof:course_and_prof_df.low_time.mean()})
    avgs = pd.Series({course_and_prof:course_and_prof_df.avg_time.mean()})
    highs = pd.Series({course_and_prof:course_and_prof_df.high_time.mean()})
    
    lows = lows.append(pd.Series({dept:dept_df.low_time.mean()}))
    avgs = avgs.append(pd.Series({dept:dept_df.avg_time.mean()}))
    highs = highs.append(pd.Series({dept:dept_df.high_time.mean()}))

    lows = lows.append(pd.Series({course:course_df.low_time.mean()}))
    avgs = avgs.append(pd.Series({course:course_df.avg_time.mean()}))
    highs = highs.append(pd.Series({course:course_df.high_time.mean()}))


    lows = lows.append(pd.Series({prof:prof_df.low_time.mean()}))
    avgs = avgs.append(pd.Series({prof:prof_df.avg_time.mean()}))
    highs = highs.append(pd.Series({prof:prof_df.high_time.mean()}))

    graph = time_graph(lows, avgs, highs, title)
    plt.savefig('./static/images/graph.png')

