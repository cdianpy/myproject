# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
class MyprojectPipeline(object):
    def process_item(self, item, spider):
        # print(item)
        # with open('58.txt','a+') as f:
        #     f.write(''.join(item['strdes']))
        #     f.write("\n")
        return item

def dbHandle():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        passwd='penghy',
        charset='utf8',
        use_unicode=False
    )
    return conn
class GupiaoPipeline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        sql = 'insert into sunck.gupiao(交易时间,余额,买入额,偿还额,融资净买入,余量,卖出量,偿还量,融券净卖出,融资融券余额) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        try:
            cursor.execute(sql, (item['jysj'], item['ye'], item['mre'], item['che'], item['rzjmr'],item['yl'], item['mcl'], item['chl'], item['rzjmc'], item['rzrqmc']))
            dbObject.commit()
        except :
            dbObject.rollback()

        return item