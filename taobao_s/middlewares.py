# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import random
from scrapy import signals
from scrapy.http import HtmlResponse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

from taobao_s.settings import USER_AGENT_LIST, PROXIES


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua  = random.choice(USER_AGENT_LIST)
        if ua:
            request.headers.setdefault('User-Agent', ua)

class ProxyMiddleware(object):

    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        request.meta['proxy'] = proxy

class TaobaoSSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TaobaoSDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class LoginMiddleware(object):
    def process_request(self, request, spider):
        url = 'https://login.taobao.com/member/login.jhtml'
        options = webdriver.ChromeOptions()
        # 不加载图片,加快访问速度
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 无头化测试
        # options.add_argument('--headless')

        self.browser = webdriver.Chrome(executable_path="G:\chromedriver_win32\chromedriver.exe", options=options)
        self.wait = WebDriverWait(self.browser, 10)  # 超时时长为10s

        # 打开网页
        self.browser.get(url)

        # 自适应等待，点击密码登录选项
        self.browser.implicitly_wait(30)  # 智能等待，直到网页加载完毕，最长等待时间为30s
        self.browser.find_element_by_xpath('//*[@class="forget-pwd J_Quick2Static"]').click()

        # 自适应等待，点击微博登录宣传
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_xpath('//*[@class="weibo-login"]').click()

        # 自适应等待，输入微博账号
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_name('username').send_keys('zhan_jinzhou@sina.com')

        # 自适应等待，输入微博密码
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_name('password').send_keys('qwer@123')

        # 自适应等待，点击确认登录按钮
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_xpath('//*[@class="btn_tip"]/a/span').click()

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
        taobao_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                      '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))
        # 输出淘宝昵称
        print(taobao_name.text)

        cookie = self.browser.get_cookies()
        jsonCookie = json.dumps(cookie)
        with open('./cookies.json', 'w')as fp:
            fp.write(jsonCookie)
        self.browser.quit()

        return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source, encoding='utf-8',
                            request=request)