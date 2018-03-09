import json
import traceback
import sys
import csv
import os
import io
import pandas as pd

from django.shortcuts import render
from django import forms

from courses import find_courses
from course_name_converter import convert_course_name_to_course_num
from gen_wordcloud import get_wc
import score_graphs
from graphs import graph_it

NOPREF_STR = 'No preference'
RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')


def _load_column(filename, col=0):
    """Load single column from csv file."""
    with open(filename) as f:
        col = list(zip(*csv.reader(f)))[0]
        return list(col)


def _load_res_column(filename, col=0):
    """Load column from resource directory."""
    return _load_column(os.path.join(RES_DIR, filename), col=col)


def _build_dropdown(options):
    """Convert a list to (value, caption) tuples."""
    return [(x, x) if x is not None else ('', NOPREF_STR) for x in options]


DEPTS = _build_dropdown([None] + _load_res_column('dept_list.csv'))
COURSE_NUMS = _build_dropdown([None] + _load_res_column('course_num_list.csv'))
COURSE_NAMES = _build_dropdown([None] + _load_res_column('course_name_list.csv'))
PROFS_FN = _build_dropdown([None] + _load_res_column('prof_fn_list.csv'))
PROFS_LN = _build_dropdown([None] + _load_res_column('prof_ln_list.csv'))
RANK_METHOD = [('', NOPREF_STR), ('avg_time', 'Average Time Spent'),
              ('prof_score', 'Average Professor Score')]


class SearchForm_course(forms.Form):
    dept = forms.ChoiceField(label='Department', choices=DEPTS, required=False)
    course_num = forms.ChoiceField(label='Course Number', choices=COURSE_NUMS, required=False)
    course_name = forms.ChoiceField(label='Course Name', choices=COURSE_NAMES, required=False)


class SearchForm_prof(forms.Form):
    prof_fn = forms.ChoiceField(label='Professor\'s First Name', choices=PROFS_FN, required=False)
    prof_ln = forms.ChoiceField(label='Professor\'s Last Name', choices=PROFS_LN, required=False)
    # show_args = forms.BooleanField(label='Show args_to_ui',
    #                                required=False) # delete this in end


class SearchForm_rank(forms.Form):
    rank = forms.ChoiceField(label='Rank Method', choices=RANK_METHOD, required=False)


def home(request):
    for file in os.listdir(os.path.join(os.path.dirname(__file__), '..', 'static', 'images')):
        if file.endswith(".png"):
            os.remove(os.path.join(os.path.dirname(__file__), '..', 'static', 'images', file))

    context = {}
    res = None
    if request.method == 'GET':
        # create form instances and populate them with data from the request:
        form_course = SearchForm_course(request.GET)
        form_prof = SearchForm_prof(request.GET)
        form_rank = SearchForm_rank(request.GET)
        
        # check if forms are valid:
        args = {}
        num_args = 0 # used in conditional check later on
        if form_course.is_valid():
            # Convert form data to an args dictionary for find_courses
            data = form_course.cleaned_data
            if data['dept']:
                args['dept'] = data['dept']
                num_args += 1
            if data['course_num'] and data['course_name']: 
            # users only need to submit one, but if they submit both, we pick one field for the sql query
                args['course_num'] = data['course_num']
            elif data['course_num']:
                args['course_num'] = data['course_num']
            elif data['course_name']:
                course_num = convert_course_name_to_course_num(data['dept'], data['course_name'])
                args['course_num'] = course_num

        if form_prof.is_valid():
            data = form_prof.cleaned_data
            if data['prof_fn']:
                args['prof_fn'] = data['prof_fn']
                num_args += 1
            if data['prof_ln']:
                args['prof_ln'] = data['prof_ln']
            # if data['show_args']:
            #     context['args'] = 'args_to_ui = ' + json.dumps(args, indent=2)
        
        if form_rank.is_valid():
            if form_rank.cleaned_data['rank']:
                args['rank'] = form_rank.cleaned_data['rank']

        # check the conditional inputs of the dropdown menus
        if ('dept' in args) != ('course_num' in args):
            context['err'] = "To search by course, \
                department and course number or course name are required."
        elif ('prof_fn' in args) != ('prof_ln' in args):
            context['err'] = "To search by professor, \
                both first name and last name are required."
        elif ('rank' in args) and num_args > 0:
            context['err'] = "You cannot perform a search and \
                view department rankings in the same request."
        else: # a valid set of search categories
            try:
                res = find_courses(args)[0]
                if len(res) > 0: # evals were found
                    context['columns'] = res.columns
                    df_rows = res.values.tolist()
                    result = []
                    for row in df_rows:
                        result.append(tuple(row))
                    context['result'] = result
                    context['num_results'] = len(res)
                    
                    if 'rank' in args:
                        context['rank'] = True
                    # we want to generate graphs and images
                    else:
                        context['rank'] = False
                        get_wc(args)
                        graph_it(args)
                        score_graphs.non_time_graphs(args)
                    # print(args)
                    if 'dept' in args and 'prof_fn' in args:
                        context['graph_type'] = 'course_and_prof'
                    elif 'dept' in args and 'course_num' in args:
                        context['graph_type'] = 'course'
                    elif 'prof_fn' in args:
                        context['graph_type'] = 'prof'
                    # print(context)
                
                else:
                    res = None

            except Exception as e:
                 print('Exception caught')
                 bt = traceback.format_exception(*sys.exc_info()[:3])
                 context['err'] = """
                 An exception was thrown in find_courses:
                 <pre>{}
         {}</pre>
                 """.format(e, '\n'.join(bt))
                 res = None

    else:
        form_course = SearchForm_course()
        form_prof = SearchForm_prof()
        form_rank = SearchForm_rank()

    # Handle different responses of res
    if res is None:
        context['result'] = None

    else: #create outputs (ex. tables and graphs)
        context['columns'] = res.columns
        df_rows = res.values.tolist()
        result = []
        for row in df_rows:
            result.append(tuple(row))
        context['result'] = result
        context['num_results'] = len(res)

    context['form_course'] = form_course
    context['form_prof'] = form_prof
    context['form_rank'] = form_rank
    return render(request, 'index.html', context)
