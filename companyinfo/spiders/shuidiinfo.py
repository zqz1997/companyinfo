# -*- coding: utf-8 -*-
import datetime
import json
import re
import time
import requests
import scrapy
from companyinfo.items import CompanyinfoItem

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        '''
        #重写json里的date时间序列
        :param obj:
        :return:
        '''
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")

        else:
            return json.JSONEncoder.default(self, obj)


class ShuidiinfoSpider(scrapy.Spider):
    name = 'shuidiinfo'
    # allowed_domains = ['shuidi.cn']
    # start_urls = ['http://shuidi.cn/']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Host': 'shuidi.cn',
        'Cookie': 'guid=e0d1535c32ac9fe1746cd419deb4616d; Hm_lvt_4cb0385b9ad8022cb597e5015cb7a9e8=1572277755; pa_guid=3cf3f3c3a2a1fb4b91260c75a4d081a9; shuidi_user_id=1889790; shuidi_uid_token=8420c2b5870e154c850b80d763d0d72c; user_name=19802359005; Hm_lpvt_4cb0385b9ad8022cb597e5015cb7a9e8=1572278620',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Referer': 'https://cha.shuidi.cn/'
    }

    def start_requests(self):
        with open('company_list2.json', "r", encoding='gb18030') as f:
            line = " "  # line不能为空，不然进不去下面的循环
            while line:
                line = f.readline()
                if line != '' and line[0] != '#':
                    url = line.strip()
                    url = re.findall(r'"company_list": "(.*?)"', url, re.S | re.M)
                    url = url[0]
                    yield scrapy.Request(url=url, callback=self.parse)

    # def start_requests(self):
    #     urls = [
    #         'https://shuidi.cn/b-search?key=%E5%8D%8E%E4%B8%BA'
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        company_urls = response.xpath('//div[@class="or_search_row_company"]//a//@href').extract()
        for company_url in company_urls:
            items = CompanyinfoItem()
            metaModel = '搜索页'
            items['metaModel'] = metaModel
            source = '水滴信用'
            items['source'] = source
            # 'https://shuidi.cn/pc-search?key='
            url = response.url
            items['url'] = url
            header = self.headers
            items['header'] = header
            date = datetime.datetime.now()
            items['date'] = date
            company_url = company_url[:-14]
            s = company_url[8:]
            company_url = 'https://shuidi.cn' + company_url  # 公司连接
            yield scrapy.Request(url=company_url, callback=self.getinfo, meta={'items': items, 's': s})

    def getinfo(self, response):
        s = response.meta['s']
        items = response.meta['items']
        name = response.xpath('//div[@class="company_header_content"]/div/span//text()').extract_first()
        items['name'] = name
        # 法定代表人 = response.xpath('//table[@class="table1"]/tr[2]/td[2]/span/a//text()').extract()[0]
        # 公司基本信息 = {"法定代表人": 法定代表人, "company_url": response.url}
        time.sleep(1)


        # # 公司背景>>>工商信息
        # if len(re.findall(r'<span class="color_primary font_14">档案编码：(.*?)</span>', response.text, re.S)) != 0:
        #     档案编码 = re.findall(r'<span class="color_primary font_14">档案编码：(.*?)</span>', response.text, re.S)[0]  # 档案编码
        # else:
        #     档案编码 ='null'
        # 公司名字 = response.xpath('//div[@class="company_header_content"]//span//text()').extract()[0].strip()  # 公司名字
        # 法定代表人 = response.xpath('//td/span[@class="query-name"]/a//text()').extract()[0]  # 法定代表人
        # if len(response.xpath('//table[@class="table1"]/tr[2]/td[4]//text()').extract()) != 0:
        #     注册资本 = response.xpath('//table[@class="table1"]/tr[2]/td[4]//text()').extract()[0] # 注册资本
        # else:
        #     注册资本 = 'null'
        # if len(response.xpath('//table[@class="table1"]/tr[3]/td[2]//text()').extract()) != 0:
        #     企业信用代码 = response.xpath('//table[@class="table1"]/tr[3]/td[2]//text()').extract()[0]  # 企业信用代码
        # else:
        #     企业信用代码 = 'null'
        # if len(response.xpath('//table[@class="table1"]/tr[3]/td[4]//text()').extract()) != 0:
        #     成立时间 = response.xpath('//table[@class="table1"]/tr[3]/td[4]//text()').extract()[0]  # 成立时间
        # else:
        #     成立时间 = 'null'
        # if len(response.xpath('//table[@class="table1"]/tr[4]/td[2]//text()').extract()) != 0:
        #     登记机关 = response.xpath('//table[@class="table1"]/tr[4]/td[2]//text()').extract()[0]  # 登记机关
        # else:
        #     登记机关 = 'null'
        # if len(response.xpath('//table[@class="table1"]/tr[4]/td[4]//text()').extract()) != 0:
        #     核准日期 = response.xpath('//table[@class="table1"]/tr[4]/td[4]//text()').extract()[0]  # 核准日期
        # else:
        #     核准日期 = 'null'
        # if len(response.xpath('//table[@class="table1"]/tr[1]/td[4]//text()').extract()) != 0:
        #     登记状态 = response.xpath('//table[@class="table1"]/tr[1]/td[4]//text()').extract()[0]  # 登记状态
        # else:
        #     登记状态 = 'null'
        # if len(response.xpath('//table[@class="table1"]/tr[5]/td[2]//text()').extract()) != 0:
        #     营业期限 = response.xpath('//table[@class="table1"]/tr[5]/td[2]//text()').extract()[0]  # 营业期限
        # else:营业期限 = 'null'
        # if len(response.xpath('//table[@class="table1"]/tr[5]/td[4]//text()').extract()) != 0:
        #     企业类型 = response.xpath('//table[@class="table1"]/tr[5]/td[4]//text()').extract()[0]  # 企业类型
        # else:
        #     企业类型 = 'null'
        # if len(response.xpath('//table[@class="table1"]/tr[6]/td[2]//text()').extract()) != 0:
        #     所在省份 = response.xpath('//table[@class="table1"]/tr[6]/td[2]//text()').extract()[0]  # 所在省份
        # else:
        #     所在省份 = 'null'
        # if len(response.xpath('//table[@class="table1"]/tr[6]/td[4]//text()').extract()) != 0:
        #     企业地址 = response.xpath('//table[@class="table1"]/tr[6]/td[4]//text()').extract()[0]  # 企业地址
        # else:
        #     企业地址 = 'null'
        # if len(response.xpath('//table[@class="table1"]/tr[7]/td[2]//text()').extract()) != 0:
        #     经营范围 = response.xpath('//table[@class="table1"]/tr[7]/td[2]//text()').extract()[2].strip()  # 经营范围
        # else:
        #     经营范围 = 'null'
        #
        # 工商信息 = {"档案编码":档案编码,"公司名称":公司名字,"法定代表人":法定代表人,
        #         "注册资本":注册资本,"企业信用代码":企业信用代码,
        #         "成立时间":成立时间,"登记机关":登记机关,"核准日期":核准日期,
        #         "登记状态":登记状态,"营业期限":营业期限,"企业类型":企业类型,
        #         "所在省份":所在省份,"企业地址":企业地址,"经营范围":经营范围}
        # 公司背景 = {'工商信息':工商信息}
        # content['公司背景'] = 公司背景
        # # items['content'] = content
        # # yield items




        # # 司法风险>>>开庭公告
        # risk_url = 'https://shuidi.cn/company/risk' + str(s)
        # risk_detail = requests.get(url=risk_url, headers=self.headers).text
        # total_kaiting = re.findall(r'<span class="col_link ml_4">(.*?)</span>', risk_detail, re.M | re.S)
        # total_kaiting = int(total_kaiting[0])
        # print('开庭信息总条数{0}'.format(total_kaiting))
        # if total_kaiting != 0:
        #     pagenum_kaiting = total_kaiting // 5
        #     rest_kaiting = total_kaiting % 5
        #     if rest_kaiting > 0:
        #         pagenum_kaiting = pagenum_kaiting + 1
        #     if pagenum_kaiting > 20:
        #         pagenum_kaiting = 20
        #     print('开庭信息页数{0}'.format(pagenum_kaiting))
        #     i = 1
        #     开庭公告 = []
        #     for p in range(1, pagenum_kaiting + 1):
        #         time.sleep(4)
        #         kaiting_json_url = 'https://shuidi.cn/company/risk' + str(s) + '?action=page_court_anno&npage=' + str(p)
        #         print(kaiting_json_url)
        #         kaiting_json = requests.get(url=kaiting_json_url, headers=self.headers)
        #         kaiting_json = kaiting_json.text.encode().decode('unicode_escape')
        #         # print(kaiting_json)
        #         kaiting_json_num = re.findall(r'{"id":".*?]}', kaiting_json, re.M | re.S)
        #         for x in kaiting_json_num:
        #             开庭公告.append({i: x})
        #             i = i + 1
        #     司法风险 = {'开庭公告': 开庭公告}
        #     content['司法风险'] = 司法风险
        #     # items['content'] = content
        #     # yield items
        #
        # else:
        #     司法风险 = {'开庭公告': 'null'}
        #     content['司法风险'] = 司法风险
        #     # items['content'] = content
        #     # yield items



        #知识产权>>>商标信息
        property_url = 'https://shuidi.cn/company/property' + str(s)
        property_detail = requests.get(url=property_url, headers=self.headers).text
        total_trademark = re.findall(r'<span class="col_link ml_4">(.*?)</span>', property_detail, re.M | re.S)
        total_trademark = int(total_trademark[0])
        print('商标总数{0}'.format(total_trademark))
        if total_trademark != 0:
            pagenum_trademark = total_trademark // 5
            rest_trademark = total_trademark % 5
            if rest_trademark > 0:
                pagenum_trademark = pagenum_trademark + 1
            if pagenum_trademark > 20:
                pagenum_trademark = 20
            print('商标页数{0}'.format(pagenum_trademark))
            i2 = 1
            商标信息 = []
            for p2 in range(1, pagenum_trademark + 1):
                time.sleep(4)
                trademark_json_url = 'https://shuidi.cn/company/property' + str(s) + '?action=page_trademarks&npage=' + str(p2)
                print(trademark_json_url)
                trademark_json = requests.get(url=trademark_json_url, headers=self.headers)
                trademark_json = trademark_json.text.encode().decode('unicode_escape')
                # print(trademark_json)
                trademark_num = re.findall(r'{"id":".*?}', trademark_json, re.M | re.S)
                for x2 in trademark_num:
                    商标信息.append({i2: x2})
                    i2 = i2 + 1
            知识产权 = {}
            知识产权['商标信息'] = 商标信息
            # items['content'] = content
            # yield items
        else:
            知识产权 = {}
            知识产权['商标信息'] = 'null'
            # items['content'] = content
            # yield items


        #知识产权>>>作品著作权
        property_url = 'https://shuidi.cn/company/property' + str(s)
        property_detail = requests.get(url=property_url, headers=self.headers).text
        total_zhuzuoquan = re.findall(r'<span class="col_link ml_4">(.*?)</span>', property_detail, re.M | re.S)
        total_zhuzuoquan = int(total_zhuzuoquan[3])
        print('著作权总数{0}'.format(total_zhuzuoquan))
        if total_zhuzuoquan != 0:
            pagenum_zhuzuoquan = total_zhuzuoquan // 5
            rest_zhuzuoquan = total_zhuzuoquan % 5
            if rest_zhuzuoquan > 0:
                pagenum_zhuzuoquan = pagenum_zhuzuoquan + 1
            if pagenum_zhuzuoquan > 20:
                pagenum_zhuzuoquan = 20
            print('著作权页数{0}'.format(pagenum_zhuzuoquan))
            i著作权 = 1
            著作权信息 = []
            for p著作权 in range(1, pagenum_zhuzuoquan + 1):
                time.sleep(4)
                zhuzuoquan_json_url = 'https://shuidi.cn/company/property' + str(s) + '?action=page_copyrights&npage=' + str(p著作权)
                print(zhuzuoquan_json_url)
                zhuzuoquan_json = requests.get(url=zhuzuoquan_json_url, headers=self.headers)
                zhuzuoquan_json = zhuzuoquan_json.text.encode().decode('unicode_escape')
                # print(zhuzuoquan_json)
                zhuzuoquan_num = re.findall(r'{"id":".*?}', zhuzuoquan_json, re.M | re.S)
                for xzhuzuoquan in zhuzuoquan_num:
                    著作权信息.append({i著作权: xzhuzuoquan})
                    i著作权 = i著作权 + 1
            知识产权['著作权信息'] = 著作权信息
            # items['content'] = content
            # yield items
        else:
            知识产权['著作权信息'] = 'null'
            # items['content'] = content
            # yield items


        #知识产权>>>专利信息
        property_url = 'https://shuidi.cn/company/property' + str(s)
        property_detail = requests.get(url=property_url, headers=self.headers).text
        total_zhuanli = re.findall(r'<span class="col_link ml_4">(.*?)</span>', property_detail, re.M | re.S)
        total_zhuanli = int(total_zhuanli[1])
        print('专利总数{0}'.format(total_zhuanli))
        if total_zhuanli != 0:
            pagenum_zhuanli = total_zhuanli // 5
            rest_zhuanli = total_zhuanli % 5
            if rest_zhuanli > 0:
                pagenum_zhuanli = pagenum_zhuanli + 1
            if pagenum_zhuanli > 20:
                pagenum_zhuanli = 20
            print('专利页数{0}'.format(pagenum_zhuanli))
            i专利 = 1
            专利信息 = []
            for p专利 in range(1, pagenum_zhuanli + 1):
                time.sleep(4)
                zhuanli_json_url = 'https://shuidi.cn/company/property' + str(s) + '?action=page_patents&npage=' + str(p专利)
                print(zhuanli_json_url)
                zhuanli_json = requests.get(url=zhuanli_json_url, headers=self.headers)
                zhuanli_json = zhuanli_json.text.encode().decode('unicode_escape')
                # print(zhuanli_json)
                zhuanli_num = re.findall(r'{"id":".*?}', zhuanli_json, re.M | re.S)
                for xzhuanli in zhuanli_num:
                    专利信息.append({i专利: xzhuanli})
                    i专利 = i专利 + 1
            知识产权['专利信息'] = 专利信息
            items['知识产权'] = 知识产权
            yield items
        else:
            知识产权['专利信息'] = 'null'
            items['知识产权'] = 知识产权
            yield items

