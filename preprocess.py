import glob, shutil
import os, re, sys
import numpy
from sklearn.model_selection import train_test_split
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

def load (dict, path):
    src_dir = path
    dataset = list(glob.iglob(os.path.join(src_dir, "*.png")))
    numpy.random.shuffle(dataset)
    train, test = train_test_split(dataset, test_size = 0.2)
    sort(dict, train, 'train')
    sort(dict, test, 'test')

def sort (dict, list, datatype):
    for pngfile in list:
        name = str(pngfile).split('/')[2]
        id = ''.join(re.findall(r'\b\d+\b', name))
        if id != '':
            primary_type = dict[id].type1
            dst_dir = 'type1_sorted/' + datatype + '/' + primary_type + '/' + name 
            if not os.path.exists(os.path.dirname(dst_dir)):
                os.makedirs(os.path.dirname(dst_dir))
            shutil.copy(pngfile, dst_dir)

# divides the sprite images into their respective types
shutil.rmtree('type1_sorted') # deletes the directory and reshuffles images each time 
typing = types('data/Pokemon-2.csv')
load(typing, 'data/icons')
