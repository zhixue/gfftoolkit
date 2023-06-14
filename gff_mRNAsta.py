#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author: Hongzhang Xue
    @Modified: 2022/11/29 7:34 PM
    @Usage: python3 gff_mRNAsta.py xx_ptpg.gff > xx_ptpg_summary.tsv
"""
# output:
# geneID mRNAID gene_len mRNA_len exon_sum_len exon_number CDS_sum_len CDS_number
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

gene_dict = dict() # {'gene_id':gene_len}
mrna_loc_dict = dict() # {'mrna_id':[chrn,start,end]}
mrna_dict = dict() # {'mrna_id':[gene_id,mrna_len,{(e1s,e1e),(e2s,e2e)},{(c1s,c1e),(c2s,c2e)}}
with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith('#') or line.startswith('\n'):
            continue
        temp = line.rstrip().split('\t')
        if len(temp) >= 9:
            eletype = temp[2]
            if eletype == 'gene':
                geneid = string2dict(temp[8])['ID']
                genelen = int(temp[4]) - int(temp[3]) + 1
                gene_dict[geneid] = genelen
            elif eletype == 'mRNA':
                attr = string2dict(temp[8])
                mrnaid = attr['ID']
                gene_parent = attr['Parent']
                mrnalen = int(temp[4]) - int(temp[3]) + 1
                mrna_dict[mrnaid] = [gene_parent, mrnalen, set(), set()]
                mrna_loc_dict[mrnaid] = [temp[0], temp[3], temp[4]]
            elif eletype == 'exon':
                attr = string2dict(temp[8])
                mrna_parent = attr['Parent']
                if mrna_parent not in mrna_dict:
                    mrna_dict[mrna_parent] = [mrna_parent.split('.')[0], 0, set(), set()]
                    mrna_loc_dict[mrna_parent] = [temp[0], 0, 0]
                mrna_dict[mrna_parent][2].add(tuple([int(temp[3]), int(temp[4])]))
            elif eletype == 'CDS':
                attr = string2dict(temp[8])
                mrna_parent = attr['Parent']
                if mrna_parent not in mrna_dict:
                    mrna_dict[mrna_parent] = [mrna_parent.split('.')[0], 0, set(), set()]
                    mrna_loc_dict[mrna_parent] = [temp[0], 0, 0]
                mrna_dict[mrna_parent][3].add(tuple([int(temp[3]), int(temp[4])]))

# fill the black records of mRNA
for mrna in mrna_dict:
    if mrna_dict[mrna][1] == 0:
        mrna_dict[mrna][1] = sum([x[1]-x[0]+1 for x in mrna_dict[mrna][2]])
        try:
            mrna_loc_dict[mrna][1] = min([x[0] for x in mrna_dict[mrna][2]])
            mrna_loc_dict[mrna][2] = max([x[1] for x in mrna_dict[mrna][2]])
        except:
            mrna_loc_dict[mrna][1] = min([x[0] for x in mrna_dict[mrna][3]])
            mrna_loc_dict[mrna][2] = max([x[1] for x in mrna_dict[mrna][3]])
    # fill the black records of gene
    if mrna_dict[mrna][0] not in gene_dict:
        gene_dict[mrna_dict[mrna][0]] = mrna_dict[mrna][1]

for mrna in mrna_dict:
    if len(mrna_dict[mrna][3]) == 0:
        continue
    #print(mrna_dict[mrna][2])
    print('\t'.join([mrna_dict[mrna][0], mrna, str(gene_dict[mrna_dict[mrna][0]]), str(mrna_dict[mrna][1]),
                     str(sum([x[1]-x[0]+1 for x in mrna_dict[mrna][2]])), str(len(mrna_dict[mrna][2])),
                     str(sum([x[1]-x[0]+1 for x in mrna_dict[mrna][3]])), str(len(mrna_dict[mrna][3])),
                     mrna_loc_dict[mrna][0],
                     str(mrna_loc_dict[mrna][1]), str(mrna_loc_dict[mrna][2])]))


