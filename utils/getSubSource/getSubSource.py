import re, yaml
import time, os
import sys
import datetime
from urllib import request 

source_sublist_path = './config/subsource/subsource.yaml'
free_sublist_path = './config/sublist_mining'


def get_subSource():     # 
    with open(source_sublist_path,encoding="UTF-8") as f: # 获取config地址内容
        data = yaml.load(f, Loader=yaml.FullLoader)
    url_list = data['机场订阅']  # 将free_V2board_sspanel格式网站地址取出到url_list
    new_url_list = []
    for url in url_list:        #读取url_list的地址
        new_url_list.append(url)
    free_list = '\n'.join(new_url_list)
    with open(free_sublist_path,'a',encoding="UTF-8") as fp:     # 打开写入文件
        fp.write(free_list)
		
def sublist_update(sourceSublist):                  # 
    print('Downloading sublist...')
    try:
        request.urlretrieve(sourceSublist, source_sublist_path)
        print('Downloading sublist Success!\n')
    except Exception:
        print('Downloading sublist Failed!\n')
        pass

def GetSublistUrl():
    today = datetime.datetime.today()
    path_base = 'https://raw.githubusercontent.com/rxsweet/collectSub/main/sub/'
    path_year = str(today.year)
    path_mon = path_year+'/'+str(today.month)
    path_yaml = path_base+'/'+path_mon+'/'+str(today.month)+'-'+str(today.day)+'.yaml'
    return path_yaml

if __name__ == '__main__':
    
    # 下载最新sublist源
    urllistsource = GetSublistUrl() # 获取subsource地址
    print(urllistsource)
    sublist_update(urllistsource)
    get_subSource()
