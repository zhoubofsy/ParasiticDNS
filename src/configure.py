#!/usr/bin/env python
#encoding:utf-8

import os
import ConfigParser

class DNSConfigure(object):
    def __init__(self, cfile):
        if cfile == None or cfile == "":
            cfile = os.path.dirname(__file__) + "/dns.ini"
        self.path = cfile

        with open(cfile, 'r') as cf:
            cfg = ConfigParser.ConfigParser()
            cfg.readfp(cf)

        self.dict_config = cfg

    def get(self, key, session="DEFAULT"):
        session_config = dict(self.dict_config.items(session))
        return session_config[key]

    def GetItem(self, key):
        return self.get(key=key)

