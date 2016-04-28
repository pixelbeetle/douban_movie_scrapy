# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    name = scrapy.Field()
    alternate_name = scrapy.Field()
    year = scrapy.Field()
    rating = scrapy.Field()
    director = scrapy.Field()
    director_id = scrapy.Field()
    director_href = scrapy.Field()
    script_editor = scrapy.Field()
    script_editor_id = scrapy.Field()
    script_editor_href = scrapy.Field()
    starring = scrapy.Field()
    starring_id = scrapy.Field()
    starring_href = scrapy.Field()
    genre = scrapy.Field()
    runtime = scrapy.Field()
    initialReleaseDate = scrapy.Field()
    region = scrapy.Field()
    language = scrapy.Field()


