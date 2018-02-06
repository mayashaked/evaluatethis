#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      alex
#
# Created:     26/01/2018
# Copyright:   (c) alex 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import re
import csv
import sys

def main(username, password, CHROMEDRIVER_PATH):

    driver = webdriver.Chrome(CHROMEDRIVER_PATH)
    driver.implicitly_wait(10)
    driver.get("https://evaluations.uchicago.edu/")
    elem = driver.find_element_by_name("j_username")
    elemp = driver.find_element_by_name("j_password")
    elem.send_keys(username)
    elemp.send_keys(password)
    elemp.send_keys(Keys.RETURN)
    choices = [c.text for c in driver.find_elements_by_tag_name("option") if c.text != ""]
    depts = []
    years = []
    for c in choices:
        d = re.search("\(([A-Z]{4})\)", c)
        y = re.search("[0-9]{4}-[0-9]{4}", c)
        if d:
           depts.append(d[1])
        if y:
           years.append(y[0])

    visit_pages(driver, depts, years)


def visit_pages(driver, depts, years):
    links_to_evals = []
    for d in depts:
        for y in years:
            deptbox = Select(driver.find_element_by_id("department"))
            yearbox = Select(driver.find_element_by_id("AcademicYear"))
            deptbox.select_by_value(d)
            yearbox.select_by_visible_text(y)
            go = driver.find_element_by_id("keywordSubmit")
            go.click()
            evals = driver.find_elements_by_partial_link_text(d)
            eval_links = [[e.get_attribute("href")] for e in evals]
            links_to_evals += eval_links

    write(links_to_evals)


def write(stuff):
    with open('ALL_LINKS.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(stuff)

if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    except:
        print("Arguements are: 'username', 'password', 'path to chromedriver.exe'")
