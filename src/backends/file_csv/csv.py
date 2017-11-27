#!/usr/bin/env python
#encoding:utf-8

import sys
import backends.backend as bk

class BkdCSV(bk.Backend):
    def __init__(self, config):
        print "[CSV Backend] file:%s , func:%s" % (__file__, sys._getframe().f_code.co_name)
        self.config = config
        self.db_path = config.GetItem("db")
        self.dns = None
        self.soa = None

    def Prepare(self):
        print "[CSV Backend] file:%s , func:%s" % (__file__, sys._getframe().f_code.co_name)
        with open(self.db_path) as fdb:
            soa_line = fdb.readline().rstrip().split(',')
            self.soa = tuple(soa_line) if len(soa_line) == 2 else None
            self.dns = [tuple(line.rstrip('\r\n').split(',')) for line in fdb.readlines()]

    def Query(self, qname):
        print "[CSV Backend] file:%s , func:%s" % (__file__, sys._getframe().f_code.co_name)
        def get_answer(q, d, names):
            name = d.get(q)
            if name:
                names.append((q, name))
                get_answer(name, d, names)

        ret = []
        get_answer(qname, dict(self.dns), ret)
        print ret
        return ret, self.soa

