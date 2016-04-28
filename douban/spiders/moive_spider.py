# coding=utf-8
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose
from scrapy.loader.processors import MapCompose

from douban.items import MovieItem


class MovieTop250Spider(CrawlSpider):
    name = "MovieTop250"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250"]
    rules = [
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/top250\?start=\d+.*', ))),
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+', )), callback="parse_movie"),
    ]

    """
    def make_requests_from_url(self, url):
        return request(
            url,
            dont_filter=true,
            headers={
                "host": "movie.douban.com",
                "user-agent": "mozilla/5.0 (macintosh; intel mac os x 10.11; rv:47.0) gecko/20100101 firefox/47.0",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "accept-language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
                "accept-encoding": "gzip, deflate, br",
                "connection": "keep-alive"
            }
        )
    """

    def parse_movie(self, response):
        self.logger.info('Parse item\'s url %s.', response.url)
        l = ItemLoader(item=MovieItem(), response=response)
        l.add_xpath('name', '//span[@property="v:itemreviewed"]/text()')
        l.add_xpath(
            'name',
            u'//div[@id="info"]/span[@class="pl"][contains(./text(), "又名:")]/following::text()[1]',
            MapCompose(lambda s: s.split('/'), unicode.strip)
        )
        l.add_css('year', '.year::text', re=r'\((\d+)\)')
        l.add_css('rating', '.rating_num::text')
        l.add_xpath('director', '//a[@rel="v:directedBy"]/text()')
        l.add_xpath('director_id', '//a[@rel="v:directedBy"]/@href', re=r'/.*?/(\d+)/')
        l.add_xpath('director_href', '//a[@rel="v:directedBy"]/@href')
        l.add_xpath('script_editor', '(//div[@id="info"]/*/span[@class="attrs"]/a)[2]/text()')
        l.add_xpath('script_editor_id', '(//div[@id="info"]/*/span[@class="attrs"]/a)[2]/@href', re=r'/.*?/(\d+)/')
        l.add_xpath('script_editor_href', '(//div[@id="info"]/*/span[@class="attrs"]/a)[2]/@href')
        l.add_xpath('genre', '//span[@property="v:genre"]/text()')
        l.add_xpath('runtime', '//span[@property="v:runtime"]/text()')
        l.add_xpath('starring', '//a[@rel="v:starring"]/text()')
        l.add_xpath('starring_id', '//a[@rel="v:starring"]/@href', re=r'/.*?/(\d+)/')
        l.add_xpath('starring_href', '//a[@rel="v:starring"]/@href')
        l.add_xpath('initialReleaseDate', '//span[@property="v:initialReleaseDate"]/text()')
        l.add_xpath(
            'region',
            u'//div[@id="info"]/span[@class="pl"][contains(./text(), "制片国家/地区:")]/following::text()[1]',
            MapCompose(lambda s: s.strip())
        )
        l.add_xpath(
            'language',
            u'//div[@id="info"]/span[@class="pl"][contains(./text(), "语言:")]/following::text()[1]',
            MapCompose(unicode.strip)
        )
        yield l.load_item()
