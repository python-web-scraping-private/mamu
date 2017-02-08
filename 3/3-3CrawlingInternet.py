from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random


pages = set()
random.seed(datetime.datetime.now())


def getInternalLinks(bsObj, includeUrl):
    includeUrl = urlparse(includeUrl).scheme + "://" + urlparse(includeUrl).netloc
    internalLinks = []
    for link in bsObj.findAll("a", href=re.compile("^(\/|.*" + includeUrl + ")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if link.attrs['href'].startswith("/"):
                    internalLinks.append(includeUrl + link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks


def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    for link in bsObj.findAll("a", href=re.compile("^(http|www)((?!" + excludeUrl + ").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks


def getRandomExternalLink(startingPage):
    try:
        html = urlopen(startingPage)
    except HTTPError as e:
        raise ValueError(e)
    else:
        bsObj = BeautifulSoup(html, "lxml")
        externalLinks = getExternalLinks(bsObj, urlparse(startingPage).netloc)
        if len(externalLinks) == 0:
            print("No external links")
            domain = (urlparse(startingPage).scheme + "://" + urlparse(startingPage).netloc)
            internalLinks = getInternalLinks(bsObj, startingPage)
            if len(internalLinks) == 0:
                raise ValueError("No internal links")
            else:
                return getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks)-1)])
        else:
            return externalLinks[random.randint(0, len(externalLinks)-1)]


def followExternalOnly(startingSite):
    try:
        externalLink = getRandomExternalLink(startingSite)
    except ValueError as e:
        print(e)
        print("Crawling is end")
    else:
        print("Random external link is : " + externalLink)
        followExternalOnly(externalLink)


def getAllExternalLinks(siteUrl, start):
    allExtLinks = set()
    allIntLinks = set(start)
    def getAllExternalLinks_sub(siteUrl):
        nonlocal allExtLinks
        nonlocal allIntLinks
        html = urlopen(siteUrl)
        domain = urlparse(siteUrl).scheme + "://" + urlparse(siteUrl).netloc
        bsObj = BeautifulSoup(html, "lxml")
        internalLinks = getInternalLinks(bsObj, domain)
        externalLinks = getExternalLinks(bsObj, domain)
        for link in externalLinks:
            if link not in allExtLinks:
                allExtLinks.add(link)
                print(link)
        for link in internalLinks:
            if link not in allIntLinks:
                allIntLinks.add(link)
                getAllExternalLinks_sub(link)
    getAllExternalLinks_sub(siteUrl)


followExternalOnly("http://oreilly.com")
print("")
getAllExternalLinks("http://oreilly.com", "http://oreilly.com")
