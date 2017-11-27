#!/usr/bin/env python
#encoding:utf-8

import SocketServer
import configure
from process import *

s = None

class DNSHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # 若缓存队列没有存满，把接收到的包放进缓存队列中（存满则直接丢弃包）
        if not s.qcache.full():
            # 缓存队列保存元组：(请求包，请求地址，sock)
            print 'client addr: %s' % type(self.client_address)
            msg = QMessage(self.request[0], self.client_address, self.request[1])
            s.qcache.put(msg)

class DNSServer(object):
    def __init__(self, config):
        self.conf = config
        self.ip = config.GetItem("ip")
        self.port = int(config.GetItem("port"))
        self.deq_size = int(config.GetItem("deq_size"))

        # 缓存队列，收到的请求都先放在这里，然后从这里拿数据处理
        self.qcache = CreateQueue(self.deq_size)

        self.processor = CreateProcessor(config)

    def start(self):
        # 启动协程，循环处理缓存队列
        ProcessQueue(self.qcache, self.processor)

        # 启动DNS服务器
        print 'Start DNS server at %s:%d\n' % (self.ip, self.port)
        dns_server = SocketServer.UDPServer((self.ip, self.port), DNSHandler)
        dns_server.serve_forever()

def main():
    # 读取配置文件
    config = configure.DNSConfigure(None)

    # 启动服务器
    global s
    s = DNSServer(config)
    s.start()

if __name__ == '__main__':
    #import pdb
    #pdb.set_trace()

    main()

