import time
import requests
import json
import subprocess
from threading import Thread
from plugins import plugin_api, domain_ip_map
from conf import settings


class AgentHandler(object):
    def __init__(self):
        self.monitored_services = {}

    def load_latest_configs(self):
        """从server端加载最新的配置"""

        request_type = settings.configs['urls']['get_configs'][1]
        url = f"{settings.configs['urls']['get_configs'][0]}/{settings.configs['HostID']}"
        latest_configs = self.url_request(request_type, url)
        # latest_configs = json.loads(latest_configs)
        print(f'latest_configs=> {latest_configs}')
        self.monitored_services.update(latest_configs)

    def forever_run(self):
        """启动Agent相关逻辑"""

        exit_flag = False
        config_last_update_time = 0
        flush_domain_ip_time = 0
        while not exit_flag:
            if time.time() - config_last_update_time > settings.configs['ConfigUpdateInterval']:
                self.load_latest_configs()
                print('Loaded latest config: {}'.format(self.monitored_services))
                config_last_update_time = time.time()

            # 刷新域名和ip的对应关系
            if time.time() - flush_domain_ip_time > settings.configs['FlushDomainIPInterval']:
                self.flush_domain_ip_map()
                flush_domain_ip_time = time.time()

            for service_name, val in self.monitored_services['services'].items():
                # val: ['Linux_CPU_plugin', '60']  插件  更新间隔时间
                if len(val) == 2:  # 表示第一次执行监控
                    self.monitored_services['services'][service_name].append(0)

                monitor_interval = val[1]
                last_invoke_time = val[2]
                if time.time() - last_invoke_time > monitor_interval:  # 运行plugin
                    print('最近调用时间和当前时间', last_invoke_time, time.time())
                    self.monitored_services['services'][service_name][2] = time.time()
                    # 开一个线程调用监控插件
                    t = Thread(target=self.invoke_plugin, args=(service_name, val))
                    t.start()
                    print('开始监控服务: {}'.format(service_name))
                else:
                    continue
                # self.monitored_services['services'][service_name][2] = time.time()

    def invoke_plugin(self, service_name, val):
        """调用插件对应的函数，获取相关服务监控的内容"""

        # 获取cdn的ip信息
        """
        [{'cdn_name': 'kspush', 'cdn_domain': 'kspush.17zuoye.cn', 'cdn_ip': '123.135.106.65', 'from': 'Ali'}, 
        {'cdn_name': 'bspush', 'cdn_domain': 'bspush.17zuoye.cn', 'cdn_ip': '123.134.184.188', 'from': 'Ali'}, 
        {'cdn_name': 'www', 'cdn_domain': 'www.shuidibao.com', 'cdn_ip': '139.129.213.170', 'from': 'Ali'}]
        """
        infra_from = settings.configs['InfraFrom']
        ip_info_list = self.get_cdn_ip(infra_from)

        plugin_name = val[0]
        if hasattr(plugin_api, plugin_name):
            print('plugin_name=> {}'.format(plugin_name))
            func = getattr(plugin_api, plugin_name)
            ret_plugin_data = func(ip_info_list)  # 结果是字典 {'user': 0.2, 'nice': 0.9, 'status': 0}
            print("plugin里的函数返回的内容: {}".format(ret_plugin_data), type(ret_plugin_data))

            report_data = {
                "client_id": settings.configs['HostID'],
                "service_name": service_name,
                "data": json.dumps(ret_plugin_data)
            }

            request_type = settings.configs['urls']['service_report'][1]
            request_url = settings.configs['urls']['service_report'][0]

            print('invoke_plugin: 提交给server端的数据: {}'.format(report_data))
            ret_server_data = self.url_request(request_type, request_url, params=report_data)
            return 'post之后,server端返回的数据: {}'.format(ret_server_data)
        else:
            print('没有找到插件: {}'.format(plugin_name))
        print('--plugin 列表: {}'.format(val))

    def url_request(self, action, url, **extra_data):
        """根据不同的请求方法向server请求"""

        abs_url = "http://{}:{}/{}".format(settings.configs['Server'],
                                           settings.configs['ServerPort'],
                                           url)
        if action in ['get', 'GET']:
            print(abs_url, extra_data)
            try:
                response = requests.get(url=abs_url, timeout=settings.configs['RequestTimeout'])
                ret_data = response.json()
                print('callback data=> {}'.format(ret_data))
                return ret_data
            except:
                exit("get请求出错, exit_code{}".format(10))

        elif action in ['post', 'POST']:
            try:
                send_data = extra_data['params']
                response = requests.post(abs_url, data=send_data)
                ret_data = response.text
                print('ret_data 是=> {}'.format(ret_data))
                return ret_data

            except:
                exit('post请求出错, exit_code{}'.format(11))

    def get_cdn_ip(self, infra_from="m7"):
        # domain_list = ['kspush.17zuoye.cn', 'bspush.17zuoye.cn', 'push.17zuoye.cn']
        domain_list = settings.configs['DomainList']
        ip_list = []
        for cdn_domain in domain_list:
            shell_command = 'ping -c 2 %s -W 1' % (cdn_domain)
            result = subprocess.Popen(shell_command, shell=True, stdout=subprocess.PIPE).stdout.readlines()
            # 对结果进行解码
            new_result = list(map(lambda x: x.strip().decode('utf-8'), result))
            # print(new_result)

            """
            ['PING i975.v.bsclink.cn (123.134.184.188) 56(84) bytes of data.', 
            '64 bytes from 123.134.184.188 (123.134.184.188): icmp_seq=1 ttl=51 time=14.7 ms', 
            '64 bytes from 123.134.184.188 (123.134.184.188): icmp_seq=2 ttl=51 time=14.4 ms', 
            '', 
            '--- i975.v.bsclink.cn ping statistics ---', '2 packets transmitted, 2 received, 0% packet loss, time 1001ms', 
            'rtt min/avg/max/mdev = 14.495/14.640/14.786/0.189 ms']
            """
            # 获取cdn的名字，域名前缀就是
            cdn_name = cdn_domain.split('.')[0]
            # 获取cdn的ip地址
            cdn_ip = new_result[0].split(' ')[2][1:-1]
            value_dict = {
                "cdn_name": cdn_name,
                "cdn_domain": cdn_domain,
                "cdn_ip": cdn_ip,
                "from": infra_from
            }
            ip_list.append(value_dict)
        # print(ip_list)

        return ip_list

    def flush_domain_ip_map(self):
        ret_dict = domain_ip_map.domain_ip_map(settings.configs['DomainList'])
        data_dict = {}
        data_dict.setdefault(settings.configs['InfraFrom'], ret_dict)
        report_data = {
            "data": json.dumps(data_dict)
        }

        request_type = settings.configs['urls']['service_report_domain'][1]
        request_url = settings.configs['urls']['service_report_domain'][0]
        ret_server_data = self.url_request(request_type, request_url, params=report_data)
        print('The response data of server=> ', ret_server_data)
