import scrapy
from autohome.items import AutohomeItem


class AutohomeSpider(scrapy.spiders.Spider):
	name = 'autohome_spider'
	allowed_domains = ['club.autohome.com.cn']
	start_urls = [
		'http://club.autohome.com.cn/'
	]

	def parse(self, response):
		for sel in response.xpath('//div[@class="forum-brand-box"]//li/a/@title').extract():
			item = AutohomeItem()
			item['content'] = sel
			yield item