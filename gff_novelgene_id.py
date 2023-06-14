#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author: Hongzhang Xue
    @Modified: 2023/6/13 4:26 PM
    @Usage:
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


def dict2string(long_dict, sep=';', eq='='):
    long_string = ''
    for i in long_dict:
        key, value = i, long_dict[i]
        long_string += str(key) + eq + str(value) + sep
    return long_string


current_geneid = ''
gff=sys.argv[1]

gene_replace_dict = dict()

with open(gff) as f:
    for line in f:
        if line.startswith('#'):
            print(line.rstrip())
        temp = line.rstrip().split('\t')
        if temp[2] == 'gene':
            attr = string2dict(temp[8])
            geneid = attr['ID']
            if (geneid.startswith('NDH') or geneid.startswith('Contig')) and len(geneid.split('_')) == 1:
                current_geneid = geneid
                print(line.rstrip())
            else:
                newgeneid = current_geneid[:-1] + str(int(current_geneid[-1])+1)
                gene_replace_dict[geneid] = newgeneid
                attr['ID'] = newgeneid
                temp[8] = dict2string(attr)
                print('\t'.join(temp))
                current_geneid = newgeneid
        else:
            attr = string2dict(temp[8])
            geneid = attr['ID'].split('.')[0]
            if geneid in gene_replace_dict:
                temp[8] = temp[8].replace(geneid, gene_replace_dict[geneid])
                print('\t'.join(temp))
            else:
                print(line.rstrip())




