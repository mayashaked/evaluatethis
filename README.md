So this fantastic project involes scraping course evaluations and using the data to create neat profiles for each professor and an easy way to compare them.

Notes: 
    I got selenium to work so we can login to shibbolith from command line. First install selenium (using pip) and chromedriver from this     link (https://sites.google.com/a/chromium.org/chromedriver/). Then in python:

    >>> from selenium import webdriver
    >>> from selenium.webdriver.common.keys import Keys
    >>> driver = webdriver.Chrome(PATH TO CHROMEDRIVER.EXE)
    >>> driver.get("https://evaluations.uchicago.edu/")
    >>> elem = driver.find_element_by_name("j_username")
    >>> elemp = driver.find_element_by_name("j_password")
    >>> elem.send_keys("USERNAME HERE")
    >>> elemp.send_keys("PASSWORD HERE")
    >>> elemp.send_keys(Keys.RETURN)

    Literally magical
