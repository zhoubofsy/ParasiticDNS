#!/usr/bin/env python
#encoding:utf-8

import gevent
from gevent import monkey

monkey.patch_all()
from gevent.queue import Queue
import pylru
import dnslib
import re
import backends

class QMessage(object):
    def __init__(self, data, addr, sock):
        self.raw_data = data
        self.addr = addr
        self.sock = sock
        self.dns_data = None
        self.response = None


class DNSProcessor(object):
    def __init__(self, config):
        self.conf = config
        self.lru_size = int(config.GetItem("lru_size"))
        # LRU Cache，使用近期最少使用覆盖原则
        self.dns_cache = pylru.lrucache(self.lru_size)
        # backend
        self.bktype = config.GetItem("backend")
        self.bkend = backends.CreateBackend(self.conf, self.bktype)

    def Predo(self, msg):
        try:
            dns = dnslib.DNSRecord.parse(msg.raw_data)
            msg.dns_data = dns
        except Exception as e:
            print 'Not a DNS Packet.\n', e

    def Doing(self, msg):
        #import pdb
        #pdb.set_trace()
        dns = msg.dns_data
        if dns != None:
            dns.header.set_qr(dnslib.QR.RESPONSE)
            # 获得请求域名
            qname = dns.q.qname
            # 在LRUCache中查找缓存过域名的DNS应答包
            response = self.dns_cache.get(qname)
            print 'qname =', qname, 'response =', response

            if response:
                # 若应答已在缓存中，直接替换id后返回给用户
                response[:2] = msg.raw_data[:2]
                self.response = response
            else:
                # 若应答不在缓存中，从db中查询（这里只用了一个简单的文件供演示）
                self.bkend.Prepare()
                answers, soa = self.bkend.Query(str(qname).rstrip('.'))
                answer_dns = self.pack_dns(dns, answers, soa)

                # 将查询到的应答包放入LRUCache以后使用
                self.dns_cache[qname] = answer_dns.pack()

                self.response = answer_dns.pack()

    def Done(self, msg):
        sock = msg.sock
        addr = msg.addr
        if self.response != None and sock != None and addr != None:
            sock.sendto(self.response, addr)

    def pack_dns(self, dns, answers, soa=None):
        content_type = lambda x: 'A' if re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', x) else 'CNAME'
        if answers:
            for ans in answers:
                if content_type(ans[1]) == 'A':
                    dns.add_answer(dnslib.RR(ans[0], dnslib.QTYPE.A, rdata=dnslib.A(ans[1])))
                elif content_type(ans[1]) == 'CNAME':
                    dns.add_answer(dnslib.RR(ans[0], dnslib.QTYPE.CNAME, rdata=dnslib.CNAME(ans[1])))
        elif soa:
            soa_content = soa[1].split()
            dns.add_auth(dnslib.RR(soa[0], dnslib.QTYPE.SOA,
                                   rdata=dnslib.SOA(soa_content[0], soa_content[1], (int(i) for i in soa_content[2:]))))
    
        return dns


def CreateProcessor(config):
    return DNSProcessor(config)

def subProcess(processor, msg):
    processor.Predo(msg)
    processor.Doing(msg)
    processor.Done(msg)


def processMsg(qcache, processor):
    while True:
        msg = qcache.get()
        gevent.spawn(subProcess, processor, msg)

def ProcessQueue(qcache, processor):
    gevent.spawn(processMsg, qcache, processor)

def CreateQueue(size):
    return Queue(maxsize=size) if size > 0 else Queue()


