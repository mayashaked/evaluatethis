#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      alex
#
# Created:     24/01/2018
# Copyright:   (c) alex 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys

def main(message):
    print(message)
    driver = webdriver.Chrome(PATH_TO_CHROMEDRIVER)
    do_it(driver, message)

def do_it(driver, message):
    driver.get("https://action.donaldjtrump.com/mainstream-media-accountability-survey/")
    forms = []
    elem = []
    for n in range(3382, 3410):
        try:
            e = driver.find_element_by_id("id_question_" + str(n) + "_0_Other")
            elem.append(e)
        except:
            pass

    for n in range(3382, 3410):
        try:
            e = driver.find_element_by_id("id_question_" + str(n) + "_1")
            forms.append(e)
        except:
            pass
    for e in elem:
         e.click()
    for f in forms:
        f.send_keys(message)
    submit = driver.find_element_by_name("respond")
    fname = driver.find_element_by_id("id_first_name")
    lname = driver.find_element_by_id("id_last_name")
    zipcode = driver.find_element_by_id("id_postal_code")
    email = driver.find_element_by_id("id_email")
    fname.send_keys("DONALD")
    lname.send_keys("TRUMP")
    zipcode.send_keys("60615")
    email.send_keys("BUILDAWALL@gmail.com")
    submit.click()

if __name__ == '__main__':
    main(sys.argv[1])
