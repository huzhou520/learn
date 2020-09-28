#!/usr/bin/env python
# -*- coding:utf-8 -*-
import subprocess
from threading import Thread


def cdn_monitor(ip_info_list, first_invoke=1):
    """监控cdn节点的ping值"""

    ret_list = []
    for dic in ip_info_list:
        infra_from = dic['from']
        cdn_name = dic['cdn_name']
        cdn_domain = dic['cdn_domain']
        cdn_ip = dic['cdn_ip']

        t = Thread(target=excute_ping, args=(infra_from, cdn_name, cdn_domain, cdn_ip), kwargs={"ret_list": ret_list})
        t.start()
    t.join()
        # 0.5秒发送一个ping包，一共发送60个, 50s后超时
        # shell_command = 'ping -c 80 -i 0.5 %s -w 50|tail -2' % (cdn_ip)
        # result = subprocess.Popen(shell_command, shell=True, stdout=subprocess.PIPE).stdout.readlines()
        # print('subprocess result: {}'.format(result))
        #
        # # 获取指定的二条数据，方便接下来进行过滤
        # loss_line, rtt_line = map(lambda x: x.decode('utf-8').strip(), result)
        # # 获取丢包率
        # loss_rate = loss_line.split(' ')[5]
        # # 获取rtt_line里的部分字符串，然后进行分割
        # rtt_part_li = rtt_line.split(' ')[-2].split('/')
        # ping_min, ping_avg, ping_max = rtt_part_li[0], rtt_part_li[1], rtt_part_li[2]
        #
        # status = 0
        # if status != 0:
        #     status = 1
        #     value_dic = {'status': status}
        # else:
        #     value_dic = {
        #         'status': 0,
        #         'cdn_ip': cdn_ip,
        #         'loss_rate': loss_rate,
        #         'ping_min': ping_min,
        #         'ping_avg': ping_avg,
        #         'ping_max': ping_max,
        #         'from': infra_from,
        #         'cdn_name': cdn_name,
        #         'cdn_domain': cdn_domain
        #     }
        # # 添加每个ip的ping的结果数据到列表中
        # ret_list.append(value_dic)
    print('CDN的ret_list=> ', ret_list)
    """
    [{'status': 0, 'cdn_ip': '120.92.10.183', 'loss_rate': '0%', 'ping_min': '3.350', 
      'ping_avg': '4.168', 'ping_max': '6.193'}, 
     {'status': 0, 'cdn_ip': '140.143.217.157', 'loss_rate': '0%', 'ping_min': '2.541', 
       'ping_avg': '3.265', 'ping_max': '4.284'}]
    """
    return ret_list


def excute_ping(infra_from, cdn_name, cdn_domain, cdn_ip, ret_list):
    # 0.5秒发送一个ping包，一共发送60个, 50s后超时
    shell_command = 'ping -c 70 -i 0.5 %s -w 50|tail -2' % (cdn_ip)
    result = subprocess.Popen(shell_command, shell=True, stdout=subprocess.PIPE).stdout.readlines()
    print('subprocess result: {}'.format(result))

    # 获取指定的二条数据，方便接下来进行过滤
    loss_line, rtt_line = map(lambda x: x.decode('utf-8').strip(), result)
    # 获取丢包率
    loss_rate = loss_line.split(' ')[5]
    # 获取rtt_line里的部分字符串，然后进行分割
    rtt_part_li = rtt_line.split(' ')[-2].split('/')
    ping_min, ping_avg, ping_max = rtt_part_li[0], rtt_part_li[1], rtt_part_li[2]

    status = 0
    if status != 0:
        status = 1
        value_dic = {'status': status}
    else:
        value_dic = {
            'status': 0,
            'cdn_ip': cdn_ip,
            'loss_rate': loss_rate,
            'ping_min': ping_min,
            'ping_avg': ping_avg,
            'ping_max': ping_max,
            'from': infra_from,
            'cdn_name': cdn_name,
            'cdn_domain': cdn_domain
        }
    # 添加每个ip的ping的结果数据到列表中

    ret_list.append(value_dic)


if __name__ == '__main__':
    ret = cdn_monitor()
    print(ret)
