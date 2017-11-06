import scrapy
from lxml import etree
import re
import json
import time
from myproject.items import MyprojectItem
class FirstSpider(scrapy.Spider):
    name = 'firstspider'
    start_urls = ['http://www.baidu.com']
    def parse(self, response):
        print(response.text)



class wbSpider(scrapy.Spider):
    name = 'wbtc'
    start_urls = ['http://bj.58.com/chuzu/?PGTID=0d100000-0000-10d1-5793-3b63d5b680a1&ClickID=1']
    # index = 2
    wbtcitem = MyprojectItem()
    def parse(self, response):
        # time.sleep(1)
        # html = etree.HTML(response.text)
        # a = response.xpath('//div[@class="des"]/h2/a//text()').extract()
        all_li = response.xpath("//ul[@class='listUl']/li[@logr]")
        if not all_li:
            return
        # print(housetype)
        # dicone = {}
        # dicall = {}
        for li in all_li:
            # print(re.split(r'\s+',x)[0])
            des = str(li.xpath(".//div[@class='des']/h2/a//text()").extract())
            house = str(li.xpath(".//div[@class='des']/p[@class='room']//text()").extract())
            add = str(li.xpath(".//div[@class='des']/p[@class='add']/a//text()").extract())
            money = str(li.xpath(".//div[@class='money']//text()").extract())
            desli = des.split()
            strdes = ''
            for y in range(1,len(desli)-1):
                if desli[y].split('\'')[0] != (','or'\\'):
                    strdes += desli[y].split('\'')[0]

            moneyli = re.split(r'\s+', money)[2].split('\'')[1]+"元/月"
            # dicone['money'] = moneyli
            self.wbtcitem['money'] = moneyli
             # print(re.split(r'\s+', house)[1])
            housesize = re.split(r'\s+', house)[1].split('\'')[0].split('a')[-1]
            # dicone['housesize'] = housesize
            self.wbtcitem['housesize'] = housesize
            housetype = re.split(r'\s+', house)[0].split('\'')[-1]
            # dicone['housetype'] = housetype
            self.wbtcitem['housetype'] = housetype
            addt = re.split(r'\s+', add)[0].split('\'')[1]
            if len(re.split(r'\s+', add)) == 1:
                # dicone['add'] = addt
                self.wbtcitem['add'] = addt
            else:
                addw = re.split(r'\s+', add)[1].split('\'')[1]
                # dicone['add'] = addt + addw
                self.wbtcitem['add'] = addt + addw
            # dicall[strdes] = dicone
            self.wbtcitem['strdes'] = strdes
            # print(dicone)
            # dicone = {}
            yield self.wbtcitem
        # dicalla = json.dumps(dicall)
        # with open('58.txt','a') as f:
            # f.write(dicalla)

        # url = 'http://bj.58.com/chuzu/pn' + str(self.index)
        # self.index += 5
        #
        # yield scrapy.Request(url,callback=self.parse)