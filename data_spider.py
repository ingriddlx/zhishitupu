import urllib.request#用来发送request和获取request的结果
import urllib.parse
from lxml import etree#解析网页
import pymongo #获取数据库
import re


class GameSpider:
    def __init__(self):#class的实例
        self.conn = pymongo.MongoClient()#创建一个MongoClient来运行mongod实例,采用默认host和port
        self.db = self.conn['game']#数据库初始化
        self.col = self.db['data']#数据库表初始化

    '''根据url，请求html'''
    def get_html(self, url):
      #headers 参数是一个字典，通过User-Agent伪装浏览器
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/51.0.2704.63 Safari/537.36'}
        req = urllib.request.Request(url=url, headers=headers)#更强大的 Request 类来构建一个请求
        res = urllib.request.urlopen(req)
      #用 urlopen() 方法来发送这个请求，只不过这次 urlopen() 方法的参数不再是一个URL，而是一个 Request
        html = res.read().decode('gbk')#读取请求返回值
        return html

    '''url解析'''
    def url_parser(self, content):
        selector = etree.HTML(content)#用来解析字符串格式的HTML文档对象，将传进去的字符串转变成_Element对象
        urls = ['https://pvp.qq.com/web201605/herolist.shtml' + i for i in  selector.xpath('//ul[@class="herolist-content"]/li[i]/a/text()')]# 通过xpath筛选出所需要的代码信息
        return urls

    # '''测试'''
    # def spider_main(self): 
    #     for page in range(1, 11000):
    #         try:
    #             basic_url = 'http://jib.xywy.com/il_sii/gaishu/%s.htm'%page
    #             cause_url = 'http://jib.xywy.com/il_sii/cause/%s.htm'%page
    #             prevent_url = 'http://jib.xywy.com/il_sii/prevent/%s.htm'%page
    #             symptom_url = 'http://jib.xywy.com/il_sii/symptom/%s.htm'%page
    #             inspect_url = 'http://jib.xywy.com/il_sii/inspect/%s.htm'%page
    #             treat_url = 'http://jib.xywy.com/il_sii/treat/%s.htm'%page
    #             food_url = 'http://jib.xywy.com/il_sii/food/%s.htm'%page
    #             drug_url = 'http://jib.xywy.com/il_sii/drug/%s.htm'%page
    #             data = {}
    #             data['url'] = basic_url
    #             data['basic_info'] = self.basicinfo_spider(basic_url)
    #             data['cause_info'] =  self.common_spider(cause_url)
    #             data['prevent_info'] =  self.common_spider(prevent_url)
    #             data['symptom_info'] = self.symptom_spider(symptom_url)
    #             data['inspect_info'] = self.inspect_spider(inspect_url)
    #             data['treat_info'] = self.treat_spider(treat_url)
    #             data['food_info'] = self.food_spider(food_url)
    #             data['drug_info'] = self.drug_spider(drug_url)
    #             print(page, basic_url)
    #             self.col.insert(data)

    #         except Exception as e:
    #             print(e, page)
    #     return

    # '''基本信息解析'''
    # def basicinfo_spider(self, url):
    #     html = self.get_html(url)
    #     selector = etree.HTML(html)
    #     title = selector.xpath('//title/text()')[0]
    #     category = selector.xpath('//div[@class="wrap mt10 nav-bar"]/a/text()')
    #     desc = selector.xpath('//div[@class="jib-articl-con jib-lh-articl"]/p/text()')
    #     ps = selector.xpath('//div[@class="mt20 articl-know"]/p')
    #     infobox = []
    #     for p in ps:
    #         info = p.xpath('string(.)').replace('\r','').replace('\n','').replace('\xa0', '').replace('   ', '').replace('\t','')
    #         infobox.append(info)
    #     basic_data = {}
    #     basic_data['category'] = category
    #     basic_data['name'] = title.split('的简介')[0]
    #     basic_data['desc'] = desc
    #     basic_data['attributes'] = infobox
    #     return basic_data

    # '''treat_infobox治疗解析'''
    # def treat_spider(self, url):
    #     html = self.get_html(url)
    #     selector = etree.HTML(html)
    #     ps = selector.xpath('//div[starts-with(@class,"mt20 articl-know")]/p')
    #     infobox = []
    #     for p in ps:
    #         info = p.xpath('string(.)').replace('\r','').replace('\n','').replace('\xa0', '').replace('   ', '').replace('\t','')
    #         infobox.append(info)
    #     return infobox

    # '''treat_infobox治疗解析'''
    # def drug_spider(self, url):
    #     html = self.get_html(url)
    #     selector = etree.HTML(html)
    #     drugs = [i.replace('\n','').replace('\t', '').replace(' ','') for i in selector.xpath('//div[@class="fl drug-pic-rec mr30"]/p/a/text()')]
    #     return drugs

    # '''food治疗解析'''
    # def food_spider(self, url):
    #     html = self.get_html(url)
    #     selector = etree.HTML(html)
    #     divs = selector.xpath('//div[@class="diet-img clearfix mt20"]')
    #     try:
    #         food_data = {}
    #         food_data['good'] = divs[0].xpath('./div/p/text()')
    #         food_data['bad'] = divs[1].xpath('./div/p/text()')
    #         food_data['recommand'] = divs[2].xpath('./div/p/text()')
    #     except:
    #         return {}

    #     return food_data

    # '''症状信息解析'''
    # def symptom_spider(self, url):
    #     html = self.get_html(url)
    #     selector = etree.HTML(html)
    #     symptoms = selector.xpath('//a[@class="gre" ]/text()')
    #     ps = selector.xpath('//p')
    #     detail = []
    #     for p in ps:
    #         info = p.xpath('string(.)').replace('\r','').replace('\n','').replace('\xa0', '').replace('   ', '').replace('\t','')
    #         detail.append(info)
    #     symptoms_data = {}
    #     symptoms_data['symptoms'] = symptoms
    #     symptoms_data['symptoms_detail'] = detail
    #     return symptoms, detail

    # '''检查信息解析'''
    # def inspect_spider(self, url):
    #     html = self.get_html(url)
    #     selector = etree.HTML(html)
    #     inspects  = selector.xpath('//li[@class="check-item"]/a/@href')
    #     return inspects

    # '''通用解析模块'''
    # def common_spider(self, url):
    #     html = self.get_html(url)
    #     selector = etree.HTML(html)
    #     ps = selector.xpath('//p')
    #     infobox = []
    #     for p in ps:
    #         info = p.xpath('string(.)').replace('\r', '').replace('\n', '').replace('\xa0', '').replace('   ','').replace('\t', '')
    #         if info:
    #             infobox.append(info)
    #     return '\n'.join(infobox)
    '''检查项抓取模块'''
    def inspect_crawl(self):
        # for page in range(1, 3685):
            try:
                url = 'http://jck.xywy.com/jc_%s.html'%page
                html = self.get_html(url)
                data = {}
                data['url']= url
                data['html'] = html
                self.db['jc'].insert(data)
                print(url)
            except Exception as e:
                print(e)


handler = GameSpider()
handler.inspect_crawl()