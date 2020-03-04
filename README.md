# Scrapy-Craigslist
Web Scraping Craigslist Healthcare Jobs in LA with Scrapy

link: https://losangeles.craigslist.org/search/hea

## Install Scrapy

You can install Scrapy using pip on terminal with this command:
```shell
$ sudo pip install scrapy
```

## Create Scrapy Project
Run the following command in your project folder:
```shell
$ scrapy startproject craigslist
```
The project name can be anything; In this case, we named it: "craigslist".

## Create Scrapy Spider
In your Terminal, navigate it to Scrapy project folder (**craigslist**).
```shell
$ cd craigslist
```
Next, create the spider using **genspider** command and give it any name you like. In this case we named it: **jobs**. Then, it should be followed by the URL.
 ```shell
$ scrapy genspider jobs https://losangeles.craigslist.org/search/hea
```

## Edit Scrapy Spider
Open spider file **jobs.py**. Edit **start_urls** if there is any wrong URL, because Scrapy adds extra http://.
```python
# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['https://losangeles.craigslist.org/search/hea']
    start_urls = ['https://losangeles.craigslist.org/search/hea/']

    def parse(self, response):
        pass

```

## Scrapy Spider #1 – Titles
```python
titles = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
```
### Run Scrapy Spider
Run the spider using the following command in your Scrapy project **craigslist**.
```shell
$ scrapy crawl jobs
```
### Store the Scraped Data to CSV
Run your spider and store the output data into CSV, JSON or XML. To store the data into CSV, run the following command:
```shell
$ scrapy crawl jobs -o result-titles.csv
```
