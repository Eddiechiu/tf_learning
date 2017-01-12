import scrapy

# 在shell中获取网站源码的response的命令，输入：scrapy shell "http://....."
# 在shell中启动爬虫：scrapy crawl xxx(spider的name)

class DomzSpider(scrapy.spiders.Spider):
	name = 'dmoz'
	allowed_domains = ['dmoz.org']
	start_urls = [
		'http://www.dmoz.org/Computers/Programming/Languages/Python/Books/',
        'http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/'
	]

	def parse(self, response):
		# response.url.split('/')[-2] 相当于把上面的url地址用/隔开，然后把Books、Resources取出来。[-1]是''(啥都没有)
		# filename = response.url.split('/')[-2]
		# with open(filename, 'wb') as f:
		# 	f.write(response.body)
		for sel in response.xpath('//ul/li'):
			title = sel.xpath('a/text()').extract()
			link = sel.xpath('a/@href').extract()
			desc = sel.xpath('text()').extract()
			print(title, link, desc)