#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# @Author   :Zhangjinzhou
# @Time     :2019/4/21 9:17
# @Filename :app.py
import codecs
import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")



@app.route("/api", methods=['POST', 'GET'])
def api_main():
    if request.method == "POST":
        search_text = request.form.get('search')
        page_num = request.form.get('pagenum')
        #写入需要搜索的内容，以及查询页数
        if search_text:
            file = r'E:\LearnSpider\taobao_s\taobao_scrapy\taobao_s\search_text.py'
            with codecs.open(file, 'w', 'utf-8') as f:
                f.write('KEY_WORDS = \"' + search_text + '\"\n')
                f.write('PAGE_NUM = '+ page_num + '\n')
                f.close()
        #调用scrapy
        os.system("scrapy crawl taobao")
        with open('E:/LearnSpider/taobao_s/taobao_scrapy/'+ search_text + '.json') as f:
            json = f.read()
            f.close()
        return json
    if request.method == "GET":
        search_text = request.args.get('search')
        page_num = request.args.get('pagenum')
        # 写入需要搜索的内容，以及查询页数
        if search_text:
            file = r'E:\LearnSpider\taobao_s\taobao_scrapy\taobao_s\search_text.py'
            with codecs.open(file, 'w', 'utf-8') as f:
                f.write('KEY_WORDS = \"' + search_text + '\"\n')
                f.write('PAGE_NUM = ' + page_num + '\n')
                f.close()
        # 调用scrapy
        os.system("scrapy crawl taobao")
        with open('E:/LearnSpider/taobao_s/taobao_scrapy/' + search_text + '.json', 'r', encoding='utf-8') as f:
            json = f.read()
            f.close()
        return json

if __name__ == '__main__':
    app.run(port=8776, debug=True)
