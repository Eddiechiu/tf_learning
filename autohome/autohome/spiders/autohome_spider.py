import scrapy
from autohome.items import AutohomeItem


class AutohomeSpider(scrapy.spiders.Spider):
	name = 'autohome'
	allowed_domains = ['club.autohome.com.cn']
	start_urls = [
		'http://club.autohome.com.cn/'
	]

	def parse(self, response):
		'''
		Here the 'li' may not be the son of 'div[@class="forum-brand-box"]',
		so '//' is used here that means all 'li' contained in 'div[@class="forum-brand-box"]'  
		'''
		for sel in response.xpath('//div[@class="forum-brand-box"]//li/a'):
			item = AutohomeItem()
			'''
			NOTICE! there's no '/' before '@title', if added there will be nothing found.
			'aaa/aaa' means relative path and '/aaa/aaa' means absolute path
			'''
			item['car_name'] = sel.xpath('@title').extract()
			item['car_club_url'] = sel.xpath('@href').extract()
			yield item