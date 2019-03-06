#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Saturday 03/02/2019
@author: fanshehu
'''

import ssl
from http import client
from urllib import request
from urllib import parse
from urllib import error
from PriorityQueue import PriorityQueue
from bs4 import BeautifulSoup

class Crawler:
    '''
    Give a query and the crawler will crawl the web using OPIC strategy.
    And output a file with all crawled URLs, in the order they are visited. 
    '''
    
    def __init__(self, query):
        # a set of keywords
        self.query = query
        # total pages to be crawled
        self.num_to_crawl = 20
        # number of pages have been crawled
        self.num_crawled = 0
        # pages to be crawled with its pagerank score, stored in priorityqueue
        self.urls = PriorityQueue()
        # starting pages
        self.url_seeds = []
        # a set that stores visited URLs
        self.url_visited = set()
        # HTTP request headers
        self.headers = {'User-Agent':'Mozilla/5.0'}
        # illeaga endings that may cause ambiguity
        self.illegal_endings = ["index.htm", "index.html", "index.jsp", "main.html"]
        self.search_google()
        self.opic_init()
    
    '''
    A method that contacts to Google and gets the top-10 result for query as starting pages.
    '''
    def search_google(self):
        query = '+'.join(self.query.strip().split(' '))
        url = "https://www.google.com/search?q=" + query + "&start=1"
        req = request.Request(url = url, headers = self.headers)
        html = request.urlopen(req).read()
        soup = BeautifulSoup(html, "html.parser")
        for cite in soup.findAll("cite"):
            url = cite.text
            if not self.is_illegal_format(url):
                self.url_seeds.append(url)
    
    '''
    A method that checks if the url has been visited.
    '''
    def has_visited(self, url):
        if url in self.url_visited:
            return True
        self.url_visited.add(url)
        return False
    
    '''
    A method that checks if the url has illegal format.
    '''
    def is_illegal_format(self, url):
        parse_res = parse.urlparse(url)
        if not parse_res.scheme:
            return True
        path = parse_res.path
        for ending in self.illegal_endings:
            if path.endswith(ending, 0, len(path)):
                return True
        return False
    
    '''
    OPIC initial method:
        assign each starting page the same cash.
        cash sum is 1.
    '''
    def opic_init(self):
        n = len(self.url_seeds)
        for url in self.url_seeds:
            self.urls.put((1/n, url))
    
    '''
    A method that parses HTML and extract links in it.
    '''
    def parse_html(self, file, cash):
        html = file.read()
        soup = BeautifulSoup(html, "html.parser")
        next_urls = set()
        for tag in soup.find_all("a"):
            link = tag.get("href")
            if self.is_illegal_format(link):
                continue
            next_urls.add(link)
            # maximum links can be extract from a page
            if len(next_urls) >= 10:
                break
        # OPIC
        # divide cash of current page and assign them equally to its children pages
        n = len(next_urls)
        for url in next_urls:
            self.urls.put((cash/n, url))
    
    '''
    A method that crawls the web based on OPIC priority.
    '''
    def crawl(self):
        while self.num_crawled < self.num_to_crawl and not self.urls.is_empty():
            cash, url = self.urls.pop()
            '''
            url去重，如有时间，可以考虑实现bloom filter
            '''
            if self.has_visited(url):
                continue
            try:
                req = request.Request(url = url, headers = self.headers)
                file = request.urlopen(req)
                # illegal MIME type
                if not file.info().get_content_type() == 'text/html':
                    continue
                # HTTP status code
                if file.getcode() != 200:
                    continue
                '''
                可以添加的操作：
                1. 把当前page下载
                2. 把访问记录写入本地文件
                '''
                print (str(self.num_crawled + 1) + " " +url + " " + str(cash))
                self.parse_html(file, cash)
                self.num_crawled += 1
            except error.HTTPError:
                continue
            except error.URLError:
                continue
            except ssl.CertificateError:
                continue
            except client.HTTPException:
                continue
            except KeyboardInterrupt:
                print ("Program stopped by user.")
                break
     
        
def main():
    query = input("What is your query:  ")
    my_crawler = Crawler(query)
    my_crawler.crawl()

if __name__ == "__main__":
    main()
    