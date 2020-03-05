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
Open spider file **jobs.py**.
Edit **start_urls** if there is any wrong URL, because Scrapy adds extra http://.
Edit **allowed_domains** too.
```python
# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['losangeles.craigslist.org']
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
    allowed_domains = ['losangeles.craigslist.org']
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

### Extract Job Titles, Address, URL, Date
```python
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

    yield {'URL': absolute_url,
           'Date': date,
           'Title': title,
           'Address': address}
```

### Run Spider and Store Data
Run your spider and store the output data into CSV, JSON or XML. To store the data into CSV, run the following command:
```shell
$ scrapy crawl jobs -o result-jobs-one-page.csv
```

## Scrapy Spider #3 – Multiple Pages
You need to extract the “next” (next page) URLs and then apply the same parse() function on them.
 
### Extract Next URLs
Outside the loop, add "next page" url.
```python
relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
absolute_next_url = response.urljoin(relative_next_url)

yield scrapy.Request(absolute_next_url, callback=self.parse)
```

### Run Spider and Store Data
```shell
$ scrapy crawl jobs -o result-jobs-multi-pages.csv
```

## Scrapy Spider #4 – Job Descriptions
The spider will open each job URL and scrape its description.

### Pass the Data to a Second Function
Change the **yield** data in parse() function with this code:
```python
yield scrapy.Request(absolute_url,
                     callback=self.parse_page,
                     meta={'URL': absolute_url,
                           'Date': date,
                           'Title': title,
                           'Address': address})

```

### Create Function to Extract Specific Data
Add parse_page() function and extract description, compensation, employment. If data is empty, we will fill it with 'N/A' string.
```python
def parse_page(self, response):
    url = response.meta['URL']
    date = response.meta['Date']
    title = response.meta['Title']
    address = response.meta['Address']
    description = "".join(line.rstrip("\n") for line in response.xpath('//*[@id="postingbody"]/text()').extract()).strip() or 'N/A'
    compensation = response.xpath('//p[@class="attrgroup"]/span/b/text()')[0].extract() or 'N/A'
    employment_type = response.xpath('//p[@class="attrgroup"]/span/b/text()')[1].extract() or 'N/A'

    yield {'URL': url,
           'Date': date,
           'Title': title,
           'Address': address,
           'Description': description,
           'Compensation': compensation,
           'Employment': employment_type}
```

### Run Spider and Store Scrapy Output Data to CSV, XML or JSON
```shell
$ scrapy crawl jobs -o result-jobs-multi-pages-content.csv
```
```shell
$ scrapy crawl jobs -o result-jobs-multi-pages-content.xml
```
```shell
$ scrapy crawl jobs -o result-jobs-multi-pages-content.json
```