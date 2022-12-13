import yaml
import urllib
# import requests,random,string
from datetime import datetime
import requests,random,string

# config.yaml配置文件地址
config_file_path = './utils/free/config.yaml'
out_list_file_path = './config/sublist_free'
out_freesub_path = "./sub/free/"

'''
"name":"feiniao",
"url":"https://feiniaoyun.xyz/",
"reg_url":"https://feiniaoyun.xyz/api/v1/passport/auth/register",
"sub":"https://feiniaoyun.xyz/api/v1/client/subscribe?token={token}"
'''

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

class tempsite():   
    def __init__(self,url,proxy=None):  # 注册信息模板
        self._proxies = proxy
        self._name=''
        self._url = url
        self._reg_url=''
        self._sub=''
    
    def set_env(self):  # 设置注册地址和获取sub的地址的模板链接
        self._name = urllib.parse.urlparse(self._url).netloc    # 网站名字获取
        self._reg_url = self._url+'api/v1/passport/auth/register'   # 注册地址
        self._sub = self._url+'api/v1/client/subscribe?token={token}'   # 获取sub的地址的模板链接

    def register(self,email,password):  # 注册账号
        headers= {
            "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
            "Refer": self._url
        }
        data={
            "email":email,
            "password":password,
            "invite_code":None,
            "email_code":None
        }
        req=requests.post(self._reg_url,headers=headers,data=data,timeout=5,proxies=self._proxies)  # 注册
        return req
        
    def getSubscribe(self): # 注册url网站账号，返回sub订阅地址
        password=''.join(random.sample(string.ascii_letters + string.digits + string.ascii_lowercase, 10))
        email=password+"@gmail.com"
        req=self.register(email,password)   #根据email 和 password 注册账号
        token=req.json()["data"]["token"]   # 获取token
        subscribe=self._sub.format(token=token) # 将获取的token传给self._sub 里面的{token} 字段
        return subscribe    # 返回刚注册账号的订阅地址

    def save_conf(self):    # 注册账号，获取订阅内容，写入./sub_list地址文件和./free/内容文件夹
        sub_url=self.getSubscribe() # 注册url网站账号，返回sub订阅地址
        #retry
        for k in range(3):
            try:
                req=requests.get(sub_url,timeout=5) # 获取订阅内容
                v2conf=req.text # 将订阅内容的节点信息赋值v2conf
                with open(out_list_file_path, 'a') as f:
                    f.write(sub_url+'\n')   # 将订阅地址写入sub_url文件
                break
            except:
                v2conf=""
        with open(out_freesub_path+self._name,"w") as f:
                    f.write(v2conf)     # 根据获取的网站名称将订阅内容写入./free/目录下的网站名文件里面

def get_conf():     # 根据config.yaml里面的地址，注册新账号获取订阅
    currentTime = datetime.now().strftime("%Y-%m-%d\t%H:%M:%S") # 获取现在的时转成字符串
    with open(out_list_file_path,'w',encoding="UTF-8") as fp:     # 打开写入文件
        fp.write('更新时间:\t'+currentTime+'\n')            # 在写入的文件开头写入更新时间
    with open(config_file_path,encoding="UTF-8") as f: # 获取config地址内容
        data = yaml.load(f, Loader=yaml.FullLoader)
    url_list = data['V2board']  # 将V2board格式网站地址取出到url_list
    for url in url_list:        #读取url_list的地址
        sub = tempsite(url)     # 定义一个sub名字的tempsite()类，默认初始化类_init_(self，url，proxy = None)
        try:
            sub.set_env()       # # 设置注册地址和获取sub的地址的模板链接
            sub.save_conf()     # 注册账号，获取订阅内容，写入./sub_list地址文件和./free/内容文件夹
        except:
            pass                # 有什么问题直接pass

# get_conf()
