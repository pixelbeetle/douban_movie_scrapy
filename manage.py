#!/usr/bin/env python
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from douban.spiders.moive_spider import MovieSpider


process = CrawlerProcess(get_project_settings())
process.crawl(MovieSpider)

# Start process
process.start()

