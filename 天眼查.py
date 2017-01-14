#功能：输入关键字，可以将所有含关键字的公司搜索出来


from selenium import webdriver
import re
import time

'''
    this website is built by dynamic webapge technology, each request to this site with a unique token.
    i take just two steps to solve the problem below:
    1,use webdriver module simulate human behavior by open chrome to download all webapge data
    2,use re module to find strings that you need. 
'''


global COMPANY_NAME
COMPANY_NAME=input('please input company name which you wanna search:')


def parse_page(link):#解析每个公司页面中的公司相关信息

    page=webdriver.Chrome()
    try:
        page.get(link)
        time.sleep(2)
        #print(page.page_source)
        hangye=re.findall(r'行业：<span class="ng-binding">(.*)</span></div></td><td class="basic-td" width="60%"><div class="c8">工商注册号',page.page_source)[0]
        gszch=re.findall(r'工商注册号：<span class="ng-binding">(.*)</span></div></td></tr><tr><td class="basic-td"><div class="c8">企业类型',page.page_source)[0]
        # with open('companyinfo.txt','r+') as fo :
        #     fo.write(hangye+'\n'+gszch+'\n'+'***********'+'\n')
        print(hangye)
        print(gszch)
        print('****************************')
    except Exception:
        page.get(link)
        time.sleep(2)
        #print(page.page_source)
        hangye=re.findall(r'行业：<span class="ng-binding">(.*)</span></div></td><td class="basic-td" width="60%"><div class="c8">工商注册号',page.page_source)[0]
        gszch=re.findall(r'工商注册号：<span class="ng-binding">(.*)</span></div></td></tr><tr><td class="basic-td"><div class="c8">企业类型',page.page_source)[0]
        # with open('companyinfo.txt','r+') as fo :
        #     fo.write(hangye+'\n'+gszch+'\n'+'***********'+'\n')
        print(hangye)
        print(gszch)
        print('****************************')
    finally:
        page.close()


def get_all_pages_urls():#获取所有页面的URL

    #打开查询结果页面
    page=webdriver.Chrome()
    page.get('http://www.tianyancha.com/search/p1?key={0}'.format(COMPANY_NAME))
    time.sleep(1)
    #一共有多少个结果页
    page_number=re.findall(r'<span>共</span>(\d{0,})<span>页</span>?',page.page_source)[0]
    #time.sleep(1)
    #关闭结果页
    page.close()
    page_number=int(page_number)
    print(page_number)
    all_urls=[]
    for num in range(1,page_number+1):
        all_urls=all_urls+get_single_page_urls(str(num))
    return all_urls


def get_single_page_urls(x):#获取单个页面的所有URL

    pageinfo=webdriver.Chrome()
    pageinfo.get('http://www.tianyancha.com/search/p{0}?key={1}'.format(str(x),COMPANY_NAME))
    time.sleep(1)
    urls=re.findall(r'href="(http://www\.tianyancha\.com/company/\d{0,})"?',pageinfo.page_source)

    pageinfo.close()
    print('page {} is finished'.format(x))
    return urls

def main():
    #获取所有链接
    url_list=get_all_pages_urls()
    #对每个链接进行内容的提取
    k=1 #k作为计数器，共有多少个页面被解析。
    for url in url_list:
        parse_page(url)
        print(k)
        k+=1


main()
