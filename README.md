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
This is basic Scrapy spider in file jobs.py:
```python
# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['https://losangeles.craigslist.org/search/hea']
    start_urls = ['https://losangeles.craigslist.org/search/hea/']

    def parse(self, response):
        titles = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
        for title in titles:
            yield {'Title': title}
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

## Scrapy Spider #2 – One Page
If you want to scrape several details about each job,you need scrape the whole “wrapper” of each job including all the information you need.

### Extract All Wrappers
Under the parse() function in jobs.py, write the following code:
```python
jobs = response.xpath('//p[@class="result-info"]')
```

### Extract Job Titles, Address, URL
```python
for job in jobs:
    title = job.xpath('a/text()').extract_first()
    address = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]
    relative_url = job.xpath('a/@href').extract_first()
    absolute_url = response.urljoin(relative_url)

    yield {'URL': absolute_url, 'Title': title, 'Address': address}
```

### Run spider and store data
Run your spider and store the output data into CSV, JSON or XML. To store the data into CSV, run the following command:
```shell
$ scrapy crawl jobs -o result-jobs-one-page.csv