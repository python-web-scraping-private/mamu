from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pymysql

conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock',
                       user='root', passwd='fortgn000', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE wikipedia")


def insertPageIfNotExist(url):
    cur.execute("SELECT * FROM pages WHERE url = %s", (url))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO pages (url) VALUES (%s)", (url))
        conn.commit()
        return cur.lastrowid
    else:
        return cur.fetchone()[0]


def insertLink(fromPageId, toPageId):
    cur.execute("SELECT * FROM links WHERE fromPageId = %s AND toPageId = %s", (int(fromPageId), int(toPageId)))
    if cur.rowcount == 0:
        cur.execute("INSERT INTO links (fromPageId, toPageId) VALUES (%s, %s)", (int(fromPageId), int(toPageId)))
        conn.commit()


page = set()
def getLinks(pageUrl, recursionLevel):
    global page
    if recursionLevel > 4:
        return
    pageId = insertPageIfNotExist(pageUrl)
    html = urlopen("http://en.wikipedia.org" + pageUrl)
    bsObj = BeautifulSoup(html, 'lxml')
    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        insertLink(pageId, insertPageIfNotExist(link.attrs['href']))
        if link.attrs['href'] not in page:
            newPage = link.attrs['href']
            page.add(newPage)
            getLinks(newPage, recursionLevel+1)


getLinks("/wiki/Kevin_Bacon", 0)
cur.close()
conn.close()