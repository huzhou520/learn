#!/usr/bin/env python
#coding:utf-8

# yum install sysstat

import subprocess


def cpu_monitor(first_invoke=1):
    shell_command = 'sar 1 3| grep "^Average:"'
    #status, result = subprocess.Popen(shell_command, shell=True, stdout=subprocess.PIPE).stdout.read()
    result = subprocess.Popen(shell_command, shell=True, stdout=subprocess.PIPE).stdout.read()
    #print('subprocess结果status=> ', status)
    print('subprocess结果result=> ', result)

    status = 0
    if status != 0:
        status = 1
        value_dic = {'status': status}
    else:  # data is correct
        value_dic = {}
        # user, nice, system, iowait, steal, idle = result.split()[2:]
        user, nice, system, iowait, steal, idle = map(lambda x: x.decode('utf-8'), result.split()[2:])
        value_dic = {
            'user': user,
            'nice': nice,
            'system': system,
            'iowait': iowait,
            'steal': steal,
            'idle': idle,
            'status': status
        }
    return value_dic

