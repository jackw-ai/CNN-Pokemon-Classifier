import glob, shutil
import os
import re
from collections import namedtuple

Pokemon = namedtuple('Pokemon', 'name, type1, type2')

def types (path):
    file = open(path, 'r').read().splitlines()
    dict = {}
    file.pop(0)
    for f in file:
        info = f.split(',')
        dict[info[0]] = Pokemon(info[1], info[2], info[3])
    return dict

def sort (dict, path):
    src_dir = path
    for pngfile in glob.iglob(os.path.join(src_dir, "*.png")):
        name = str(pngfile).split('/')[2]
        id = ''.join(re.findall(r'\b\d+\b', name))
        if id != '':
            primary_type = dict[id].type1
            dst_dir = 'type1_sorted/' + primary_type + '/' + name 
            if not os.path.exists(os.path.dirname(dst_dir)):
                os.makedirs(os.path.dirname(dst_dir))
            shutil.copy(pngfile, dst_dir)

# divides the sprite images into their respective types
typing = types('data/Pokemon-2.csv')
sort(typing, 'data/icons')
