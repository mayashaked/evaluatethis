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

from courses import find_courses
from gen_wordcloud import get_wc

NOPREF_STR = 'No preference'
RES_DIR = os.path.join(os.path.dirname(__file__), '..', 'res')
COLUMN_NAMES = dict(
    dept = 'Department',
    course_num = 'Course Number',
    prof = 'Professor',
)


# def _valid_result(res):
#     """Validate results returned by find_courses."""
#     (HEADER, RESULTS) = [0, 1]
#     ok = (isinstance(res, (tuple, list)) and
#           len(res) == 2 and
#           isinstance(res[HEADER], (tuple, list)) and
#           isinstance(res[RESULTS], (tuple, list)))
#     if not ok:
#         return False

#     n = len(res[HEADER])

#     def _valid_row(row):
#         return isinstance(row, (tuple, list)) and len(row) == n
#     return reduce(and_, (_valid_row(x) for x in res[RESULTS]), True)


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
PROFS_FN = _build_dropdown([None] + _load_res_column('prof_fn_list.csv'))
PROFS_LN = _build_dropdown([None] + _load_res_column('prof_ln_list.csv'))


class SearchForm_course(forms.Form):
    dept = forms.ChoiceField(label='Department', choices=DEPTS, required=False)
    course_num = forms.ChoiceField(label='Course Number', choices=COURSE_NUMS, required=False)


class SearchForm_prof(forms.Form):
    prof_fn = forms.ChoiceField(label='Professor\'s First Name', choices=PROFS_FN, required=False)
    prof_ln = forms.ChoiceField(label='Professor\'s Last Name', choices=PROFS_LN, required=False)
    show_args = forms.BooleanField(label='Show args_to_ui',
                                   required=False) # delete this in end


def home(request):
    context = {}
    res = None
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form_course = SearchForm_course(request.GET)
        form_prof = SearchForm_prof(request.GET)
        # check whether it's valid:
        args = {}
        if form_course.is_valid():
            # Convert form data to an args dictionary for find_courses
            dept = form_course.cleaned_data['dept']
            if dept:
                args['dept'] = dept
            course_num = form_course.cleaned_data['course_num']
            if course_num:
                args['course_num'] = course_num
            
        if form_prof.is_valid():   
            prof_fn = form_prof.cleaned_data['prof_fn']
            if prof_fn:
                args['prof_fn'] = prof_fn
            prof_ln = form_prof.cleaned_data['prof_ln']
            if prof_ln:
                args['prof_ln'] = prof_ln
            if form_prof.cleaned_data['show_args']:
                context['args'] = 'args_to_ui = ' + json.dumps(args, indent=2)

            try:
                res = find_courses(args) #result of courses.py
                context["wordcloud"] = None
                # result of courses.py
                wc = get_wc(args)
                context["wordcloud"] = wc
                plt.figure(figsize = (10, 5))
                plt.imshow(wc)
                plt.axis("off")
                plt.savefig('./static/images/wordcloud.png')
                plt.close()


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
        form = SearchForm()

    # Handle different responses of res
    if res is None:
        context['result'] = None
    elif isinstance(res, str):
        context['result'] = None
        context['err'] = res
        result = None
    # elif not _valid_result(res):
    #     context['result'] = None
    #     context['err'] = ('Return of find_courses has the wrong data type. '
    #                       'Should be a tuple of length 4 with one string and '
    #                       'three lists.')
    
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
    return render(request, 'index.html', context)
