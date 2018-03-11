import courses
import pandas as pd

def display_dyadic_partitioning(args_from_ui):
    if len(args_from_ui) == 2:
        if 'prof_fn' in args_from_ui and 'prof_ln' in args_from_ui:
            return prof_display(args_from_ui)
            
        elif 'dept' in args_from_ui:
            return course_display(args_from_ui)

    else:
        return course_and_prof_display(args_from_ui)

def course_display(args_from_ui):
    if "course_num" in args_from_ui:
        course_name = args_from_ui['dept'] + " " + args_from_ui['course_num']
    elif "course_name" in args_from_ui:
        course_name = args_from_ui['dept'] + " " + args_from_ui['course_name']
    course_df, dept_df = courses.find_courses(args_from_ui)
    would_recommend = 1 - pd.factorize(course_df.would_recommend)[0].mean()
    would_like_inst = 1 - pd.factorize(course_df.would_like_inst)[0].mean()
    would_recommend_str = "{:.2%}".format(would_recommend) + " of classes of " + course_name + " would recommend it."
    would_like_str = "{:.2%}".format(would_like_inst) + ' of classes of' + course_name + ' classes felt positively about their instructor.'
    return would_recommend_str, would_like_str
    


def prof_display(args_from_ui):
    prof_name = args_from_ui['prof_fn'] + " " + args_from_ui['prof_ln']
    prof_df, dept_df, primary_dept = courses.find_courses(args_from_ui)
    would_recommend = 1 - pd.factorize(prof_df.would_recommend)[0].mean()
    would_like_inst = 1 - pd.factorize(prof_df.would_like_inst)[0].mean()
    would_recommend_str = "{:.2%}".format(would_recommend) + " of classes taught by " + prof_name + " would recommend it overall."
    would_like_str = "{:.2%}".format(would_like_inst) + ' of classes taught by ' + prof_name + ' classes felt positively about their instructor.'
    return would_recommend_str, would_like_str
    

def course_and_prof_display(args_from_ui):
    course_and_prof_df, dept_df, course_df, prof_df = courses.find_courses(args_from_ui)
    prof_name = args_from_ui['prof_fn'] + " " + args_from_ui['prof_ln']
    would_recommend = 1 - pd.factorize(course_and_prof_df.would_recommend)[0].mean()
    would_like_inst = 1 - pd.factorize(course_and_prof_df.would_like_inst)[0].mean()
    would_recommend_str = "{:.2%}".format(would_recommend) + " of " + course_name + " classes taught by " + prof_name + " would recommend it overall."
    would_like_str = "{:.2%}".format(would_like_inst) + " of " + course_name + " classes taught by " + prof_name + ' felt positively about their instructor.'
    return would_recommend_str, would_like_str