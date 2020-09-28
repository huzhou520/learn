# Agent配置文件
import time

configs = {
    "HostID": 3,  # ID
    "Server": "10.6.13.230",  # Specify Server host
    "ServerPort": 81,  # 连接服务器的端口
    "urls": {
        "get_configs": ["api/client/config", "get"],  # Get all of the services
        # server端的post
        "service_report": ["api/client/service/report/", "post"],
        # 接受域名ip的对应关系
        "service_report_domain": ["api/client/service/report/domain_ip_map/", "post"],
    },
    "RequestTimeout": 30,
    "ConfigUpdateInterval": 300,  # 5 minutes as default
    "FlushDomainIPInterval": 86400,  # A whole day as default
    "InfraFrom": "m7",  # 配置机房位置 Ali或者m7
    # CDN域名配置
    "DomainList": ["push.17zuoye.cn", "video-center-bj.alivecdn.com",
                   "tcpush.17zuoye.cn", "kspush.17zuoye.cn",
                   "bspush.17zuoye.cn", "ucpush.17zuoye.cn"],
    "NodeList": ["120.92.10.183"],
    # 要监听的端口
    "MonitorPort": {"rtmp_port": 1935}
}
