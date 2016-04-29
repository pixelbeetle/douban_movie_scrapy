# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    poster = scrapy.Field()
    alternate_name = scrapy.Field()
    year = scrapy.Field()
    rating = scrapy.Field()
    rating_per = scrapy.Field()
    rating_betterthan = scrapy.Field()
    rating_betterthan_href = scrapy.Field()
    director = scrapy.Field()
    director_id = scrapy.Field()
    script_editor = scrapy.Field()
    script_editor_id = scrapy.Field()
    starring = scrapy.Field()
    starring_id = scrapy.Field()
    genre = scrapy.Field()
    tags = scrapy.Field()
    summary = scrapy.Field()
    runtime = scrapy.Field()
    initialReleaseDate = scrapy.Field()
    region = scrapy.Field()
    language = scrapy.Field()
    imdb = scrapy.Field()
    imdb_href = scrapy.Field()
    recommendations_id = scrapy.Field()
    recommendations = scrapy.Field()
    collections_number = scrapy.Field()
    wishes_number = scrapy.Field()
    last_update_time = scrapy.Field()


