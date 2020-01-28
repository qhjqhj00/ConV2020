import json
import os
from bs4 import BeautifulSoup
from collections import defaultdict

source_dir = '../dxy2019nCoV/data/'
target_dir = './res/'
head = []
province = defaultdict()
city = defaultdict()
file_list = list(os.walk(source_dir))[0][2]
file_list.sort(reverse=True)

def cat(file,text):
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    with open(f'{target_dir}{file}', 'a') as f:
        f.write(text+'\n')


def update(p, c, d):
    for pro in d:
        p_name = pro['provinceShortName']
        if p_name not in p:
            p[p_name] = defaultdict(list)
        for k,v in pro.items():
            if type(v) is int:
                p[p_name][k].insert(0,v)
        for cit in pro['cities']:
            c_name = cit['cityName']
            if f'{p_name}_{c_name}' not in c:
                c[f'{p_name}_{c_name}'] = defaultdict(list)
            for k,v in cit.items():
                if type(v) is int:
                    c[f'{p_name}_{c_name}'][k].insert(0,v)
    return p,c

for file in file_list:
    if file.endswith('html'):
        head.insert(0, file.split('.')[0])
        with open(source_dir+file) as f:
            soup = BeautifulSoup(f, "html.parser")
            data = json.loads(soup.select('#getAreaStat')[0].text[27:-11])
            province, city = update(province, city, data)

for n,pro in province.items():
    for k in pro:
        padding = [0] * (len(head) - len(pro[k]))
        padding.extend(pro[k])
        padding = [str(d) for d in padding]
        padding.insert(0, n)
        text = '\t'.join(padding)
        cat(f'provinces_{k}.csv',text)

for n, cit in city.items():
    for k in cit:
        padding = [0] * (len(head) - len(cit[k]))
        padding.extend(cit[k])
        padding = [str(d) for d in padding]
        padding.insert(0, n)
        text = '\t'.join(padding)
        cat(f'cities_{k}.csv',text)

for file in list(os.walk(target_dir))[0][2]:
    with open(f'{target_dir}{file}', 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        t = '\t'.join(head)
        f.write(f'timestamp\t{t}\n'+content)
