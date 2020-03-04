# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['https://losangeles.craigslist.org/search/hea']
    start_urls = ['https://losangeles.craigslist.org/search/hea/']

    def parse(self, response):
        jobs = response.xpath('//p[@class="result-info"]')

        for job in jobs:
            title = job.xpath('a/text()').extract_first()
            address = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]
            relative_url = job.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)

            yield {'URL': absolute_url, 'Title': title, 'Address': address}
