#-------------------------------------------------------------------------------
# Name:        Link Scraper
# Purpose:     Scrape all links to evaluation pages in preparation of scraping
#              the evaluations themselves.
#
# Author:      Alex Maiorella
#
# Created:     01/26/2018
#-------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import re
import csv
import sys

def main(username, password, CHROMEDRIVER_PATH):
    '''
    Initializes chromedriver, navigates to and signs into evaluation site.
    Then scrapes all the possible departments and years (takes 20 seconds or so)
    and calls visit_pages to begin crawling for links.
    Inputs:
        username & password for shibbolith, path to chromedriver executable
    Returns:
        None
    '''
    driver = webdriver.Chrome(CHROMEDRIVER_PATH)

    # This setting ensures that a page is allowed to load completely
    driver.implicitly_wait(10)

    driver.get("https://evaluations.uchicago.edu/")
    elem = driver.find_element_by_name("j_username")
    elemp = driver.find_element_by_name("j_password")

    elem.send_keys(username)
    elemp.send_keys(password)
    elemp.send_keys(Keys.RETURN)

    choices = [c.text for c in driver.find_elements_by_tag_name("option") \
              if c.text != ""]

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
    '''
    Uses dropdown menus on evaluation site to systematically visit every
    combination of year and department in order to find links to every
    evaluation.
    Inputs:
        Chromedriver, list of depts, list of years
    Returns:
        None (calls write function)
    '''
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


def write(links):
    '''
    Writes the list of evaluation links to a csv file.
    '''
    with open('ALL_LINKS.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(links)


if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    except:
        print("Arguements: 'username', 'password', 'path to chromedriver.exe'")
