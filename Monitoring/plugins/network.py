#!/usr/bin/env python
# -*- coding:utf-8 -*-
import subprocess


def network_monitor(first_invoke=1):
    shell_command = 'sar -n DEV 1 5 |grep -v IFACE |grep Average'
    result = subprocess.Popen(shell_command, shell=True, stdout=subprocess.PIPE).stdout.readlines()
    print('subprocess result: {}'.format(result))

    value_dic = {'status': 0, 'data': {}}
    for line in result:
        line = line.split()
        nic_name, t_in, t_out = line[1], line[4], line[5]
        # 调试
        nic_name = nic_name.decode('utf-8')
        t_in = t_in.decode('utf-8')
        t_out = t_out.decode('utf-8')
        print(f't_in=> {t_in}', f't_out=> {t_out}')
        #value_dic['data'][nic_name] = {"t_in": line[4], "t_out": line[5]}
        value_dic['data'][nic_name] = {"t_in": t_in, "t_out": t_out}

    # print(value_dic)
    return value_dic
