#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author: Hongzhang Xue
    @Modified: 2023/5/30 12:54 PM
    @Usage: python3 gff_add_aalen.py raw.gff raw.pep > new.gff
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


len_dict = dict()

seq = ''
sid = ''

with open(sys.argv[2]) as f:
    for line in f:
        if line.startswith('>'):
            if seq != '':
                sl = len(seq) - seq.count('\n') - seq.count(' ')
                len_dict[sid] = sl
            sid = line.rstrip()[1:]
            seq = ''
        else:
            seq += line
    # last one
    sl = len(seq) - seq.count('\n') - seq.count(' ')
    len_dict[sid] = sl

with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith('#'):
            print(line.rstrip())
        else:
            temp = line.rstrip().split('\t')
            if temp[2] == 'mRNA':
                mrnaid = string2dict(temp[8])['ID']
                if mrnaid in len_dict:
                    print(line.rstrip().rstrip(';') + ';' + 'aa_len=' + str(len_dict[mrnaid]) + ';')
                else:
                    print(line.rstrip().rstrip(';') + ';')
            else:
                print(line.rstrip())
