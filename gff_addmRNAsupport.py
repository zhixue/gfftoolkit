#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Author: Hongzhang Xue
    @Modified: 2023/5/22 10:33 AM
    @Usage: python3 gff_addmRNAsupport.py raw.gff rna_evidence.gtf > new.gff
"""
# still have some bugs
import sys


def union_length(regions):
    regions = sorted(regions)
    if len(regions) == 0:
        return 0.000001
    count_length = 0
    for i in range(1, len(regions)):
        if regions[i-1][1] > regions[i][1]:
            regions[i] = (regions[i][0], regions[i-1][1])
        count_length += \
            (regions[i-1][1] - regions[i-1][0] + 1) - \
            max(0, regions[i-1][1] - regions[i][0] + 1)
    # final one
    count_length += regions[-1][1] - regions[-1][0] + 1
    return count_length


def intersect_length(interval_list1, interval_list2):
    i, j = 0, 0
    intersect = []
    while i < len(interval_list1) and j < len(interval_list2):
        a1, a2 = interval_list1[i][0], interval_list1[i][1]
        b1, b2 = interval_list2[j][0], interval_list2[j][1]
        if b2 >= a1 and a2 >= b1:
            intersect += [(max(a1, b1), min(a2, b2))]
        if b2 < a2:
            j += 1
        else:
            i += 1
    return sum([x[1] - x[0] + 1 for x in intersect])


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
gtf=sys.argv[2]


transcript_d = dict()

with open(gtf) as f:
    for line in f:
        if line.startswith('#'):
            continue
        temp = line.rstrip().split('\t')
        if temp[2] == 'transcript':
            if temp[0] not in transcript_d:
                transcript_d[temp[0]] = dict()
            transcript_loc = (int(temp[3]), int(temp[4]))
            transcript_d[temp[0]][transcript_loc] = []
        else:
            exon_loc = (int(temp[3]), int(temp[4]))
            transcript_d[temp[0]][transcript_loc] += [exon_loc]

chrn = ''
temp_mrna = ''
mrna_region = ()
exon_region = []
temp_mrna_sublines = ''
temp_mrna_line = ''
old_temp_gene_line = ''
new_temp_gene_line = ''
gene_print = dict()

f = open(gff)
for line in f:
    if line.startswith('#'):
        print(line.rstrip())
        continue
    temp = line.rstrip().split('\t')
    if temp[2] == 'gene':
        old_temp_gene_line = new_temp_gene_line
        new_temp_gene_line = line.rstrip()

        if temp_mrna == '':
            print(new_temp_gene_line)
            gene_print[string2dict(temp[8])['ID']] = 1
    elif temp[2] == 'mRNA':
        if temp_mrna != '':
            # compute
            mrna_cov = 0
            exon_cov = 0
            for tr in transcript_d[chrn]:
                if tr[1] < mrna_region[0]:
                    continue
                if tr[0] > mrna_region[1]:
                    break
                else:
                    mrna_intersect_length = intersect_length([tr], [mrna_region])
                    exon_intersect_length = intersect_length(transcript_d[chrn][tr], exon_region)
                    mrna_cov = mrna_intersect_length / union_length([mrna_region])
                    exon_cov = exon_intersect_length / union_length(exon_region)
                    temp_mrna_line += 'mRNA_cov=' + str(round(mrna_cov, 3)) + ';' + \
                        'exon_cov=' + str(round(exon_cov, 3)) + ';'
            if temp_mrna.split('.')[0] in gene_print:
                print(temp_mrna_line + temp_mrna_sublines)
                gene_print[temp_mrna.split('.')[0]] = 1
            else:
                print(old_temp_gene_line + '\n' + temp_mrna_line + temp_mrna_sublines)
        chrn = temp[0]
        temp_mrna = string2dict(temp[8])['ID']
        temp_mrna_line = line.rstrip()
        temp_mrna_sublines = ''
        exon_region = []
        mrna_region = (int(temp[3]), int(temp[4]))
    else:
        ele_attr = string2dict(temp[8])
        if 'Parent' in ele_attr and ele_attr['Parent'] == temp_mrna:
            temp_mrna_sublines += '\n' + line.rstrip()
            if temp[2] == 'exon':
                exon_region += [(int(temp[3]), int(temp[4]))]
    # final
    if temp[2] == 'mRNA':
        if temp_mrna != '':
            # compute
            for tr in transcript_d[chrn]:
                if tr[1] < mrna_region[0]:
                    continue
                if tr[0] > mrna_region[1]:
                    break
                else:
                    mrna_intersect_length = intersect_length([tr], [mrna_region])
                    exon_intersect_length = intersect_length(transcript_d[chrn][tr], exon_region)
                    mrna_cov = mrna_intersect_length / union_length([mrna_region])
                    exon_cov = exon_intersect_length / union_length(exon_region)
                    temp_mrna_line += 'mRNA_cov=' + str(round(mrna_cov, 3)) + ';' + \
                        'exon_cov=' + str(round(exon_cov, 3)) + ';'
            if temp_mrna.split('.')[0] in gene_print:
                print(temp_mrna_line + temp_mrna_sublines)
                gene_print[temp_mrna.split('.')[0]] = 1
            else:
                print(old_temp_gene_line + '\n' + temp_mrna_line + temp_mrna_sublines)
f.close()



