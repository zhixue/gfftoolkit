#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author: Hongzhang Xue
    @Modified: 2023/5/30 1:44 PM
    @Usage: python3 gff_drop_id.py raw.gff id.list > new.gff
"""
import sys

def string2dict(long_string, sep=';', eq='=', rm_quote=False):
    if rm_quote:
        long_string = long_string.replace('"', '').replace("'", '')
    long_string = long_string.replace('; ', ';')
    out_dict = dict()
    tmp = long_string.rstrip(sep).split(sep)
    for i in tmp:
        if len(i.split(eq)) == 2:
            key, value = i.split(eq)
        else:
            key = i.split(eq)[0]
            value = eq.join(i.split(eq)[1:])
        out_dict[key] = value
    return out_dict

id_list = dict()
with open(sys.argv[2]) as f:
    for line in f:
        id_list[line.rstrip()] = ''
        #id_list[line.rstrip().split('-mRNA')[0]] = ''

with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith('#'):
            print(line.rstrip())
            continue
        else:
            temp = line.rstrip().split('\t')
            attr = string2dict(temp[8])
            if attr['ID'] in id_list:
                continue
            if 'Parent' in attr:
                if attr['Parent'] in id_list:
                    continue
            print(line.rstrip())