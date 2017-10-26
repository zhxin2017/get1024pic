import os
import requests
import time
from bs4 import BeautifulSoup as bs

agent = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"}

def get_url_page_list(url_main, params):
    url_base = 'http://t66y.com/'
    url_page_list = []
    page_title_list = []
    try:
        r_site = requests.get(url_main, headers=agent, params=params)
        r_site.encoding = 'GBK'
        html = r_site.text
        soup_main = bs(html)
        h3_tags = soup_main.find_all('h3')
        start_page = 0
        if params['page'] == '1':
            start_page = 9
        for i in range(start_page,len(h3_tags)):
            url_page = url_base + h3_tags[i].a.get('href')
            page_title = h3_tags[i].a.contents[0]
            print("url_page---" + url_page + ' ' + page_title)
            url_page_list.append(url_page)
            page_title_list.append(page_title)

    except:
        print('failed to get page list. ')
    return url_page_list, page_title_list
    

def get_src_list(url_page):
    src_list = []
    try:
        r_page = requests.get(url_page, headers=agent)
        r_page.encoding = 'GBK'
        soup_pic = bs(r_page.text)
        inputs = soup_pic.find_all(
                'div', class_='tpc_content do_not_catch')[0].find_all('input')
        for i in inputs:
            src = i.get('src')
            src_list.append(src)
    except:
        print("failed to get src list. ")
    return src_list


def save_pic(src_list):
    for i in src_list:
        pic_name = i.split('/')[-1]
        if not os.path.exists(pic_name):
            try:
                r_pic = requests.get(i, headers=agent)
                with open(pic_name, 'wb') as f:
                    f.write(r_pic.content)
                print("succeeded to save pic: " + pic_name + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            except Exception as ex:
                print(str(ex))
                print("failed to save pic: " + pic_name + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        else:
            print("file already exists: " + pic_name)


def download():
    if not os.path.exists('1024'):
        os.mkdir('1024')
    os.chdir('1024')
    url_main = 'http://t66y.com/thread0806.php'
    params = {'fid':'16','search':'','page':'0'}
    for i in range(1,11):
        params['page'] = str(i)
        url_page_list, page_title_list = get_url_page_list(url_main, params)
        page_list_len = len(url_page_list)
        for j in range(page_list_len):
            src_list = get_src_list(url_page_list[j])
            if not os.path.exists(page_title_list[j]):
                os.mkdir(page_title_list[j])
            os.chdir(page_title_list[j])
            save_pic(src_list)
            os.chdir('..')
