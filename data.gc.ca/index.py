from bs4 import BeautifulSoup
import requests
import re
from time import time

TOPURL = "http://data.gc.ca/data/en/dataset"

def pageSoup(i):
    start = time()
    url = "%s?page=%d" % (TOPURL, i)
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    return soup, time()-start

def dirDatasetAnchors(soup):
    return soup.find_all('a', 
        href=re.compile(r'/data/en/dataset/[a-z0-9-]+'))

def maxPage(soup):
    pattern = re.compile(r'\?page=(\d+)')
    maxnum = 0
    for a in soup.find_all('a', href=pattern):
        href = a.get('href')
        m = pattern.search(href)
        pagenum = int(m.group(1))
        maxnum = max(maxnum, pagenum)
    return maxnum

print "Starting..."
(soup, t) = pageSoup(1)
print "Page 1 took: %.2f seconds" % t
N = maxPage(soup)

for i in range(2,N+1):
    soup, t = pageSoup(i)
    print "Page %d took: %.2f seconds" % (i, t)
    print "estimated total index time: %.2f hr" % (t*N/60.0/60.0)
