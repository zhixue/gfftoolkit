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


with open(sys.argv[1]) as f:
    for line in f:
        if line.startswith('#'):
            print(line.rstrip())
            continue
        temp = line.rstrip().split('\t')
        if temp[2] == 'gene' or temp[2] == 'mRNA':
            print(line.rstrip())
            continue
        
        attr = string2dict(temp[8])      
        oldid = attr['ID']
        newid = attr['Parent'] + oldid.replace(oldid.split('.')[0],'')
        attr['ID'] = newid
        s = ''
        for key in attr:
            s += key + '=' + attr[key] + ';'
        temp[8] = s
        print('\t'.join(temp))

