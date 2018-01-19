# -*- coding: utf-8 -*-

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

    driver = webdriver.Chrome(args.driver)
    
    driver.implicitly_wait(60)
    driver.set_page_load_timeout(60)

    for line in open("passwords.txt"):
        if line.strip() == "": continue
        kitnum,password = line.split()
        if not args.kit or kitnum == args.kit:
            download(args,driver,kitnum,password)

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
            print "[%s s] Waiting for %s" % (i,fname)
            time.sleep(5)
            i += 5
        print "Done:", fname
    
    def download_ff():
        print "Downloading,", ff_fname
        driver.get("https://www.familytreedna.com/my/familyfinder/")
        click("#download-csv")
        wait(ff_fname)
    
    def download_cb():
        print "Downloading,", cb_fname
        driver.get("https://www.familytreedna.com/my/family-finder/chromosome-browser")
        click("#dwnLdAllExcel")
        wait(cb_fname)

    def download_a37():
        print "Downloading,", a37_fname
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
            print "Already exists:", ff_fname
        else:
            download_ff()
    
    if args.cb:
        cb_fname = dirname+"{}_Chromosome_Browser_Results_{}.csv".format(kitnum,date)
        if os.path.exists(cb_fname):
            print "Already exists:", cb_fname
        else:
            download_cb()

    if args.a37:
        a37_fname = dirname+"{}_Autosomal_o37_Results_{}.csv.gz".format(kitnum,date)
        if os.path.exists(a37_fname):
            print "Already exists:", a37_fname
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
    parser.add_argument("--37x",action="store_true",default=False,dest="x37")
    parser.add_argument("--passwords",default="passwords.txt")
    parser.add_argument("--driver",default="./chromedriver")
    parser.add_argument("--downloads-folder",default="$HOME/Downloads")
    parser.add_argument("--quiet",action="store_true",default=False)
    args = parser.parse_args()
    if args.ff: args.all = False
    if args.cb: args.all = False
    if args.a37: args.all = False
    if args.x37: args.all = False
    if args.all:
        args.ff = True
        args.cb = True
        args.a37 = True
        args.x37 = True
    #print args

    main(args)

