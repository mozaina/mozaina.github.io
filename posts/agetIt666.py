# coding:utf-8

import datetime
import codecs
import requests
import os
import time
import re
from pyquery import PyQuery as pq
import html2text as ht


import sys

text_maker = ht.HTML2Text()

def git_add_commit_push(date, filename):
    cmd_git_add = 'git add {filename}'.format(filename=filename)
    cmd_git_commit = 'git commit -m "{date}"'.format(date=date)
    cmd_git_push = 'git push -u origin master'

    os.system(cmd_git_add)
    os.system(cmd_git_commit)
    os.system(cmd_git_push)


def createMarkdown(title, tag):
    with open(title+'.md', 'w') as f:
        date=datetime.datetime.now().strftime('%Y-%m-%d')
        f.write(wrapHexoTitile(title,date,tag))




def scrape(page,tag):

    HEADERS = {
        'User-Agent'		: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Accept'			: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding'	: 'gzip,deflate,sdch',
        'Accept-Language'	: 'zh-CN,zh;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    url = 'https://www.it610.com/search/{tag}/{page}.htm'.format(page=page,tag=tag)
    r = requests.get(url, headers=HEADERS)
    print(url)
    print(r.status_code)
    # assert r.status_code == 200
    print(page)



    d = pq(r.content)

    items = d("div.news__item-info")

    for item in items:
        i = pq(item)
        titleUrl=i("a").attr("href")

        #访问文章内容
        titleUrl="https://www.it610.com/"+titleUrl
        r = requests.get(titleUrl, headers=HEADERS)
        # assert r.status_code == 200
        d = pq(r.content)
        #中文标题
        zhTitle=washTitile(d("h1#articleTitle").text().replace(" ",""))
        if len(zhTitle)>100:
            zhTitle=zhTitle[0:100]

        #创建markdown文件
        createMarkdown(zhTitle,tag)
        print("标题"+zhTitle)

        #追加写入
        # codecs to solve the problem utf-8 codec like chinese
        with codecs.open(zhTitle+'.md', "a", "utf-8") as f:
             html=d("div#content_views").html()
             media=d("div#js_content").html()
             if  not html is None:
                 # dat=ht.html2text(html)
                 # print(html)
                 f.write(ht.html2text(html)+'\n')
                #问题
                # print("标题"+d("div#idarticle_content").text())
             elif  not media is None:
                 f.write(ht.html2text(media)+'\n')












def wrapH4(title):
    return '\n#### {title}\n'.format(title=title)

def wrapH1(title):
    return '\n# {title}\n'.format(title=title)

def wrapH3(title):
    return '\n### {title}\n'.format(title=title)

def wrapH2(title):
    return '\n## {title}\n'.format(title=title)
def wrapCode(code):
    return '\n```\n {code}\n```\n'.format(code=code)

def wrapHexoTitile(title,date,tags):
    return '---\n title: {title}\n date: {date}\n tags: [\"{tags}\"]\n---\n'.format(title=title,date=date,tags=tags)
def wrapLink(title,link):
    return '\n[{title}]({link})\n'.format(title=title,link=link)

def wrapImage(url):
    return '\n![]({url})\n'.format(url=url)
def wrapBold(text):
    return '**{text}**'.format(text=text)
def wrapRaw(content):
    return '{% raw %}\n'+'{content}'.format(content=content)+'\n{% endraw %}\n'

#去除特殊字符 只保留汉字 字母 和数字
def washTitile(title):
    return re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])","",title)


tags=['xml','session','node.js','mysql','spring','ajax','c#','windows']

def job():

    strdate = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = '{date}.md'.format(date=strdate)

    # create markdown file
    # createMarkdown("strdate", filename)

    # write markdown
    #scrape('1')

    for i in range(0,1972):#34509
        scrape(i,"shell")
    #scrape('swift', filename)
    #scrape('javascript', filename)
    #scrape('go', filename)

    # git add commit push
    # git_add_commit_push(strdate, filename)


if __name__ == '__main__':
    job()
