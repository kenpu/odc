import requests
import re
import os
import sys
from bs4 import BeautifulSoup
from time import time, sleep

SITE = "http://data.gc.ca"
index_file = "download/index.txt"
totalDatasets = 0
csvPattern = re.compile(r'\S+\.csv$')
downloadPattern = re.compile(r'Download')

def resolveUrl(url, href):

    if href.startswith("/"):
        url2 = SITE + href
    elif href.startswith("http"):
        url2 = href
    else:
        url2 = url[:url.rindex("/")] + "/" + href

    if href.endswith(".csv"):
        path = href.split("/")
        lang = "FR" if href.endswith("_FR.csv") else "EN"
        dataset = lang + "__" + "__".join(path[-2:])
    else:
        dataset = None

    return (dataset, url2)

#
# scan for csv.  If there is any, download.
#
def downloadDatasets(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    download_a = list(soup.find_all("a", text=downloadPattern))
    for a in download_a:
        href = a.get('href')
        dataset, url2 = resolveUrl(url, href)
        if dataset:
            save(dataset, url2)
        else: # download an index page of a few data sets
            downloadCsvset(url2)
            
def downloadCsvset(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    for a in soup.find_all("a", href=lambda x: x.endswith(".csv")):
        href = a.get('href')
        dataset, url2 = resolveUrl(url, href)
        save(dataset, url2)

def save(dataset, url):
    if dataset:
        print "[%s] %s" % (dataset, url)
        with open("download/%s" % dataset, "w") as out:
            r = requests.get(url)
            if r.text:
                out.write(r.text.encode('utf8', 'ignore'))
#
# count the lines
#
with open(index_file, "r") as index:
    for _ in index.xreadlines():
        totalDatasets += 1

with open(index_file, "r") as index:
    prefix = "/data/en/dataset/"
    n = len(prefix)

    for line in index.xreadlines():
        path = line.strip()
        url = SITE + path
        downloadDatasets(url)
        break
