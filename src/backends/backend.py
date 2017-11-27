#!/usr/bin/env python
#encoding:utf-8

import sys

class Backend(object):
    def __init__(self):
        print "[Backend Interface] Unimplement file: %s , func: %s" % (__file__, sys._getframe().f_code.co_name)
        raise NotImplementedError, "Backend's %s" % (sys._getframe().f_code.co_name)

    def Prepare(self):
        print "[Backend Interface] Unimplement file: %s , func: %s" % (__file__, sys._getframe().f_code.co_name)
        raise NotImplementedError, "Backend's %s" % (sys._getframe().f_code.co_name)

    def Query(self):
        print "[Backend Interface] Unimplement file: %s , func: %s" % (__file__, sys._getframe().f_code.co_name)
        raise NotImplementedError, "Backend's %s" % (sys._getframe().f_code.co_name)

