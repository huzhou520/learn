#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

def rtmp_port_monitor(ip_info_list, port=1935):
    """监控rtmp服务的端口1935"""

    # 过滤出域名对应的cdn ip地址
    # cdn_list = [dic['cdn_ip'] for dic in ip_info_list]
    ret_list = []
    for dic in ip_info_list:
        shell_command = 'nc -zv %s %s' % (dic['cdn_ip'], port)
        result = os.system(shell_command)
        print('subprocess result: {}'.format(result))

        if result == 0:
            value_dic = {
                'status': 0,
                'from': dic['from'],
                'cdn_domain': dic['cdn_domain'],
                'cdn_ip': dic['cdn_ip'],
                'port': port,
                'msg': 'Port OK!'
            }
            ret_list.append(value_dic)
        else:
            value_dic = {
                'status': 1,
                'from': dic['from'],
                'cdn_domain': dic['cdn_domain'],
                'cdn_ip': dic['cdn_ip'],
                'port': port,
                'msg': 'Port Failed!'
            }
            ret_list.append(value_dic)

    return ret_list
    # # 过滤出域名对应的cdn ip地址
    # cdn_list = [dic['cdn_ip'] for dic in ip_info_list]
    # # cdn_list = ['10.200.242.55', '123.134.184.187']
    # ret_list = []
    # for cdn_ip in cdn_list:
    #     shell_command = 'nc -zv %s %s' % (cdn_ip, port)
    #     result = os.system(shell_command)
    #     print('subprocess result: {}'.format(result))
    #
    #     if result == 0:
    #         value_dic = {
    #             'status': 0,
    #             'cdn_ip': cdn_ip,
    #             'port': port,
    #             'msg': 'Port OK!'
    #         }
    #         ret_list.append(value_dic)
    #     else:
    #         value_dic = {
    #             'status': 1,
    #             'cdn_ip': cdn_ip,
    #             'port': port,
    #             'msg': 'Port Failed!'
    #         }
    #         ret_list.append(value_dic)
    #
    # return ret_list


if __name__ == '__main__':
    ret = rtmp_port_monitor('10.10.10.10')
    print(ret)

