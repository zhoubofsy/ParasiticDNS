#!/usr/bin/env python
#encoding:utf-8

#import backends.backend as bki
from backends.file_csv import csv as bk_csv

def CreateBackend(config, bkname = 'file_csv'):
    '''
    根据配置文件配置创建与之对应的Backend实例
    '''
    bkend = None

    # CSV Backend
    if 'file_csv' == bkname:
        print 'create file_csv backend'
        bkend = bk_csv.BkdCSV(config)
    else:
        print '%s unsupport backend'%bkname
        return None

    return bkend

