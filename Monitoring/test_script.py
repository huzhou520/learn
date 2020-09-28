# import plugin_api
import json

# service_name = 'Linux_CPU_plugin'

# if hasattr(plugin_api, service_name):
#     func = getattr(plugin_api, service_name)
#     ret_plugin_data = func  # 结果是字典
#     # print("plugin里的函数返回的内容: {}".format(ret_plugin_data))
#     print("plugin里的函数返回的内容: {}".format(ret_plugin_data))


# ret = {'status': 0, 'data': {b'eth0': {'t_in': b'0.30', 't_out': b'0.82'}, b'lo': {'t_in': b'0.03', 't_out': b'0.03'}}}
# ret_dumps = json.dumps(ret)
#
# print(type(ret))
# print(type(ret_dumps))

# b1 = b'0.96'
# print(b1)
# b2 = b1.decode('utf-8')
# print(b2, type(b2))
# print(str(b1), type(str(b1)))

# li = [b'0.44', b'0.95', b'10.88']
# ret = map(lambda x: x.decode('utf-8'), li)
# print(ret)
# print(list(ret))

# dict1 = {'status': '0', 'cdn_ip': '123.135.106.69', 'loss_rate': '0%', 'ping_min': '13.414', 'ping_avg': '14.095',
#       'ping_max': '14.789', 'from': 'm7', 'cdn_name': 'kspush', 'cdn_domain': 'kspush.17zuoye.cn'}
#
# for k,v in dict1.items():
#       if v.isalpha():
#             print(v)
#       else:
#             continue
import subprocess

cdn_ip = ['120.92.10.183']
shell_command = 'ping -c 20 %s -W 1' % (cdn_ip)
result = subprocess.Popen(shell_command, shell=True, stdout=subprocess.PIPE).stdout.readlines()
print(result[0].decode('gbk'))