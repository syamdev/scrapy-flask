# -*- coding: utf-8 -*-
import scrapy
from craigslist.items import CraigslistItem


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['losangeles.craigslist.org']
    start_urls = ['https://losangeles.craigslist.org/search/ant/hea']

    def parse(self, response):
        jobs = response.xpath('//p[@class="result-info"]')

        for job in jobs:
            title = job.xpath('a/text()').extract_first()
            address = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first()
            if not address:
                address = 'N/A'
            else:
                address = address[2:-1]
            date = job.xpath('time[@class="result-date"]/@datetime').extract_first()
            relative_url = job.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)

            yield scrapy.Request(absolute_url,
                                 callback=self.parse_page,
                                 meta={'URL': absolute_url,
                                       'Date': date,
                                       'Title': title,
                                       'Address': address})

        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)

        yield scrapy.Request(absolute_next_url, callback=self.parse)

    def parse_page(self, response):
        url = response.meta['URL']
        date = response.meta['Date']
        title = response.meta['Title']
        address = response.meta['Address']
        #description = "".join(line.rstrip("\n") for line in response.xpath('//*[@id="postingbody"]/text()').extract()).strip() or 'N/A'
        compensation = response.xpath('//span[contains(text(), "compensation")]/b/text()').extract_first() or 'N/A'
        employment_type = response.xpath('//span[contains(text(), "employment type")]/b/text()').extract_first() or 'N/A'

        item = CraigslistItem()
        item['url'] = url
        item['date'] = date
        item['title'] = title
        item['address'] = address
        #item['description'] = description
        item['compensation'] = compensation
        item['employment_type'] = employment_type
        return item
