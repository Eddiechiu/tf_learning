import scrapy
from autohome.items import AutohomeItem
import re

class AutohomeSpider(scrapy.spiders.Spider):
	name = 'autohome'
	allowed_domains = ['club.autohome.com.cn']
	start_urls = [
		'http://club.autohome.com.cn/'
	]

	def parse(self, response):
	
		# Here the 'li' may not be the son of 'div[@class="forum-brand-box"]',
		# so '//' is used here that means all 'li' contained in 'div[@class="forum-brand-box"]'  

		for sel in response.xpath('//div[@class="forum-brand-box"]//li/a'):
			
			# NOTICE! there's no '/' before '@title', if added there will be nothing found.
			# 'aaa/aaa' means relative path and '/aaa/aaa' means absolute path

			url_path = 'http://club.autohome.com.cn' + sel.xpath('@href').extract()[0]
			# post_path = 'http://club.autohome.com.cn' + item['car_club_url'] 
			# print(post_path)
			yield scrapy.Request(url_path, callback=self.parse_single_club)
		# item = AutohomeItem()
		# item['num_posts'] = response.xpath('//div[@class="pagearea"]/div[@class="fl"]/span').extract()
		# yield item

	def parse_single_club(self, response):
		item = AutohomeItem()
		# note .extract() return a list, not a string 
		content = response.xpath('//div[@class="pagearea"]/div[@class="fl"]/span').extract()[0]
		item['num_posts'] = re.findall(r'<span>(.*?)</span>', content)
		yield item
	# 	# regular expression for the number of posts in the club:
	# 	# re.findall(r'<span>(.*?)</span>', response.xpath('//div[@class="pagearea"]/div[@class="fl"]/span').extract())
	# 	# response is from url='http://club.autohome.com.cn/bbs/forum-c-692-1.html'
	# 	# (NOTICE here [@class="xxxx"], "" must be used, which cannot be replaced by '')