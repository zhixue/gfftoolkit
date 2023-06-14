#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author: Hongzhang Xue
    @Modified: 2023/6/14 9:01 AM
    @Usage: python3 gff_fix_phase.py raw.gff ref.gff > new.gff
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


rawgff = sys.argv[1]
refgff = sys.argv[2]

cds_phase = dict()

white_list = ['NDH06G029820.1']
with open(refgff) as f:
    for line in f:
        if line.startswith('#'):
            #print(line.rstrip())
            continue
        temp = line.rstrip().split('\t')
        if temp[2] == 'CDS':
            attr = string2dict(temp[8])
            cdsid = attr['ID']
            mrnaid = attr['Parent']
            phase = temp[7]
            cds_phase[(mrnaid, temp[3], temp[4])] = phase

with open(rawgff) as f:
    for line in f:
        if line.startswith('#'):
            print(line.rstrip())
            continue
        temp = line.rstrip().split('\t')
        if temp[2] == 'CDS':
            attr = string2dict(temp[8])
            cdsid = attr['ID']
            mrnaid = attr['Parent']
            if mrnaid in white_list:
                print(line.rstrip())
                continue
            phase = temp[7]
            if (mrnaid, temp[3], temp[4]) in cds_phase:
                temp[7] = cds_phase[(mrnaid, temp[3], temp[4])]
            print('\t'.join(temp))
        else:
            print(line.rstrip())

