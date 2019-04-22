# -*- coding: utf-8 -*-
import json
import scrapy
from pathlib import Path
import random
from time import sleep
from urllib import parse

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from taobao_s.items import TaobaoSItem
from taobao_s.search_text import KEY_WORDS, PAGE_NUM

class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['s.taobao.com', 'rate.tmall.com']
    #start_urls = ['http://s.taobao.com/search?q=']
    base_url = 'https://s.taobao.com/search?q=%s&sort=sale-desc&s=%s'

    # scrapy请求的开始时start_request
    def start_requests(self):
        # taobao_findUrl = 'https://s.taobao.com/search?q=%E5%B8%BD%E5%AD%90&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.50862.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170817&s=300'
        if not Path('taobaoCookies.json').exists():
            __class__.loginTaobao()  # 先执行login，保存cookies之后便可以免登录操作
        # 从文件中获取保存的cookies
        with open('taobaoCookies.json', 'r', encoding='utf-8') as f:
            listcookies = json.loads(f.read())  # 获取cookies
        # 把获取的cookies处理成dict类型
        cookies_dict = dict()
        for cookie in listcookies:
            # 在保存成dict时，我们其实只要cookies中的name和value，而domain等其他都可以不要
            cookies_dict[cookie['name']] = cookie['value']
        key_words = KEY_WORDS
        key_words = parse.quote(key_words).replace(' ', '+')
        print(key_words)
        page_num = PAGE_NUM
        one_page_num = self.settings['ONE_PAGE_COUNT']
        for i in range(page_num):
            url = self.base_url % (key_words, i*one_page_num)
            sleep(random.randint(1,3))
            yield scrapy.Request(url, cookies=cookies_dict, callback=self.parse)

    # 使用selenium登录并获取登录后的cookies，后续需要登录的操作都可以利用cookies
    @staticmethod
    def loginTaobao():
        url = 'https://login.taobao.com/member/login.jhtml'
        options = webdriver.ChromeOptions()
        # 不加载图片,加快访问速度
        # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_argument('--headless')
        browser = webdriver.Chrome(executable_path="G:\chromedriver_win32\chromedriver.exe", options=options)
        wait = WebDriverWait(browser, 10)  # 超时时长为10s
        # 打开网页
        browser.get(url)
        # 自适应等待，点击密码登录选项
        browser.implicitly_wait(30)  # 智能等待，直到网页加载完毕，最长等待时间为30s
        browser.find_element_by_xpath('//*[@class="forget-pwd J_Quick2Static"]').click()
        browser.find_element_by_xpath('//*[@class="weibo-login"]').click()
        browser.find_element_by_name('username').send_keys('微博账号')
        browser.find_element_by_name('password').send_keys('微博密码')
        browser.find_element_by_xpath('//*[@class="btn_tip"]/a/span').click()
        # try:
        #     WebDriverWait(self.browser, 5, 0.5).until(
        #         EC.presence_of_element_located((By.NAME, 'verifycode')))
        #     print('！！！！出现验证码！！！！')
        #     img_url = self.browser.find_element_by_xpath('//*[@class="code"]/img').get_attribute('node-type')
        #     print(img_url)
        #     code = input('请输入验证码：')
        #     self.browser.find_element_by_name('verifycode').send_keys(code)
        #     self.browser.find_element_by_xpath('//*[@class="btn_tip"]/a/span').click()
        # except Exception as e:
        #     print('get button failed: ', e)

        # 直到获取到淘宝会员昵称才能确定是登录成功
        taobao_name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                      '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))
        # 输出淘宝昵称
        print(taobao_name.text)

        # 通过上述的方式实现登录后，其实我们的cookies在浏览器中已经有了，我们要做的就是获取
        cookies = browser.get_cookies()  # Selenium为我们提供了get_cookies来获取登录cookies
        browser.close()  # 获取cookies便可以关闭浏览器
        # 然后的关键就是保存cookies，之后请求从文件中读取cookies就可以省去每次都要登录一次的
        # 当然可以把cookies返回回去，但是之后的每次请求都要先执行一次login没有发挥cookies的作用
        jsonCookies = json.dumps(cookies)  # 通过json将cookies写入文件
        with open('taobaoCookies.json', 'w') as f:
            f.write(jsonCookies)
        print(cookies)

    def open_url(self, url):
        options = webdriver.ChromeOptions()
        # 不加载图片,加快访问速度
        # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--headless')
        browser = webdriver.Chrome(executable_path="G:\chromedriver_win32\chromedriver.exe", options=options)
        wait = WebDriverWait(browser, 10)  # 超时时长为10s
        # 打开网页
        browser.get(url)
        try:
            WebDriverWait(browser, 5, 0.5).until(
                EC.presence_of_element_located((By.ID, "nc_1__scale_text")))  # 等待滑动拖动控件出现
            swipe_button = browser.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span')  # 获取滑动拖动控件
            # 模拟拽托
            action = ActionChains(browser)  # 实例化一个action对象
            action.click_and_hold(swipe_button).perform()  # perform()用来执行ActionChains中存储的行为
            action.reset_actions()
            action.move_by_offset(580, 0).perform()  # 移动滑块
        except Exception as e:
            print('get button failed: ', e)


    def parse(self, response):
        p = 'g_page_config = ({.*?});'
        g_page_config = response.selector.re(p)[0]
        g_page_config = json.loads(g_page_config)
        auctions = g_page_config['mods']['itemlist']['data']['auctions']
        url1 = 'https://rate.tmall.com/list_detail_rate.htm?itemId=%s&sellerId=%s&order=3&currentPage=%s'
        # 从文件中获取保存的cookies
        with open('taobaoCookies.json', 'r', encoding='utf-8') as f:
            listcookies = json.loads(f.read())  # 获取cookies
        # 把获取的cookies处理成dict类型
        cookies_dict = dict()
        for cookie in listcookies:
            # 在保存成dict时，我们其实只要cookies中的name和value，而domain等其他都可以不要
            cookies_dict[cookie['name']] = cookie['value']
        for auction in auctions:
            item = TaobaoSItem()
            item['price'] = auction['view_price']
            item['sales'] = auction['view_sales']
            item['title'] = auction['raw_title']
            item['nick'] = auction['nick']
            item['loc'] = auction['item_loc']
            item['detail_url'] = auction['detail_url']
            item['nid'] = auction['nid']
            item['sellerid'] = auction['user_id']
            yield item
            # #天猫爬取商品详情页
            # if 'tmall' in item['detail_url']:
            #     for i in range(2):
            #         print(item['sellerid'])
            #         url = url1 % (item['nid'], item['sellerid'], str(i+1))
            #         print(url)
            #         request = scrapy.Request(url, cookies=cookies_dict, callback=self.parseNext, meta={'item':item})
            #         yield request

    def parseNext(self, response):
        print(response.meta['item']['detail_url'])
        print(response.text)
        # p = 'jsonp128({.*?})'
        # page_info = response.selector.re(p)[0]
        # page_info = json.loads(page_info)
        # print(page_info)
