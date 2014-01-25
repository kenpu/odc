from bs4 import BeautifulSoup
import requests
import re
from time import time, sleep

TOPURL = "http://data.gc.ca/data/en/dataset"

def pageSoup(i, output, delay=1.0):
    start = time()
    sleep(delay)
    url = "%s?page=%d" % (TOPURL, i)
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    dirDatasetAnchors(soup, output)
    return soup, time()-start

def dirDatasetAnchors(soup, output):
    for a in soup.find_all('a', href=re.compile(r'/data/en/dataset/[a-z0-9-]+')):
        print >>output, a.get('href')
        output.flush()

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

with open('output', 'w') as output:

    (soup, t) = pageSoup(1, output=output, delay=0.0)
    print "Page 1 took: %.2f seconds" % t
    N = maxPage(soup)


    for i in range(2,N+1):
        soup, t = pageSoup(i, output=output, delay=1.0)
        print "Page %d took: %.2f seconds" % (i, t)
        print "estimated total index time: %.2f hr" % (t*N/60.0/60.0)

