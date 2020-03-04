# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['losangeles.craigslist.org']
    start_urls = ['https://losangeles.craigslist.org/search/hea/']

    def parse(self, response):
        jobs = response.xpath('//p[@class="result-info"]')

        for job in jobs:
            title = job.xpath('a/text()').extract_first()
            address = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]
            date = job.xpath('time[@class="result-date"]/@datetime').extract_first()
            relative_url = job.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)

            yield {'URL': absolute_url,
                   'Date': date,
                   'Title': title,
                   'Address': address}

        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)

        yield scrapy.Request(absolute_next_url, callback=self.parse)
