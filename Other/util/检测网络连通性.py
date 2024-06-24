# -*- coding: utf-8 -*-
# @Time    : 2020/9/29 9:24
# @Author  : tmb
import os
import socket


def is_network_link(ip, port, timeout=10):
    """检测网络连通性

    Args:
        ip: IP地址
        port: 端口
        timeout: 超时时间
    Returns:
        boolean
    """
    try:
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(socket_client)
        socket_client.settimeout(timeout)
        socket_client.connect((ip, int(port)))
        socket_client.close()
    except socket.error as e:
        print(e)
        return False

    return True


def icmp_packet_link(ip_address, times):
    """

    :param ip_address: 地址
    :param times: ping的次数
    :return: 最小时延、平均时延、最大时延、丢包率
    """
    stdout = ''
    try:
        stdout = os.popen('ping -c ' + str(times) + ' ' + ip_address).read()
        stdout = stdout.strip('\n').split('\n')

        # if len(stdout) == int(times) + 5:
        if 'received' in stdout[-2] and 'loss' in stdout[-2] and 'min/avg/max/' in stdout[-1]:
            delay_info = stdout[-1].split(' ', 1)[1]
            delay_info = delay_info.split(' = ')
            delay_vals = delay_info[1].split('/')

            loss_info = stdout[-2].split(', ')[2]
            loss_info = loss_info.split(' ')[0].replace('%', '')

            if float(loss_info) < 40:
                return delay_vals[0], delay_vals[1], delay_vals[2], loss_info
    except Exception as e:
        pass
    return None, None, None, 100


def get_device_status_by_ip_port(ip, port, times=5):
    if is_network_link(ip, port):
        status = 1
        if int(icmp_packet_link(ip, times)[3]) >= 40:
            status = 0
    else:
        ret = icmp_packet_link(ip, times)
        status = 0 if int(ret[3]) >= 40 else 2  # 暂定丢包率>=40为离线
    return status


if __name__ == '__main__':
    print(is_network_link('192.168.10.33', '6379'))
