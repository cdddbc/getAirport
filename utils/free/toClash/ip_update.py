# from ip_update import geoip_update  #更新IP位置数据库,将此行放入需要引用的文件里使用'geoip_update()'即可用的文件里
# 默认下载位置 './Country.mmdb'---

from urllib import request          # Urllib是python内置的HTTP请求库,urllib.request获取URL的Python模块

#Country.mmdb 下载地址
geoip_url = 'https://raw.githubusercontent.com/Loyalsoldier/geoip/release/Country.mmdb'

#根据自己情况设置mmdb存放位置
countrymmdb_file = './Country.mmdb'

def geoip_update(url = geoip_url):                  # 更新IP位置数据库存放到  `./utils/Country.mmdb`
    print('Downloading Country.mmdb...')
    try:
        request.urlretrieve(url, countrymmdb_file)
        print('Downloading Country.mmdb Success!\n')
    except Exception:
        print('Downloading Country.mmdb Failed!\n')
        pass

if __name__ == '__main__':
    geoip_update(geoip_url)                           # 更新IP位置数据库
