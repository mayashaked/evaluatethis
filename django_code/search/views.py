import json
import traceback
import sys
import csv
import os

from functools import reduce
from operator import and_

from django.shortcuts import render
from django import forms

#from courses import find_courses

from django.shortcuts import render_to_response

def index(request):
    return render('templates/index.html')