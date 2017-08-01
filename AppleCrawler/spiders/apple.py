# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs
import urllib.parse
import datetime
from AppleCrawler.spiders.utils import daterange

archive_url = 'http://www.appledaily.com.tw/appledaily/archive/{}'
host_url = 'http://www.appledaily.com.tw'

def get_start_urls():
    date_strings = []
    start_date = datetime.date(2017, 1, 1)
    end_date = datetime.date(2017, 1, 2)
    for single_date in daterange(start_date, end_date):
        date_strings.append(single_date.strftime("%Y%m%d"))
    urls = []
    for date_str in date_strings:
        urls.append(archive_url.format(date_str))
    return urls

class AppleSpider(scrapy.Spider):
    name = "apple"
    # get all archive pages of a specific date range
    start_urls = get_start_urls()
    post_path = 'data/apple.json'
    lines_path = 'data/apple.json.lines'

    def parse(self, response):
        soup = bs(response.body, 'lxml')
        # get all the links in the archive page
        links = [link['href'] for link in soup.select('ul.fillup a')]
        for link in links:
            url = link
            if 'appledaily.com.tw' not in link:
                url = host_url + url
            yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        soup = bs(response.body, 'lxml')
        title = soup.select('header h1#h1')[0].text
        date = soup.select('time')[0]['datetime']
        url = response.url

        # clean script tags
        [e.extract() for e in soup.select('.articulum.trans script')]

        text = soup.select('.articulum.trans')[0].text

        yield {'title': title, 'date': date, 'url': url, 'text': text}
