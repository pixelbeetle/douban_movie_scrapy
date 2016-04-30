# coding=utf-8
import json
import threading
from datetime import datetime
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join
from scrapy.loader.processors import MapCompose
from scrapy.http import Request

from douban.items.movie_item import MovieItem


class MovieSpider(CrawlSpider):
    name = "movie"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/"]
    rules = [
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/top250\?start=\d+.*', ))),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+', )), callback="parse_movie"),
    ]
    lock = threading.Lock()
    parse_search_semaphore = threading.Semaphore(5)

    handle_httpstatus_list = [403, ]

    def __init__(self, *a, **kw):
        self.tag_urls_pool = {}
        self.page_limit = 20
        super(MovieSpider, self).__init__(*a, **kw)

    def parse_start_url(self, response):
        if response.status == 403:
            yield Request(url=response.url)
        yield Request(url='https://movie.douban.com/j/search_tags?type=movie', callback=self.parse_search_tags)

    def parse_search_tags(self, response):
        tags = json.loads(response.body)['tags']
        with self.lock:
            for tag in tags:
                tag = tag.strip()
                self.tag_urls_pool.update({
                    tag: {
                        'page_start': 0,
                        'page_limit': self.page_limit,
                        'all_done': False
                    }
                })
        for tag in tags:
            while True:
                if self.tag_urls_pool[tag]['all_done']:
                    break
                with self.lock:
                    page_start = self.tag_urls_pool[tag]['page_start']
                    page_limit = self.tag_urls_pool[tag]['page_limit']
                    self.tag_urls_pool[tag]['page_start'] = page_start + page_limit
                yield Request(
                    url='https://movie.douban.com/j/search_subjects?type=movie&tag='+tag+'&sort=recommend&page_limit=' +
                        str(page_limit)+'&page_start='+str(page_start)+'',
                    meta={'tag': tag},
                    callback=self.parse_movie_urls
                )

    def parse_movie_urls(self, response):
        json_data = json.loads(response.body)['subjects']
        if not len(json_data):
            tag = response.meta['tag']
            if self.tag_urls_pool[tag]['all_done']:
                return
            with self.lock:
                self.tag_urls_pool[tag]['all_done'] = True
            return
        for item in json_data:
            yield Request(
                url=item['url'],
                callback=self.parse_movie
            )

    def parse_movie(self, response):
        self.logger.info('Parse item\'s url %s.', response.url)
        l = ItemLoader(item=MovieItem(), response=response)
        l.add_value('id', response.url, re=r'/.*?/(\d+)/')
        l.add_xpath('name', '//span[@property="v:itemreviewed"]/text()')
        l.add_xpath('poster', u'//img[@title="点击看更多海报" and @rel="v:image"]/@src')
        l.add_xpath(
            'alternate_name',
            u'//div[@id="info"]/span[@class="pl"][contains(./text(), "又名:")]/following::text()[1]',
            MapCompose(lambda s: s.split('/'), unicode.strip)
        )
        l.add_css('year', '.year::text', re=r'\((\d+)\)')
        l.add_css('rating', '.rating_num::text')
        l.add_xpath('rating_per', '//span[@class="rating_per"]/text()')
        l.add_xpath('rating_betterthan', '//div[@class="rating_betterthan"]/a/text()')
        l.add_xpath('rating_betterthan_href', '//div[@class="rating_betterthan"]/a/@href')
        l.add_xpath('director', '//a[@rel="v:directedBy"]/text()')
        l.add_xpath('director_id', '//a[@rel="v:directedBy"]/@href', re=r'/.*?/(\d+)/')
        l.add_xpath('script_editor', '(//div[@id="info"]//span[@class="attrs"]/a)[2]/text()')
        l.add_xpath('script_editor_id', '(//div[@id="info"]//span[@class="attrs"]/a)[2]/@href', re=r'/.*?/(\d+)/')
        l.add_xpath('genre', '//span[@property="v:genre"]/text()')
        l.add_xpath('tags', '//div[@class="tags-body"]/a/text()')
        l.add_xpath(
            'summary',
            '//span[@property="v:summary"]/text()',
            MapCompose(unicode.strip), Join('<br>')
        )
        l.add_xpath('runtime', '//span[@property="v:runtime"]/text()')
        l.add_xpath('starring', '//a[@rel="v:starring"]/text()')
        l.add_xpath('starring_id', '//a[@rel="v:starring"]/@href', re=r'/.*?/(\d+)/')
        l.add_xpath('initialReleaseDate', '//span[@property="v:initialReleaseDate"]/text()')
        l.add_xpath(
            'region',
            u'//div[@id="info"]/span[@class="pl"][contains(./text(), "制片国家/地区:")]/following::text()[1]',
            MapCompose(unicode.strip)
        )
        l.add_xpath(
            'language',
            u'//div[@id="info"]/span[@class="pl"][contains(./text(), "语言:")]/following::text()[1]',
            MapCompose(unicode.strip)
        )
        l.add_xpath(
            'imdb',
            u'//div[@id="info"]/span[@class="pl"][contains(./text(), "IMDb链接:")]/following::a[1]/text()'
        )
        l.add_xpath(
            'imdb_href',
            u'//div[@id="info"]/span[@class="pl"][contains(./text(), "IMDb链接:")]/following::a[1]/@href'
        )
        l.add_xpath('recommendations_id', '//div[@class="recommendations-bd"]/dl/dd/a/@href', re=r'/.*?/(\d+)/')
        l.add_xpath('recommendations', '//div[@class="recommendations-bd"]/dl/dd/a/text()')
        l.add_value(
            'collections_number',
            '//div[@class="subject-others-interests-ft"]/a[1]/text()',
            re=r'(\d+)'
        )
        l.add_value(
            'wishes_number',
            '//div[@class="subject-others-interests-ft"]/a[2]/text()',
            re=r'(\d+)'
        )
        l.add_value('last_update_time', str(datetime.utcnow()))
        # download poster image file
        l.add_xpath('image_urls', u'//img[@title="点击看更多海报" and @rel="v:image"]/@src')
        yield l.load_item()
