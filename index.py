#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 12:55:36 2018

@author: greg
"""

import pandas;
import requests;
import os.path;

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

bucketURL = "https://s3.amazonaws.com/tripdata/"
indexURL = bucketURL + "index.html";
refreshTripData = False;
## Get the page source for debugging
#indexReq = requests.get("https://s3.amazonaws.com/tripdata/index.html");
#print (indexReq.content);

## Load from selenium to allow async table to load
tripIndexFile = "trip_index.html";
if refreshTripData:
    try:
        driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
        driver.get(indexURL)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*/table/tbody/tr")))
        table = driver.find_element_by_xpath('//*/table');
        table_html = table.get_attribute('outerHTML');
        f = open(tripIndexFile, "w");
        f.write(table_html);
        f.close()
    finally:
        driver.quit();
else:
    #read from file
    f = open(tripIndexFile, "r");
    table_html = f.read();
    f.close();

df = pandas.read_html(table_html)[0];
zips = df[df["Type"] == "ZIP file"];

tripFileDir = "trip_data/"
if not os.path.isdir(tripFileDir):
    os.mkdir(tripFileDir);
for i, col in zips.iterrows():
    if i > 3:
        continue;
    tripFileName = tripFileDir + col["Name"] + "_" + col["Date Modified"] + ".zip";
    if not os.path.isfile(tripFileName):
        
        tripCSVURL = bucketURL + col["Name"];
        print("downloading " + tripFileName + " (" + col["Size"] + " ) from " + tripCSVURL)
        tripDataZIP = requests.get(tripCSVURL)
        with open(tripFileName, "wb") as code:
            code.write(tripDataZIP.content);
#        f = open(tripFileName, "w");
#        f.write(tripDataZIP);
#        f.close();
#    if os.path.isfile(tripFileDir & col["Name"])
