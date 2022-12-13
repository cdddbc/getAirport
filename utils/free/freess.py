import re
import yaml
import urllib
import requests,random,string
# config.yaml配置文件地址
config_file_path = './utils/free/config.yaml'
out_list_file_path = './config/sublist_free'
out_freesub_path = "./sub/free/"
'''
"name":"www.kuaicloud.xyz",
"url":'https://www.kuaicloud.xyz/',
"reg_url":"https://www.kuaicloud.xyz/auth/register",
"sub":"https://www.kuaicloud.xyz/link/1y9vD5mYIdpNjmxJ?sub=3&extend=1"
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
        self._login_url = ''
        self._user_url = ''
        self._sub=''
    
    def set_env(self):   # 设置注册地址和获取sub的地址的模板链接
        self._name = urllib.parse.urlparse(self._url).netloc    # 网站名字获取
        self._reg_url = self._url+'auth/register'   # 注册地址
        self._login_url = self._url+'auth/login'    # 登录地址
        self._user_url = self._url+'user'           # 用户界面地址

    def register(self,email,password):  # 注册账号
        headers= {
            "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
            "referer": self._reg_url
        }
        data={
            "email":email,
            "name":password,
            "passwd":password,
            "repasswd":password,
            "invite_code":None,
            "email_code":None
        }
        geetest={
                "geetest_challenge": "98dce83da57b0395e163467c9dae521b1f",
                "geetest_validate": "bebe713_e80_222ebc4a0",
                "geetest_seccode": "bebe713_e80_222ebc4a0|jordan"}
        data.update(geetest)
        with requests.session() as session:
            resp = session.post(self._reg_url,headers=headers,data=data,timeout=5,proxies=self._proxies)
            print(resp.json())

            data ={
                'email': email,
                'passwd': password,
                'code': '',
                'remember_me': 1,
            }
            try:
                resp = session.post(self._login_url,headers=headers,data=data,timeout=5,proxies=self._proxies)
                print(resp.json())
            except:
                pass

            resp = session.get(self._user_url,headers=headers,timeout=5,proxies=self._proxies)
            # print(resp.text)
            try:
                token= re.search("https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+sub=3", resp.text).group(0)
            except:
                token = re.search("https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+clash=1", resp.text).group(0)
            self._sub = token
            print(token)
        return token    # 返回解析完的订阅地址

        
    def getSubscribe(self):  # 注册url网站账号，返回sub订阅地址
        password=''.join(random.sample(string.ascii_letters + string.digits + string.ascii_lowercase, 10))
        email=password+"@gmail.com"
        subscribe=self.register(email,password) 
        return subscribe    # 返回刚注册账号的订阅地址

    def save_conf(self):    # 注册账号，获取订阅内容，写入list_file_path地址文件和./free/内容文件夹
        sub_url=self.getSubscribe() # 注册url网站账号，返回sub订阅地址
        #retry
        for k in range(3):
            try:
                req=requests.get(sub_url,timeout=5) # 获取订阅内容
                v2conf=req.text              # 将订阅内容的节点信息赋值v2conf
                with open(out_list_file_path, 'a') as f:
                    f.write(sub_url+'\n')            # 将订阅地址写入sub_url文件
                break
            except:
                v2conf=""
        with open(out_freesub_path+self._name,"w") as f:
                    f.write(v2conf)                  # 根据获取的网站名称将订阅内容写入./free/目录下的网站名文件里面

def get_conf():     # 根据config.yaml里面的地址，注册新账号获取订阅
    with open(config_file_path,encoding="UTF-8") as f:  # 获取config地址内容
        data = yaml.load(f, Loader=yaml.FullLoader)
    url_list = data['SSpanel']       # 将SSpanel格式网站地址取出到url_list
    for url in url_list:                #读取url_list的地址
        sub = tempsite(url)             # 定义一个sub名字的tempsite()类，默认初始化类_init_(self，url，proxy = None)
        try:
            sub.set_env()           # 设置注册地址和获取sub的地址的模板链接
            sub.save_conf()          # 注册账号，获取订阅内容，写入./sub_list地址文件和./free/内容文件夹
        except:
            pass  

# get_conf()
