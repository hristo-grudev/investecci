import json

import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import InvestecciItem
from itemloaders.processors import TakeFirst

import requests

url = "https://www.investec.com/bin/search/elasticsearch?r=chArticleListingArticles"

payload="{\"id\":\"dotcom-articles\",\"params\":{\"sortby\":\"datearticle\",\"sortorder\":\"\",\"from\":0,\"size\":3,\"localefilter\":\"en_gb\",\"sitesourcefilter\":\"\",\"pagetypefilter\":\"\",\"tagsfilter\":[\"dotcom:product-page-tags/geography/united-kingdom\",\"dotcom:content-hub-tags/newsletter/prime-property\",\"dotcom:content-hub-tags/content-hub-category/markets-and-economy\",\"dotcom:content-hub-tags/newsletter/brexit\"],\"tagsandfilter\":[],\"datecreated.min\":\"\",\"datecreated.max\":\"\",\"includepath\":[\"/content/dotcom/en_gb/focus\"],\"excludetags\":[\"\"],\"tagsort\":{},\"highlightsarticle\":[\"\"],\"excludedocs\":[],\"excludepages\":[\"/content/dotcom/en_chis.html\",\"/content/microsites/impact/en_chis.html\",\"/content/microsites/ifacontent/en_chis.html\"],\"returnedfields\":[\"_id\",\"tagtitles\",\"imagedesktop\",\"imageeditorspick\",\"excerpt\",\"imagelisting\",\"video\",\"podcast\",\"includedate\",\"read\",\"displaydatearticle\",\"podcasthours\",\"podcastminutes\",\"videohours\",\"videominutes\",\"readhours\",\"readminutes\",\"highlightsarticle\",\"author\",\"type\",\"pageurl\",\"datecreated\",\"sitesource\",\"pagetype\",\"tags\",\"imageurl\",\"content\",\"locale\",\"title\",\"displaydatecreated\",\"rawtags\",\"tagtitles\",\"externalsite\",\"toplines\",\"primarytagtitle\",\"dcheading\",\"primarytag\"],\"sourcefields\":[],\"getsuggest\":true,\"gethighlight\":true,\"getaggregations\":true,\"pinarticlefilter\":[\"\"],\"editorspickfilter\":[\"\"],\"pinseriesfilter\":false,\"highlightsarticlefilter\":[\"\"]}}"
headers = {
  'authority': 'www.investec.com',
  'pragma': 'no-cache',
  'cache-control': 'no-cache',
  'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
  'accept': 'application/json, text/plain, */*',
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
  'content-type': 'application/json',
  'origin': 'https://www.investec.com',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.investec.com/en_chis.html',
  'accept-language': 'en-US,en;q=0.9,bg;q=0.8',
  'cookie': '__cfduid=d71a2eecde2f872804846b4efdcd2f0771615878405; AMCVS_38AC7FBA57E2AF467F000101%40AdobeOrg=1; s_ecid=MCMID%7C36646105356360524191322424761042891896; _ga=GA1.2.619859221.1615878421; _gid=GA1.2.1843448193.1615878421; s_cc=true; _fbp=fb.1.1615878423770.999134707; _gcl_au=1.1.459747009.1615878426; _gat=1; s_dfa=invbnkdigitalprod; AMCV_38AC7FBA57E2AF467F000101%40AdobeOrg=870038026%7CMCIDTS%7C18703%7CMCMID%7C36646105356360524191322424761042891896%7CMCAAMLH-1616490723%7C6%7CMCAAMB-1616490723%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1615893123s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.0.0; s_ppn=DotCom_en_chis_EN_prod; s_vnum=1618470422606%26vn%3D2; s_invisit=true; s_sq=%5B%5BB%5D%5D; s_ppvl=DotCom_en_chis_EN_prod%2C33%2C33%2C977%2C1920%2C977%2C1920%2C1080%2C1%2CP; s_ptc=0.02%5E%5E0.04%5E%5E0.04%5E%5E0.05%5E%5E0.28%5E%5E0.04%5E%5E8.52%5E%5E0.02%5E%5E8.98; s_getNewRepeat=1615885931840-Repeat; s_ppv=DotCom_en_chis_EN_prod%2C100%2C33%2C3003%2C1341%2C977%2C1920%2C1080%2C1%2CP'
}


class InvestecciSpider(scrapy.Spider):
	name = 'investecci'
	start_urls = ['https://www.investec.com/en_chis.html']

	def parse(self, response):
		data = requests.request("POST", url, headers=headers, data=payload)
		raw_data = json.loads(data.text)

		for post in raw_data['hits']['hits']:
			title = post['fields']['title'][-1]
			description = remove_tags(post['fields']['content'][0])
			date = post['fields']['displaydatecreated'][0]

			item = ItemLoader(item=InvestecciItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)

			yield item.load_item()
