import matplotlib
matplotlib.use('Agg')
import pandas as pd
from matplotlib import pyplot as plt 
import os
from pypinyin import lazy_pinyin
from matplotlib.ticker import MaxNLocator
import re

target_dir = './res/'
picture = './images/'

func = lambda z:dict([(x, y) for y, x in z.items()])
 
def plot(x,y,t,a):
    ax = plt.figure().gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.title(a) 
    plt.xlabel("time (month.day.hour)") 
    plt.ylabel(t) 
    for a, b in zip(x, y):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=20)
    plt.plot(x,y) 
    if not os.path.exists(picture+f'{a}/'):
        os.mkdir(picture+f'{a}/')
    plt.savefig(picture+f'{a}/{t}.png')
    plt.close()

def time(t):
    year = t[:4]
    month = t[4:6]
    day = t[6:8]
    hour = t[8:10]
    minute = t[10:]
    return f'{month}.{day}.{hour}'


def to_images(data, t):
    for l in data:
        d = data[l].to_dict()
        d = func(d)
        y = list(d.keys())
        x = list(d.values())
        x = [time(t) for t in x]
        x.insert(0,'')
        y.insert(0,0)
        a = ''.join(lazy_pinyin(l))
        plot(x,y,t,a)
        
fields = '|'.join(['confirmedCount', 'deadCount', 'curedCount'])
        
for table in list(os.walk(target_dir))[0][2]:
    t = re.findall(fields, table)
    if len(t) > 0:
        data = pd.read_csv(target_dir+table, '\t',header=0,index_col=0).T
        to_images(data, t[0])
