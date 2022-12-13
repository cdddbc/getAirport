import yaml
import urllib
from bs4 import BeautifulSoup
import requests,random,string

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
    def __init__(self,url,proxy=None):
        self._proxies = proxy
        self._name=''
        self._url = url
        self._reg_url=''
        self._login_url = ''
        self._user_url = ''
        self._sub=''
    
    def set_env(self):
        self._name = urllib.parse.urlparse(self._url).netloc
        self._reg_url = self._url+'auth/register'
        self._login_url = self._url+'auth/login'
        self._user_url = self._url+'user'

    def register(self,email,password):
        headers= {
            "User-Agent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
            "referer": self._reg_url
        }
        data={
            "email":email,
            "name":self._name,
            "passwd":password,
            "repasswd":password,
            "invite_code":None,
            "email_code":None
        }
        with requests.session() as session:
            resp = session.post(self._reg_url,headers=headers,data=data,timeout=5,proxies=self._proxies)
            print(resp.json())
            data ={
                'email': email,
                'passwd': password,
                'code': '',
                'remember_me': 1,
            }
            resp = session.post(self._login_url,headers=headers,data=data,timeout=5,proxies=self._proxies)
            print(resp.json())
            resp = session.get(self._user_url,headers=headers,timeout=5,proxies=self._proxies)
            # print(resp.text)
            page = BeautifulSoup(resp.text,'html.parser')
            token = page.find("a",class_='btn btn-icon icon-left btn-primary btn-v2ray copy-text btn-lg btn-round')['data-clipboard-text']
            self._sub = token
            print(token)
        return token

        
    def getSubscribe(self):
        password=''.join(random.sample(string.ascii_letters + string.digits + string.ascii_lowercase, 10))
        email=password+"@gmail.com"
        subscribe=self.register(email,password)
        return subscribe

    def save_conf(self):
        sub_url=self.getSubscribe()
        #retry
        for k in range(3):
            try:
                req=requests.get(sub_url,timeout=5)
                v2conf=req.text
                with open('./sub_list', 'a') as f:
                    f.write(sub_url+'\n')
                break
            except:
                v2conf=""
        with open("./free/"+self._name,"w") as f:
                    f.write(v2conf)

def get_conf():
    with open('./utils/config.yaml',encoding="UTF-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    url_list = data['SSpanel']
    for url in url_list:
        sub = tempsite(url)
        try:
            sub.set_env()
            sub.save_conf()
        except:
            pass  

# get_conf()
