#-------------------------------------------------------------------------------
# Name:        ui_lists
# Purpose:     Queries the sql database and builds csv files of lists of 
#              department codes, course numbers, course names, professor 
#              last names, and professor first names to populate
#              the dropdown menus on the website.
#
# Author:      Lily Li
#
# Created:     03/02/2018
#-------------------------------------------------------------------------------

import sqlite3
import csv


def generate_lists():
    connection = sqlite3.connect('reevaluations.db')
    c = connection.cursor()

    # get lists of unique, non-null values from sql database
    dept = c.execute('''SELECT DISTINCT dept FROM courses WHERE dept IS NOT 
        NULL and dept <> "" ORDER BY dept''').fetchall()
    course_num = c.execute('''SELECT DISTINCT course_number FROM courses 
        WHERE course_number IS NOT NULL and course_number <> "" ORDER BY 
        course_number''').fetchall()
    course_name = c.execute('''SELECT DISTINCT course FROM courses 
        WHERE course IS NOT NULL and course <> "" ORDER BY 
        course''').fetchall()
    prof_ln = c.execute('''SELECT DISTINCT ln FROM profs WHERE 
        ln IS NOT NULL and ln <> "" ORDER BY ln''').fetchall()
    prof_fn = c.execute('''SELECT DISTINCT fn FROM profs WHERE 
        fn IS NOT NULL and fn <> "" ORDER BY fn''').fetchall()

    connection.close()

    # write lists of unique values to files
    f = open('dept_list.csv', 'w')
    w = csv.writer(f, delimiter="|")
    for row in dept:
        w.writerow(row)
    f.close()

    f = open('course_num_list.csv', 'w')
    w = csv.writer(f, delimiter="|")
    for row in course_num:
        w.writerow(row)
    f.close()

    f = open('course_name_list.csv', 'w')
    w = csv.writer(f, delimiter="|")
    for row in course_name:
        w.writerow(row)
    f.close()

    f = open('prof_ln_list.csv', 'w')
    w = csv.writer(f, delimiter="|")
    for row in prof_ln:
        w.writerow(row)
    f.close()

    f = open('prof_fn_list.csv', 'w')
    w = csv.writer(f, delimiter="|")
    for row in prof_fn:
        w.writerow(row)
    f.close()
