#!/usr/bin/env python ud3k_bed.py in.gff > out.gff


import sys


with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith('#'):
            print(line.rstrip())
            continue
        temp = line.rstrip().split('\t')
        geneid = temp[8].split(';')[0].split('=')[1].split('.')[0]
        temp[8] += 'gene_id={gid};'.format(gid=geneid)
        print('\t'.join(temp))
