#!/usr/bin/env python
# coding:utf-8
import subprocess

DomainList = ["push.17zuoye.cn", "video-center-bj.alivecdn.com","tcpush.17zuoye.cn", "kspush.17zuoye.cn"]


def domain_ip_map(DomainList):
    domain_ip_map_dict = {}
    for domain in DomainList:
        # shell_command = "dig -t A bspush.17zuoye.cn | awk '/^[a-z]/ {print $5}' | awk '/^[[:digit:]]/{print $1}'"
        shell_command = "dig -t A %s | awk '/^[a-z]/ {print $5}' | awk '/^[[:digit:]]/{print $1}'" % (domain)
        result = subprocess.Popen(shell_command, shell=True, stdout=subprocess.PIPE).stdout.read()
        print('subprocess结果result=> ', result)

        # ret = map(lambda x: x, result.decode('utf-8').split('\n'))
        ip_list = result.decode('utf-8').strip().split('\n')
        domain_ip_map_dict.setdefault(domain.split('.')[0], ip_list)
    print(domain_ip_map_dict)
    return domain_ip_map_dict


if __name__ == '__main__':
    domain_ip_map(DomainList)
