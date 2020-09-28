# import cpu, network
from plugins import cpu, network, cdn, rtmp_port


def Linux_CPU_plugin():
    return cpu.cpu_monitor()


def Linux_Network_plugin():
    return network.network_monitor()


def CDN_State_plugin(ip_info_list):
    return cdn.cdn_monitor(ip_info_list)


def Rtmp_Port_plugin(ip_info_list):
    return rtmp_port.rtmp_port_monitor(ip_info_list)
