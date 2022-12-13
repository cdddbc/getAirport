import re, yaml
import time, os
from tqdm import tqdm   #进度条库
import threading  #线程
from ip_update import geoip_update  # 更新ip库Country.mmdb 
from sub_convert import sub_convert

#源文件
urllistfile = './config/sublist_mining'
#输出订阅文件位置
outputUrlSub_path = './sub/miningUrl'
outputBase64Sub_path =  './sub/miningUrl64'
outputClashSub_path = './sub/miningClash.yml' 
#转YAML需要用到的config.yml文件
config_file = './config/provider/config.yml'

class NoAliasDumper(yaml.SafeDumper): # https://ttl255.com/yaml-anchors-and-aliases-and-how-to-disable-them/
    def ignore_aliases(self, data):
        return True

def eternity_convert(file, config, output, provider_file_enabled=True):
    
    file_eternity = open(file, 'r', encoding='utf-8')
    sub_content = file_eternity.read()
    file_eternity.close()
    all_provider = sub_convert.main(sub_content,'content','YAML',custom_set={'dup_rm_enabled': True,'format_name_enabled': True})

    # 创建并写入 provider 
    lines = re.split(r'\n+', all_provider)
    
    all_proxy = []
    hk_proxy = []
    jp_proxy = []
    sg_proxy = []
    others_proxy = []

    for line in lines:
        if line != 'proxies:'  and 'plugin' not in line:
            line = '  ' + line  
            all_proxy.append(line)
            if 'HK' in line or '香港' in line:
                hk_proxy.append(line)
            elif 'JP' in line or '日本' in line:
                jp_proxy.append(line)
            elif 'SG' in line or '新加坡' in line:
                sg_proxy.append(line)
            else:
                others_proxy.append(line)
    allproxy_provider = 'proxies:\n' + '\n'.join(all_proxy)
    hk_provider = 'proxies:\n' + '\n'.join(hk_proxy)
    jp_provider = 'proxies:\n' + '\n'.join(jp_proxy)
    sg_provider = 'proxies:\n' + '\n'.join(sg_proxy)
    others_provider = 'proxies:\n' + '\n'.join(others_proxy)
     
    eternity_providers = {
            'all': allproxy_provider,
            'hk': hk_provider,
            'jp': jp_provider,
            'sg': sg_provider,
            'others': others_provider
        }

    # 创建完全配置的Eternity.yml
    config_f = open(config_file, 'r', encoding='utf-8')
    config_raw = config_f.read()
    config_f.close()
    
    config = yaml.safe_load(config_raw)
    all_provider_dic = {'proxies': []}
    hk_provider_dic = {'proxies': []}
    jp_provider_dic = {'proxies': []}
    sg_provider_dic = {'proxies': []}
    others_provider_dic = {'proxies': []}
    
    provider_dic = {
        'all': all_provider_dic,
        'hk': hk_provider_dic,
        'jp': jp_provider_dic,
        'sg': sg_provider_dic,
        'others': others_provider_dic
    }
    for key in eternity_providers.keys(): # 将节点转换为字典形式
        provider_load = yaml.safe_load(eternity_providers[key])
        provider_dic[key].update(provider_load)

    # 创建节点名列表
    all_name = []   
    hk_name = []
    jp_name = [] 
    sg_name = []
    others_name = []    
    
    name_dict = {
        'all': all_name,
        'hk': hk_name,
        'jp': jp_name,
        'sg': sg_name,
        'others': others_name     
    }
    for key in provider_dic.keys():
        if not provider_dic[key]['proxies'] is None:
            for proxy in provider_dic[key]['proxies']:
                name_dict[key].append(proxy['name'])
        if provider_dic[key]['proxies'] is None:
            name_dict[key].append('DIRECT')
    # 策略分组添加节点名
    proxy_groups = config['proxy-groups']
    proxy_group_fill = []
    for rule in proxy_groups:
        if rule['proxies'] is None: # 不是空集加入待加入名称列表
            proxy_group_fill.append(rule['name'])
    for rule_name in proxy_group_fill:
        for rule in proxy_groups:
            if rule['name'] == rule_name:
                rule.update({'proxies': all_name})
                
                if '香港' in rule_name:
                    rule.update({'proxies': hk_name})
                elif '日本' in rule_name:
                    rule.update({'proxies': jp_name})
                elif '狮城' in rule_name or '新加坡' in rule_name:
                    rule.update({'proxies': sg_name})
                elif '其他节点' in rule_name:
                    rule.update({'proxies': others_name})
                else:
                    rule.update({'proxies': all_name})
                    
    config.update(all_provider_dic)
    config.update({'proxy-groups': proxy_groups})

    config_yaml = yaml.dump(config, default_flow_style=False, sort_keys=False, allow_unicode=True, width=750, indent=2, Dumper=NoAliasDumper)
    
    Eternity_yml = open(output, 'w+', encoding='utf-8')
    Eternity_yml.write(config_yaml)
    Eternity_yml.close()
   
def sub_to_url(url,bar,allProxy):   #将url订阅内容append到allProxy列表，并完成进度bar
    if 'http' in url:
        subContent =sub_convert.convert_remote(url,'url','http://127.0.0.1:25500')        
        allProxy.append(subContent)
    bar.update(1)


def urlListToSub(urllistfile):  #将url订阅列表内容转换成url,base64,clash文件保存
    
    #打开url列表文件
    file_urllist = open(urllistfile, 'r', encoding='utf-8')
    urllist_content = file_urllist.read()
    file_urllist.close()
    
    #打开url列表文件内容，以行为单位存放到line列表
    lines = re.split(r'\n+',urllist_content)
    allProxy = []
    
    #计算打印url总数
    lenlines =len(lines)
    print('airport total == '+str(lenlines)+'\n')
    
    #Semaphore 是用于控制进入数量的锁，控制同时进行的线程，内部是基于Condition来进行实现的
    #https://www.cnblogs.com/callyblog/p/11147456.html
    #文件， 读、写， 写一般只是用于一个线程写，读可以允许有多个
    thread_max_num =threading.Semaphore(lenlines)
    
    #进度条添加
    bar = tqdm(total=lenlines, desc='订阅获取：')
    thread_list = []
    
    for line in lines:
        #为每个新URL创建线程
        t = threading.Thread(target=sub_to_url, args=(line,bar,allProxy))
        #加入线程池
        thread_list.append(t)
        #setDaemon()线程守护，配合下面的一组for...t.join(),实现所有线程执行结束后，才开始执行下面代码
        t.setDaemon(True)	#python多线程之t.setDaemon(True) 和 t.join()  https://www.cnblogs.com/my8100/p/7366567.html
		#启动
        t.start()
        
    #等待所有线程完成，配合上面的t.setDaemon(True)
    for t in thread_list:
        t.join()
    bar.close() #进度条结束
    
    # 将列表内容，以行写入字符串？
    ownallProxy = '\n'.join(allProxy)   

    # 写入url 订阅文件
    print('write miningUrl content!')
    file = open(outputUrlSub_path, 'w', encoding= 'utf-8')
    file.write(ownallProxy)
    file.close()

    # 写入base64 订阅文件
    subContent = sub_convert.base64_encode(ownallProxy)
    print('write miningUrl64 content!')
    file = open(outputBase64Sub_path, 'w', encoding= 'utf-8')
    file.write(subContent)
    file.close()

   # 写入Clash 订阅文件
    print('write miningClash begin!')
    eternity_convert(outputBase64Sub_path, config_file,    output=outputClashSub_path)
    print('write miningClash Over!')

if __name__ == '__main__':
    #更新IP库
    geoip_update('https://raw.githubusercontent.com/Loyalsoldier/geoip/release/Country.mmdb')
    urlListToSub(urllistfile)


