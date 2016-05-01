# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    comment = scrapy.Field()
    user_id = scrapy.Field()
    name = scrapy.Field()
    avatar = scrapy.Field()
    rating = scrapy.Field()
    date = scrapy.Field()
    comment_vote = scrapy.Field()
    movie_id = scrapy.Field()
    last_update_time = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

    class Meta(object):
        db_collection_name = 'comment'
