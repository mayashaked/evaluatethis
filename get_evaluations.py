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
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import re
import sys

def main(pwd):
    links = []
    with open('ALL_LINKS.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            for l in row:
                links.append(l)

    driver = webdriver.Chrome("C:/Users/alex/Downloads/chromedriver_win32/chromedriver.exe")
    driver.get("https://evaluations.uchicago.edu/")
    elem = driver.find_element_by_name("j_username")
    elemp = driver.find_element_by_name("j_password")
    elem.send_keys("alexmaiorella")
    elemp.send_keys(pwd)
    elemp.send_keys(Keys.RETURN)

    raw_evals = []
    for l in links[:20]:
        driver.get(l)
        raw_eval = driver.find_element_by_tag_name("html").text
        title = driver.find_element_by_id("page-title").text
        try:
            dept = re.search("[A-Z]{4}", title)[0]
        except:
            dept = 'MISFIT'
        with open(dept + '-EVALS.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([raw_eval])



if __name__ == '__main__':
    main(sys.argv[1])
