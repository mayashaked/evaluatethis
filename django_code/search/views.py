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

def index(request):
    return render_to_response('index.html')