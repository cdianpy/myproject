import scrapy
import json
import time
from myproject.items import GupiaojectItem
class gupiaos(scrapy.Spider):
    name = 'gupiao'
    # custom_settings = {
    #     'ITEM_PIPELINES': {}
    # }
    guP = GupiaojectItem()
    start_urls = ['http://stock.10jqka.com.cn/']
    def parse(self, response):

        a_list = response.xpath("//div[@id='rzrq']/table[@class='m-table']/tbody/tr/td[2]")
        for a in a_list:
            href = a.xpath("./a/@href").extract()[0]
            text = a.xpath(".//text()").extract()[0]
            yield scrapy.Request(href,
                                 callback=self.download,
                                 meta={'gp_name':text})
    dicone = {}
    def download(self,response):
        index = response.xpath(".//div[@class='m-page J-ajax-page']/span/text()").extract()[0]
        inds = index.split("/")[-1]
        url = response.url
        print(inds)
        gp_name = response.meta['gp_name']
        for x in range(1,int(inds)+1):
            print(x)
            href = url + "order/desc/page/"+ str(x)+"/ajax/1/"
            time.sleep(1)
            print(href)
            yield scrapy.Request(href,
                                 callback=self.download_all,
                                 meta={'gp_name': gp_name})

    def download_all(self, response):
        tr_list = response.xpath("//table[@class='m-table']/tbody/tr")
        gp_name = response.meta['gp_name']
        for tr in tr_list:
            a = tr.xpath(".//td[2]//text()").extract()[0].strip()
            self.guP['jysj'] = a
            self.dicone['交易时间'] = a
            self.guP['ye'] = tr.xpath(".//td[3]//text()").extract()[0] + "亿"
            self.dicone['余额'] = tr.xpath(".//td[3]//text()").extract()[0] + "亿"
            self.guP['mre'] = tr.xpath(".//td[4]//text()").extract()[0] + "亿"
            self.dicone['买入额'] = tr.xpath(".//td[4]//text()").extract()[0] + "亿"
            self.guP['che'] = tr.xpath(".//td[5]//text()").extract()[0] + "亿"
            self.dicone['偿还额'] = tr.xpath(".//td[5]//text()").extract()[0] + "亿"
            self.guP['rzjmr'] = tr.xpath(".//td[6]//text()").extract()[0] + "万"
            self.dicone['融资净买入'] = tr.xpath(".//td[6]//text()").extract()[0] + "万"
            self.guP['yl'] = tr.xpath(".//td[7]//text()").extract()[0] + "万股"
            self.dicone['余量'] = tr.xpath(".//td[7]//text()").extract()[0] + "万股"
            self.guP['mcl'] = tr.xpath(".//td[8]//text()").extract()[0] + "万股"
            self.dicone['卖出量'] = tr.xpath(".//td[8]//text()").extract()[0] + "万股"
            self.guP['chl'] = tr.xpath(".//td[9]//text()").extract()[0] + "万股"
            self.dicone['偿还量'] = tr.xpath(".//td[9]//text()").extract()[0] + "万股"
            self.guP['rzjmc'] = tr.xpath(".//td[10]//text()").extract()[0] + "万股"
            self.dicone['融券净卖出'] = tr.xpath(".//td[10]//text()").extract()[0] + "万股"
            self.guP['rzrqmc'] = tr.xpath(".//td[11]//text()").extract()[0] + "亿"
            self.dicone['融资融券余额'] = tr.xpath(".//td[11]//text()").extract()[0] + "亿"
            gup = json.dumps(self.dicone)
            with open(gp_name,'a+') as f:
                f.write(gup + "\n")
            self.dicone = {}





