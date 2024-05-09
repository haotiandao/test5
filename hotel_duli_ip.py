import random
import concurrent.futures
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import re
from bs4 import BeautifulSoup
from queue import Queue
import threading
import requests
from requests.exceptions import Timeout

lock = threading.Lock()
# 查找所有符合指定格式的网址
infoList = []
urls_y = []
resultslist = []
urls = []
# 初始化计数器为0
counter = -1
 
# 每次调用该函数时将计数器加1并返回结果
def increment_counter():
    global counter
    counter += 1
    return counter

#判断一个数字是单数还是双数可
def is_odd_or_even(number):
    if number % 2 == 0:
        return True
    else:
        return False


    
sorted_list = [
    "171.117.255.176:8082",
]

headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '72',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'foodieguide.com',
    'Origin': 'http://foodieguide.com',
    'Referer': 'http://foodieguide.com/iptvsearch/hoteliptv.php',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

def worker(thread_url,counter_id):
    try:
        # 创建一个Chrome WebDriver实例
        results = []
        page_url= f"http://foodieguide.com/iptvsearch/alllist.php?s={thread_url}"
        response = response.get(page_url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            print(soup)
            tables_div = soup.find("div", class_="tables")
            results = (
                tables_div.find_all("div", class_="result")
                if tables_div
                else []
            )
            if not any(
                result.find("div", class_="m3u8") for result in results
            ):
                #break
                print("Err-------------------------------------------------------------------------------------------------------")
            for result in results:
                #print(result)
                m3u8_div = result.find("div", class_="m3u8")
                url_int = m3u8_div.text.strip() if m3u8_div else None
                #取频道名称
                m3u8_name_div = result.find("div", class_="channel")
                url_name = m3u8_name_div.text.strip() if m3u8_div else None
                #－－－－－
                #print("-------------------------------------------------------------------------------------------------------")
                name =f"{url_name}"
                if len(name) == 0:
                    name = "Err画中画"
                #print(name)
                urlsp =f"{url_int}"
                if len(urlsp) == 0:
                    urlsp = "rtp://127.0.0.1"             
                print(f"{url_name}\t{url_int}")
                #print("-------------------------------------------------------------------------------------------------------")
                urlsp = urlsp.replace("http://67.211.73.118:9901", "")
                name = name.replace("cctv", "CCTV")
                name = name.replace("中央", "CCTV")
                name = name.replace("央视", "CCTV")
                name = name.replace("高清", "")
                name = name.replace("HD", "")
                name = name.replace("标清", "")
                name = name.replace("频道", "")
                name = name.replace("-", "")
                name = name.replace(" ", "")
                name = name.replace("PLUS", "+")
                name = name.replace("＋", "+")
                name = name.replace("(", "")
                name = name.replace(")", "")
                name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
                name = name.replace("CCTV1综合", "CCTV1")
                name = name.replace("CCTV2财经", "CCTV2")
                name = name.replace("CCTV3综艺", "CCTV3")
                name = name.replace("CCTV4国际", "CCTV4")
                name = name.replace("CCTV4中文国际", "CCTV4")
                name = name.replace("CCTV4欧洲", "CCTV4")
                name = name.replace("CCTV5体育", "CCTV5")
                name = name.replace("CCTV6电影", "CCTV6")
                name = name.replace("CCTV7军事", "CCTV7")
                name = name.replace("CCTV7军农", "CCTV7")
                name = name.replace("CCTV7农业", "CCTV7")
                name = name.replace("CCTV7国防军事", "CCTV7")
                name = name.replace("CCTV8电视剧", "CCTV8")
                name = name.replace("CCTV9记录", "CCTV9")
                name = name.replace("CCTV9纪录", "CCTV9")
                name = name.replace("CCTV10科教", "CCTV10")
                name = name.replace("CCTV11戏曲", "CCTV11")
                name = name.replace("CCTV12社会与法", "CCTV12")
                name = name.replace("CCTV13新闻", "CCTV13")
                name = name.replace("CCTV新闻", "CCTV13")
                name = name.replace("CCTV14少儿", "CCTV14")
                name = name.replace("CCTV15音乐", "CCTV15")
                name = name.replace("CCTV16奥林匹克", "CCTV16")
                name = name.replace("CCTV17农业农村", "CCTV17")
                name = name.replace("CCTV17农业", "CCTV17")
                name = name.replace("CCTV5+体育赛视", "CCTV5+")
                name = name.replace("CCTV5+体育赛事", "CCTV5+")
                name = name.replace("CCTV5+体育", "CCTV5+")
                name = name.replace("CMIPTV", "")
                name = name.replace("内蒙卫视", "内蒙古卫视")
                name = name.replace("CCTVCCTV", "CCTV")
                if "http" in urlsp:
                    # 获取锁
                    lock.acquire()
                    infoList.append(f"{name},{urlsp}")
                    # 释放锁
                    lock.release()
            print(f"=========================>>> Thread {thread_url} save ok")
    except Exception as e:
        print(f"=========================>>> Thread {thread_url} caught an exception: {e}")
    finally:
        print(f"=========================>>> Thread {thread_url}  quiting")
        # 标记任务完成
        time.sleep(10)

# 创建一个线程池，限制最大线程数为3
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    # 提交任务到线程池，并传入参数
    counter = increment_counter()
    for i in sorted_list:  # 假设有5个任务需要执行
        executor.submit(worker, i ,counter)

infoList = set(infoList)  # 去重得到唯一的URL列表
infoList = sorted(infoList)

with open("unicom-test.txt", 'w', encoding='utf-8') as file:
    for info in infoList:
        file.write(info + "\n")
        print(info)
    file.close()
