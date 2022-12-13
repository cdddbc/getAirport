import re
import requests
import threading
import time
import requests
from tqdm import tqdm
from retry import retry
from datetime import datetime

#check列表的位置
urllist_path = './config/sublist_mining'

def list_rm(url_list):  #列表去重
    begin = 0
    length = len(url_list)
    print(f'\n-----去重开始-----\n')
    while begin < length:
        proxy_compared = url_list[begin]
        begin_2 = begin + 1
        while begin_2 <= (length - 1):
            if proxy_compared == url_list[begin_2]:
                url_list.pop(begin_2)
                length -= 1
            begin_2 += 1
        begin += 1
    print(f'\n-----去重结束-----\n')
    return url_list
    
def sub_check(url,bar):
    headers = {'User-Agent': 'ClashforWindows/0.18.1'}
    with thread_max_num:
        @retry(tries=3)
        def start_check(url):
            res=requests.get(url,headers=headers,timeout=5)#设置5秒超时防止卡死
            if res.status_code == 200:
                try: #有流量信息
                    info = res.headers['subscription-userinfo']
                    info_num = re.findall('\d+',info)
                    time_now=int(time.time())
                    # 剩余流量大于10MB
                    if int(info_num[2])-int(info_num[1])-int(info_num[0])>10485760:
                        if len(info_num) == 4: # 有时间信息
                            if time_now <= int(info_num[3]): # 没有过期
                                new_list.append(url)
                            else: # 已经过期
                                old_list.append(url)
                        else: # 没有时间信息
                            new_list.append(url)
                    else: # 流量小于10MB
                        old_list.append(url)       
                except:
                    old_list.append(url)  
                # output_text='无流量信息捏'
            else:
                old_list.append(url)
        try:
            start_check(url)
        except:
            old_list.append(url)
        bar.update(1)

if __name__=='__main__':
    new_list = []
    old_list = []
    with open(urllist_path, 'r') as f:
        data = f.read()
    url_list=re.findall("https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]",data)#使用正则表达式查找订阅链接并创建列表
    url_list=list_rm(url_list)    # 去重
    # url_list = data.split() :list
    thread_max_num =threading.Semaphore(32) #32线程
    bar = tqdm(total=len(url_list), desc='订阅筛选：')
    thread_list = []
    for url in url_list:
        #为每个新URL创建线程
        t = threading.Thread(target=sub_check, args=(url,bar))
        #加入线程池并启动
        thread_list.append(t)
        t.setDaemon(True)
        t.start()
    for t in thread_list:
        t.join()
    bar.close()
    with open(urllist_path,"w+") as f:
        # str = '\n'
        # f.write(str.join(list))
        for url in new_list:
            f.write(url+'\n')
"""         
    with open("./logs/old/old","a") as f:
        for url in old_list:
            f.write(url+'\n')
    with open("./logs/old/time","w",encoding="UTF-8") as f:
        currentTime = datetime.now().strftime("%Y-%m-%d\t%H:%M:%S")
        f.write('更新时间:\t'+currentTime+'\n')
 """           
