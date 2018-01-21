#!/usr/bin/env python3

import os
import time
import sys
import unittest, time, re
import argparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main(args):

    if args.browser == "chrome":    
        if args.driver is None: args.driver = "./chromedriver"
        driver = webdriver.Chrome(args.driver)
    if args.browser == "firefox":   
        if args.driver is None: args.driver = "./geckodriver"
        driver = webdriver.Firefox(args.driver)
    if args.browser == "opera":     
        if args.driver is None: args.driver = "./operadriver"
        driver = webdriver.Opera(args.driver)
    if args.browser == "ie":        
        if args.driver is None: args.driver = "./IEDriverServer.exe"
        driver = webdriver.Ie(args.driver)
    
    try:
        driver.implicitly_wait(60)
        driver.set_page_load_timeout(60)

        for line in open(args.passwords):
            if line.strip() == "": continue
            kitnum,password = line.split()
            if not args.kit or kitnum == args.kit:
                download(args,driver,kitnum,password)
    finally:
        driver.quit()

def download(args,driver,kitnum,password):
    def click(element_selector):
        element = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, element_selector)))
        element.click()

    def logon():
        driver.get("https://www.familytreedna.com/sign-in")

        driver.find_element_by_id("kitnum-input").clear()
        driver.find_element_by_id("kitnum-input").send_keys(kitnum)

        driver.find_element_by_id("password-input").clear()
        driver.find_element_by_id("password-input").send_keys(password)
        driver.find_element_by_css_selector("span.ladda-label").click()
        WebDriverWait(driver, 30).until(EC.title_contains("myFTDNA Home"))

    def logout():
        driver.delete_all_cookies()  # logout

    def wait(fname):
        i = 0
        while not os.path.exists(fname):
            print("[{} s] Waiting for {}".format(i,fname))
            time.sleep(5)
            i += 5
        print("Done: {}".format(fname))
    
    def download_ff():
        print("Downloading {}".format(ff_fname))
        driver.get("https://www.familytreedna.com/my/familyfinder/")
        click("#download-csv")
        wait(ff_fname)
    
    def download_cb():
        print("Downloading {}".format(cb_fname))
        driver.get("https://www.familytreedna.com/my/family-finder/chromosome-browser")
        click("#dwnLdAllExcel")
        wait(cb_fname)

    def download_a37():
        print("Downloading {}".format(a37_fname))
        driver.get("https://www.familytreedna.com/my/family-finder/downloads.aspx")
        click("#Content_MainContent_lbAutosomal37")
        wait(a37_fname)

    home = os.getenv("HOME")
    dirname = args.downloads_folder.replace("$HOME",home) + "/"
    date = time.strftime("%Y%m%d",time.localtime(time.time()))

    logon()
    
    if args.ff:
        ff_fname = dirname+"{}_Family_Finder_Matches_{}.csv".format(kitnum,date)
        if os.path.exists(ff_fname):
            print("Already exists: {}".format(ff_fname))
        else:
            download_ff()
    
    if args.cb:
        cb_fname = dirname+"{}_Chromosome_Browser_Results_{}.csv".format(kitnum,date)
        if os.path.exists(cb_fname):
            print("Already exists: {}".format(cb_fname))
        else:
            download_cb()

    if args.a37:
        a37_fname = dirname+"{}_Autosomal_o37_Results_{}.csv.gz".format(kitnum,date)
        if os.path.exists(a37_fname):
            print("Already exists: {}".format(a37_fname))
        else:
            download_a37()

    time.sleep(4)
    logout()

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kit")
    parser.add_argument("--all",action="store_true",default=True)
    parser.add_argument("--ff",action="store_true",default=False)
    parser.add_argument("--cb",action="store_true",default=False)
    parser.add_argument("--37",action="store_true",default=False,dest="a37")
    parser.add_argument("--passwords",default="passwords.txt")
    parser.add_argument("--driver") #,default="./chromedriver")
    parser.add_argument("--downloads-folder",default="$HOME/Downloads")
    parser.add_argument("--browser",choices=["chrome","firefox","opera","ie"],default="chrome")
    parser.add_argument("--quiet",action="store_true",default=False)
    args = parser.parse_args()
    if args.ff: args.all = False
    if args.cb: args.all = False
    if args.a37: args.all = False
    if args.all:
        args.ff = True
        args.cb = True
        args.a37 = True
    #print args

    main(args)

