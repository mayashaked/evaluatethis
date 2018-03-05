import json
import traceback
import sys
import csv
import os
import io
import pandas as pd
import matplotlib.pyplot as plt

from functools import reduce
from operator import and_

from django.shortcuts import render
from django import forms

from courses import find_courses #, get_wc

NOPREF_STR = 'No preference'
RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')
COLUMN_NAMES = dict(
    dept = 'Department',
    course_num = 'Course Number',
    prof = 'Professor',
)


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


# create the dropdown menus that appear on the website 
DEPTS = _build_dropdown([None] + _load_res_column('dept_list.csv'))
COURSE_NUMS = _build_dropdown([None] + _load_res_column('course_num_list.csv'))
PROFS_FN = _build_dropdown([None] + _load_res_column('prof_fn_list.csv'))
PROFS_LN = _build_dropdown([None] + _load_res_column('prof_ln_list.csv'))


class SearchForm_course_dept(forms.Form):
    dept = forms.ChoiceField(label='Department', choices=DEPTS, required=False)


class SearchForm_course_num(forms.Form):
    course_num = forms.ChoiceField(label='Course Number', choices=COURSE_NUMS, required=False)


class SearchForm_prof_fn(forms.Form):
    prof_fn = forms.ChoiceField(label='Professor\'s First Name', choices=PROFS_FN, required=False)


class SearchForm_prof_ln(forms.Form):
    prof_ln = forms.ChoiceField(label='Professor\'s Last Name', choices=PROFS_LN, required=False)


# the main function. it gathers the data from the dropdown menus we defined 
# above, cleans the data, checks if the input queries are valid, and returns
# outputs (tables, graphs, images) to be rendered in the html text
def home(request):
    context = {}
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form_course_dept = SearchForm_course_dept(request.GET)
        form_course_num = SearchForm_course_num(request.GET)
        form_prof_fn = SearchForm_prof_fn(request.GET)
        form_prof_ln = SearchForm_prof_ln(request.GET)
        # check whether the forms are valid and convert form data to an args 
        # dictionary for find_courses
        args = {}
        if form_course_dept.is_valid():
            dept = form_course_dept.cleaned_data['dept']
            if dept:
                args['dept'] = dept
        if form_course_num.is_valid():
            course_num = form_course_num.cleaned_data['course_num']
            if course_num:
                args['course_num'] = course_num
        if form_prof_fn.is_valid():   
            prof_fn = form_prof_fn.cleaned_data['prof_fn']
            if prof_fn:
                args['prof_fn'] = prof_fn
        if form_prof_ln.is_valid():   
            prof_ln = form_prof_ln.cleaned_data['prof_ln']
            if prof_ln:
                args['prof_ln'] = prof_ln

        # check the conditional inputs of the dropdown menus
        if ('dept' in args) == ('course_num' in args): 
        #either they were both inputs or neither were inputs
            if ('prof_fn' in args) == ('prof_ln' in args):
                try:
                    res = find_courses(args) # inputs are valid, run courses.py                
                    context["wordcloud"] = None
                    # result of courses.py
                    '''wc = get_wc(args)
                    context["wordcloud"] = wc
                    f = io.BytesIO()
                    plt.figure(figsize = (15, 8))
                    plt.imshow(wc)
                    plt.axis("off")
                    plt.savefig(f, format = "png")
                    plt.clf()'''

                except Exception as e:
                    print('Exception caught')
                    bt = traceback.format_exception(*sys.exc_info()[:3])
                    context['err'] = """
                    An exception was thrown in find_courses:
                    <pre>{}
                    {}</pre>
                    """.format(e, '\n'.join(bt))
            else:
                context['err'] = forms.ValidationError("To search by professor, \
                    both first name and last name are required.")
                res = None
        else:
            context['err'] = forms.ValidationError("To search by course, both \
                department and course number are required.")
            res = None

    else:
        form = SearchForm()

    # handle situation when res is None (i.e. no inputs have been entered)
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
   
    context['form_course_dept'] = form_course_dept
    context['form_course_num'] = form_course_num
    context['form_prof_fn'] = form_prof_fn
    context['form_prof_ln'] = form_prof_ln
    return render(request, 'index.html', context)
