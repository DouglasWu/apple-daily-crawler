# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs
import urllib.parse
import datetime
from AppleCrawler.spiders.utils import daterange

host_url = 'http://www.chinatimes.com';
archive_url = 'http://www.chinatimes.com/history-by-date/{}-260{}?page={}'

def get_start_urls():
    date_strings = []
    start_date = datetime.date(2017, 1, 1)
    end_date = datetime.date(2017, 8, 1)
    for single_date in daterange(start_date, end_date):
        date_strings.append(single_date.strftime("%Y-%m-%d"))
    urls = []
    for date_str in date_strings:
        for aid in range(1,5):
            urls.append(archive_url.format(date_str, aid, 1))
    return urls

class ChinaTimesSpider(scrapy.Spider):
    name = "chinatimes"
    # get all archive pages of a specific date range
    start_urls = get_start_urls()
    post_path = 'data/chinatimes.json'
    lines_path = 'data/chinatimes.json.lines'

    def parse(self, response):
        soup = bs(response.body, 'lxml')
        # get all the links in the archive page
        links = [host_url+link['href'] for link in soup.select('.listRight li h2 a')]
        for link in links:
            yield scrapy.Request(link, callback=self.parse_page)

        cur_page = int(response.url.split('=')[1])
        total_page = int(soup.select('.pagination li a')[-1]['href'].split('=')[1])
        if cur_page < total_page:
            next_page_url = response.url.split('=')[0] + '=' + str(cur_page + 1)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_page(self, response):
        soup = bs(response.body, 'lxml')
        title = soup.select('article header h1')[0].text
        date = soup.select('.reporter time')[0]['datetime'].split()[0]
        url = response.url
        text = ''.join([p.text for p in soup.select('article p')])

        yield {'title': title, 'date': date, 'url': url, 'text': text}