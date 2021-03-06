import courses
import pandas as pd


def display_dyadic_partitioning(args):
    if len(args) == 2:
        if 'prof_fn' in args and 'prof_ln' in args:
            return prof_display(args)
        elif 'dept' in args:
            return course_display(args)
    else:
        return course_and_prof_display(args)


def avg_generator(df):
    would_recommend = pd.factorize(df.would_recommend)[0]
    would_recommend = would_recommend[would_recommend != -1]
    would_recommend = 1 - would_recommend.mean()
    would_like_inst = pd.factorize(df.would_like_inst)[0]
    would_like_inst = would_like_inst[would_like_inst != -1]
    would_like_inst = 1 - would_like_inst.mean()
    return would_recommend, would_like_inst



def course_display(args):
    course_name = args['dept'] + " " + args['course_num']
    course_df, dept_df = courses.find_courses(args)
    would_recommend, would_like_inst = avg_generator(course_df)
    would_recommend_str = "{:.2%}".format(would_recommend) + " of students of " + course_name + " would recommend it."
    would_like_str = "{:.2%}".format(would_like_inst) + " of students of " + course_name + " felt positively about their instructor."
    return would_like_str, would_recommend_str


def prof_display(args):
    prof_name = args['prof_fn'] + " " + args['prof_ln']
    prof_df, dept_df, primary_dept = courses.find_courses(args)
    would_recommend, would_like_inst = avg_generator(prof_df)
    would_recommend_str = "{:.2%}".format(would_recommend) + " of students taught by " + prof_name + " would recommend this professor overall."
    would_like_str = "{:.2%}".format(would_like_inst) + " of students taught by " + prof_name + " felt positively about their instructor."
    return would_like_str, would_recommend_str
    

def course_and_prof_display(args):
    course_name = args['dept'] + " " + args['course_num']
    course_and_prof_df, dept_df, course_df, prof_df = courses.find_courses(args)
    prof_name = args['prof_fn'] + " " + args['prof_ln']
    would_recommend, would_like_inst = avg_generator(course_and_prof_df)
    would_recommend_str = "{:.2%}".format(would_recommend) + " of students who took " + course_name + " taught by " + prof_name + " would recommend it overall."
    would_like_str = "{:.2%}".format(would_like_inst) + " of students who took " + course_name + " taught by " + prof_name + " felt positively about their instructor."
    return would_like_str, would_recommend_str
