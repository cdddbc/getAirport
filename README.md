# getAirport

## copy source

> copy [RenaLio/Mux2sub](https://github.com/RenaLio/Mux2sub)

## 功能

> 1.获取网络分享的airport订阅地址 
> 
> 2.测试订阅地址的可用性
> 
> 3.将可用订阅地址转成订阅 
> 
> 其它功能: 抓取免费airport

## 仓库文档
<details>
  <summary>展开查看仓库文档</summary>
  
```
fetchPorxy.main
├── .github──workflows──getSub.yml(actions Deploy)
├── config
│   ├── provider──config.yml(转clash订阅用的配置)
│   ├── subsource──subsource.yaml(网络获取的订阅源)
│   ├── sublist_free.json(免费airport订阅列表) 
│   └── sublist_mining.json(爬取的可用订阅列表) 	
├── sub
│   ├── free(免费airport订阅)
│   │   ├── clash---(clash格式订阅)
│   │   ├── test---(test新资源)
│   │   └── 其它v2ray订阅
│   ├── miningUrl(未测速节点合集url格式)
│   ├── miningUrl64(未测速合集base64格式)
│   └── miningClash.yml(未测速合集Clash格式)
├── utils(程序功能模块)
│   ├── getSubSource──getSubSource.py((获取爬取到的订阅源文件放入'./config/source/subsource.yaml'))
│   ├── checkUrllist
│   │   ├── check.py(检测订阅源列表的可用性)
│   │   ├── ip_update.py(下载country.mmdb文件)
│   │   ├── urllist2sub.py(转换节点文件到'./sub/'目录下的订阅文件)
│   │   └── sub_convert.py(转换订阅格式的功能模块)
│   ├── free(获取免费airport)
│   │   ├── myUseClash ---(获取自用clash)
│   │   ├── test ---(测试新的airport)
│   │   ├── config.yaml(免费airport网站列表)
│   │   ├── main.py(主程序开始)
│   │   ├── freev2.py(获取'V2board'网站Gmail注册订阅)
│   │   ├── qqfreev2.py(获取'V2board'网站QQ邮箱注册订阅)
│   │   └── freess.py(获取'SSpanel'网站订阅)
│   └── requirements.txt(依赖库)
└── README.md
```
</details>

### 使用注意
>转码功能用到的`subconverter工具`
>
>IP库`country.mmdb`
>
>已备份到'rx/all/githubTools'

## 仓库声明
订阅节点仅作学习交流使用，只是对网络上节点的优选排序，用于查找资料，学习知识，不做任何违法行为。所有资源均来自互联网，仅供大家交流学习使用，出现违法问题概不负责。
