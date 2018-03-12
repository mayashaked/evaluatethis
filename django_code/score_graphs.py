#-------------------------------------------------------------------------------
# Name:        Score Graphs
# Purpose:     Builds graphs to compare the score types for the course, professor
#              or course and professor that the user searched for. 
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

import graphs

def df_maker(args_from_ui, sentiment_or_score, graph_type):
    '''
    Uses the query functions in courses to get a dataframe corresponding to the user's search, 
    then returns a dataframe reduced by get_small_df that includes the columns required by the
    different possible types of graphs (specified by sentiment_or_score, where the two options
    are "sentiment" or "score"). 
    Depending on the user's input, graph_type can be either "prof" or "course."
    '''
    if graph_type == "prof":
        prof_df, dept_df, dept = courses.find_courses(args_from_ui)
        small_df, year = get_small_df(prof_df, graph_type)


    if graph_type == "course":
        course_df, dept_df = courses.find_courses(args_from_ui)
        course_df['prof_name'] = course_df['fn'].astype('str') + ' ' + course_df['ln']
        dept = args_from_ui['dept']
        small_df, year = get_small_df(course_df, graph_type)
    

    if sentiment_or_score == "sentiment":
        columns_to_graph = ['inst_sentiment', 'course_sentiment']

    if sentiment_or_score == "score":
        columns_to_graph = ['prof_score', 'ass_score', 'over_score', 'test_score']

    current_columns = list(small_df.columns)
    columns_to_graph = list(set(current_columns).intersection(columns_to_graph))
    continuous_df = small_df[columns_to_graph]

    compare_to_dept_columns = list(continuous_df.columns)
    dept_df = dept_df[compare_to_dept_columns].mean()
    dept_df.rename(index = dept, inplace = True)
    continuous_df = continuous_df.append(dept_df)
    
    return continuous_df

def get_small_df(dataframe, prof_or_course):
    '''
    Drops results from successive years from the dataframe so that the resulting graph
    will not have more than 10 groups of columns. 
    This happens in slightly different ways corresponding to the data visualization 
    requirements for "prof" or "course" type graphs. 
    '''
    current_year = 2018
    timespan = 15
    if prof_or_course == "prof":
        while dataframe.course.unique().shape[0] > 10:
            timespan -= 1
            if timespan == 1:
                break
            dataframe = dataframe[dataframe.year >= current_year - timespan]
        dataframe = dataframe.groupby(['course']).mean()

    if prof_or_course == "course":
        while dataframe.prof_name.unique().shape[0] > 10:
            if timespan == 1:
                break
            timespan -= 1
            dataframe = dataframe[dataframe.year >= current_year - timespan]
        dataframe = dataframe.groupby(['prof_name']).mean()



    return dataframe, current_year - timespan


def course_and_prof_score_df_maker(args_from_ui):
    '''
    If the user searches by course and professor, this code will produce a graph that compares the scores 
    for this professor averaged over every time they taught the course, the time demands made by
    other professors who  have taught this course, departmental average time demands, and this professor's average
    time demands.
    '''
    dept = args_from_ui['dept']
    prof = args_from_ui['prof_fn'] + " " + args_from_ui['prof_ln']
    course = dept + " " + args_from_ui['course_num']
    course_and_prof =  course + " taught by " + prof
    course_and_prof_df, dept_df, course_df, prof_df = courses.find_courses(args_from_ui)
    course_and_prof_df = course_and_prof_df.mean().to_frame()
    dept_df = dept_df.mean()
    course_df = course_df.mean()
    prof_df = prof_df.mean()
    scores_df = pd.concat([course_and_prof_df, dept_df, course_df, prof_df], axis = 1)
    scores_df.columns = [course_and_prof, dept, course, prof]
    scores_df = scores_df.dropna(how = "all", axis = 0)
    return scores_df.transpose()


def columns_to_graph(scores_df, sentiment_or_score):
    '''
    Returns only the columns of interest in the case when the user searches for course and professor at the same time. 
    '''
    if sentiment_or_score == "sentiment":
        columns_to_graph = ['inst_sentiment', 'course_sentiment']

    if sentiment_or_score == "score":
        columns_to_graph = ['prof_score', 'ass_score', 'over_score', 'test_score']

    current_columns = list(scores_df.columns)
    columns_to_graph = list(set(current_columns).intersection(columns_to_graph))
    scores_df = scores_df[columns_to_graph]

    return scores_df
    

def graph_from_df(continuous_df):
    '''
    Given a dataframe of continuous non-time data, creates a grouped bar graph displaying scores 
    and sentiment scores for that data. 
    Different versions of matplotlib require you to switch out "left" for "x" sometimes in 
    the line that starts with "bar = "
    The error that will let you know that this is happening is: "bar() missing 1 required positional argument"
    '''
    colors = ['b', 'g', 'r', 'k', 'm', 'y']
    n = continuous_df.shape[0]
    ind = np.arange(n)
    width = 0.1  
    offset = 0
    plt.figure(figsize = (20, 7))
    bars = []
    for column in continuous_df:
        bar = plt.bar(left = ind - (offset * width), width=width, height=continuous_df[column], color = colors[offset])
        offset += 1
        bars.append(bar)
    xnames = list(continuous_df.axes[0])
    plt.xticks(ind, xnames, rotation = 10, fontsize = 10, ha = 'right')
    legend_contents = list([continuous_df.axes[1]])[0]
    if "prof_score" in legend_contents:
        legend = []
        legend_translator = {'prof_score':'Professor Score', 
                            'ass_score':'Assignment Score', 
                            'test_score':"Test Score", 
                            'over_score':'Overall Score'}
        for label in legend_contents:
            legend.append(legend_translator[label])
        legend_contents = legend
    if 'inst_sentiment' in legend_contents:
        legend = []
        legend_translator = {'inst_sentiment':'Professor sentiment score', 
                            'course_sentiment': "Course sentiment score"}
        for label in legend_contents:
            legend.append(legend_translator[label])
        legend_contents = legend

    plt.legend(bars, legend_contents)
    plt.ylim(ymax = 100)
    return plt


def prof_score_graph(args_from_ui):
    '''
    Creates a graph for a professor's scores compared to the department average. 
    '''
    continuous_df = df_maker(args_from_ui, "score", "prof")
    if 'prof_score' in continuous_df:
            continuous_df = continuous_df.sort_values(by = 'prof_score', axis = 0, ascending = False)
    plt = graph_from_df(continuous_df)
    prof = args_from_ui['prof_fn'] + " " + args_from_ui['prof_ln']
    title = prof + "'s aggregated scores with dept avg."
    plt.title(title)
    plt.ylabel("Aggregated scores from reviews", fontsize = 15)
    plt.savefig('./static/images/profscore.png')

def prof_sentiment_graph(args_from_ui):
    '''
    Creates a graph for a professor's sentiment scores compared to the department average. 
    '''
    continuous_df = df_maker(args_from_ui, "sentiment", "prof")
    if 'inst_sentiment' in continuous_df:
            continuous_df = continuous_df.sort_values(by = 'inst_sentiment', axis = 0, ascending = False)
    plt = graph_from_df(continuous_df)
    prof = args_from_ui['prof_fn'] + " " + args_from_ui['prof_ln']
    title = prof + "'s sentiment scores with dept avg."
    plt.title(title)
    plt.ylabel("Sentiment scores from reviews", fontsize = 15)
    plt.savefig('./static/images/profsent.png')

def course_sentiment_graph(args_from_ui):
    '''
    Creates a graph for the sentiment scores for all professors that have taught a
    class compared to the department average. 
    '''
    continuous_df = df_maker(args_from_ui, "sentiment", "course")
    if 'inst_sentiment' in continuous_df:
            continuous_df = continuous_df.sort_values(by = 'inst_sentiment', axis = 0, ascending = False) 
    plt = graph_from_df(continuous_df)
    course = args_from_ui['dept'] + " " + args_from_ui['course_num']
    title = "Sentiment scores for " + course + " with dept avg."
    plt.title(title)
    plt.ylabel("Sentiment scores from reviews", fontsize = 15)
    plt.savefig('./static/images/coursesent.png')

def course_score_graph(args_from_ui):
    '''
    Creates a graph for the scores for all professors that have taught a class compared to
    the department average. 
    '''
    continuous_df = df_maker(args_from_ui, "score", "course")
    if 'prof_score' in continuous_df:
            continuous_df = continuous_df.sort_values(by = 'prof_score', axis = 0, ascending = False)
    plt = graph_from_df(continuous_df)
    course = args_from_ui['dept'] + " " + args_from_ui['course_num']
    title = "Aggregated scores for " + course + " with dept avg."
    plt.title(title)
    plt.ylabel("Aggregated scores from reviews", fontsize = 15)
    plt.savefig('./static/images/coursescore.png')

def course_and_prof_score_graph(args_from_ui):
    '''
    Creates a graph for the scores for a specific course taught by a specific professor together with 
    information about that course taught by all professors, all courses taught by that specific professor, 
    and the average overall department scores. 
    '''
    scores_df = course_and_prof_score_df_maker(args_from_ui)
    scores_df = columns_to_graph(scores_df, 'score')
    plt = graph_from_df(scores_df)
    prof = args_from_ui['prof_fn'] + ' ' + args_from_ui['prof_ln']
    dept = args_from_ui['dept']
    course = dept + ' ' + args_from_ui['course_num']
    title = "Scores for " + prof + "'s " + course + ' with scores from dept and past classes'
    plt.title(title)
    plt.ylabel("Aggregated scores from evaluations", fontsize = 15)
    plt.savefig('./static/images/courseprofscore.png')

def course_and_prof_sentiment_graph(args_from_ui):
    '''
    Creates a graph for the sentiment scores for a specific course taught by a specific professor together with 
    information about that course taught by all professors, all courses taught by that specific professor, 
    and the average overall department scores. 
    '''
    scores_df = course_and_prof_score_df_maker(args_from_ui)
    scores_df = columns_to_graph(scores_df, 'sentiment')
    plt = graph_from_df(scores_df)
    prof = args_from_ui['prof_fn'] + ' ' + args_from_ui['prof_ln']
    dept = args_from_ui['dept']
    course = dept + ' ' + args_from_ui['course_num']
    title = "Sentiment scores for " + prof + "'s " + course + ' with scores from dept and past classes'
    plt.title(title)
    plt.ylabel("Aggregated scores from evaluations", fontsize = 15)
    plt.savefig('./static/images/courseprofsent.png')

def non_time_graphs(args_from_ui):
    '''
    Given arguments from the user, calls the appropriate graphing function to display the information requested. 
    '''
    if len(args_from_ui) == 2:

        if 'prof_fn' in args_from_ui and 'prof_ln' in args_from_ui:
            prof_score_graph(args_from_ui)
            prof_sentiment_graph(args_from_ui)

        elif 'dept' in args_from_ui:
            course_score_graph(args_from_ui)
            course_sentiment_graph(args_from_ui)

        

    else:
        course_and_prof_score_graph(args_from_ui)
        course_and_prof_sentiment_graph(args_from_ui)

