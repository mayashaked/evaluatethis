#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      alex
#
# Created:     28/01/2018
# Copyright:   (c) alex 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import sys

def main(usrme, pwd, start):
    links = []
    with open('ALL_LINKS.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            for l in row:
                links.append(l)

    driver = webdriver.Chrome("/home/alexmaiorella/cmsc12200-win-18-alexmaiorella/Project/chromedriver")
    driver.get("https://evaluations.uchicago.edu/")
    elem = driver.find_element_by_name("j_username")
    elemp = driver.find_element_by_name("j_password")
    elem.send_keys(usrme)
    elemp.send_keys(pwd)
    elemp.send_keys(Keys.RETURN)

    raw_evals = []
    failures = []
    for index, link in enumerate(links[start:]):
        driver.get(link)
        driver.implicitly_wait(10)
        raw_eval = driver.find_element_by_tag_name("html").text
        title = driver.find_element_by_id("page-title").text
        print((index + start, title))
        try:
            dept = re.findall("[A-Z]{4}", title)[0]
            with open(dept + '-EVALS.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([title, raw_eval])
        except:
            print("FYI: I failed to get the evaluation for link: " + str(index + start))
            failures.append(index + start)

    return failures


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
