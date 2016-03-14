#!/usr/bin/env python
# coding=utf-8
import argparse
from socket import socket

from gevent.pool import Pool
import gevent
from gevent import monkey
monkey.patch_all()


open_ports = []


def scan_a_host(host, ports):
    pool = Pool(15)
    for port in ports:
        pool.spawn(scan_a_port, host, port)
    gevent.wait()
    return open_ports


def scan_a_port(host, port):
    _socket = socket()
    _socket.settimeout(5)
    result = _socket.connect_ex((host, port))
    if result == 0:
        open_ports.append(port)
        print('port: {} is a open port!'.format(port))
    _socket.close()


def prep_args():
    parser = argparse.ArgumentParser(
        description='Scan open ports of a given host and a range of ports')
    parser.add_argument('--host', help='ip or hostname of the host')
    parser.add_argument('-p', '--ports', help='ports range, be separeted by -, e.g. 1-1000')
    args = parser.parse_args()
    host = args.host
    start_p, end_p = map(int, args.ports.split('-'))
    ports = range(start_p, end_p+1)
    return host, ports


if __name__ == '__main__':
    host, ports = prep_args()
    open_ports = scan_a_host(host, ports)
    print('The open ports: {}'.format(open_ports))
