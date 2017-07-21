# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup as bs
import urllib.parse
from AppleCrawler.spiders.utils import get_start_urls, host_url

class AppleSpider(scrapy.Spider):
    name = "apple"
    # get all archive pages of a specific date range
    start_urls = get_start_urls()

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
