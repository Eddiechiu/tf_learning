import scrapy
from autohome.items import AutohomeItem
import re


class AutohomeSpider(scrapy.spiders.Spider):
	# name属性用于在cmd窗口启动爬虫，每个爬虫的name必须唯一，如：scrapy crawl autohome
	name = 'autohome'
	allowed_domains = ['car.autohome.com.cn']
	start_urls = [
		'http://car.autohome.com.cn/price/brand-70.html'
	]

	def parse(self, response):

		# Here the 'li' may not be the son of 'div[@class="forum-brand-box"]',
		# so '//' is used here that means all 'li' contained in 'div[@class="forum-brand-box"]'  

		for href in response.xpath('//div[@class="main-title"]/a/@href').extract():
			
			# NOTICE! there's no '/' before '@title', if added there will be nothing found.
			# 'aaa/aaa' means relative path and '/aaa/aaa' means absolute path

			url_path = 'http://car.autohome.com.cn' + href
			# post_path = 'http://club.autohome.com.cn' + item['car_club_url'] 
			# print(post_path)
			yield scrapy.Request(url_path, callback=self.car_list)
		# item = AutohomeItem()
		# item['num_posts'] = response.xpath('//div[@class="pagearea"]/div[@class="fl"]/span').extract()
		# yield item

	def car_list(self, response):
		for href in response.xpath('//div[@class="interval01-list-cars-infor"]/p/a/@href').extract()[0]:
			# 这一步会返回两种href，其中一种是“惠民补贴”，需要筛出
			yield scrapy.Request('http://' + href, callback=self.car_infor_collect)
		#item = AutohomeItem()
		#  # note .extract() return a list, not a string
		#item['car_name'] = response.xpath('//div[@class="brand-name"]/a').extract()

		#content = response.xpath('//div[@class="pagearea"]/div[@class="fl"]/span').extract()[0]
		#item['num_posts'] = re.findall(r'<span>(.*?)</span>', content)
		#yield item
	# 	# regular expression for the number of posts in the club:
	# 	# re.findall(r'<span>(.*?)</span>', response.xpath('//div[@class="pagearea"]/div[@class="fl"]/span').extract())
	# 	# response is from url='http://club.autohome.com.cn/bbs/forum-c-692-1.html'
	# 	# (NOTICE here [@class="xxxx"], "" must be used, which cannot be replaced by '')

	def car_infor_collect(self, response):
		item = AutohomeItem()

		data_0 = response.xpath('//div[@class="breadnav fn-left"]/a/text()').extract()
		item['size'] = data_0[1]
		item['name'] = data_0[2]
		item['details'] = data_0[3]

		item['score'] = response.xpath('//a[@class="fn-fontsize14 font-bold"]/text()').extract()[0]
		yield item