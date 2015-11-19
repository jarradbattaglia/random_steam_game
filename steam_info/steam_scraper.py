import scrapy
import json
import logging
from scrapy.selector import Selector
from scrapy import signals, log
from scrapy.spiders import Spider
from scrapy.item import Item, Field
from scrapy.http import FormRequest
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from twisted.internet import reactor

def start_scraper():
    print "Starting Steam Spider"
    crawler_obj = SteamSpider()
    crawler = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    crawler.crawl(crawler_obj)
    crawler.start()

def spider_closing(spider):
    print "Stopping Steam Spider"
    reactor.stop()

class SteamTag(Item):
    tag = Field()
    appid = Field()

class SteamSpider(Spider):
    name = "steam"
    steam_items = []

    def start_requests(self):
        urls = []
        with open("steam_games.txt", "r") as f:
            appids = f.readlines()
            for appid in appids:
                appid = appid.strip()
                yield scrapy.Request(url="http://store.steampowered.com/app/%s" % appid, 
                    meta = {"relative_app_url": appid})

        with open("steam.json", "w+") as f:
            json.dump(self.steam_items, f)

    def parse(self, response):
        if "agecheck" in response.url:
            if "relative_app_url" in response.meta:
                appid = response.meta["relative_app_url"]
                yield scrapy.FormRequest(url="http://store.steampowered.com/agecheck/app/%s" % appid,
                        formdata={"ageDay": "1", "ageMonth": "January", "ageYear": "1955"},
                        meta = {"relative_app_url": appid})
                return
            else:
                return
        sel = Selector(response)
        tags = sel.xpath('//*[@id="game_highlights"]/div[1]/div/div[4]/div/div[2]/a')
        #print response.meta
        items = []
        appid = response.meta["relative_app_url"]
        for tag in tags:
            #print tag.xpath("text()").extract()[0].strip("\r\t\n")
            items.append(tag.xpath("text()").extract()[0].strip("\r\t\n"))
        self.steam_items.append({"tag": items, "appid": appid})
