#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author: Hongzhang Xue
    @Modified: 2023/5/20 6:51 PM
    @Usage: python3 gff_addfunction.py raw.gff domain_col4.tsv > new.gff
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


gff=sys.argv[1]
tsv=sys.argv[2]

function_d = dict()
with open(tsv) as f:
    for line in f:
        temp = line.rstrip().split('\t')
        mrna = temp[0]
        fid = temp[4]
        fdescription = temp[5]
        # remove ";",'"'
        fdescription = fdescription.replace(';', ',').replace('"', "'")
        if mrna not in function_d:
            function_d[mrna] = list()
        add_item = fid + "::" + fdescription
        if add_item not in function_d[mrna]:
            function_d[mrna] += [fid + "::" + fdescription]


with open(gff) as f:
    for line in f:
        if line.startswith('#'):
            print(line.rstrip())
        temp = line.rstrip().split('\t')
        if temp[2] != 'mRNA':
            print(line.rstrip())
        else:
            mrnaid = string2dict(temp[8])['ID']
            if mrnaid in function_d:
                print(line.rstrip() + 'function="' + ',,'.join(function_d[mrnaid]) + '";')
            else:
                print(line.rstrip())
