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
    type_dict = {}
    for pngfile in dataset:
        name = str(pngfile).split('/')[2]
        id = ''.join(re.findall(r'\b\d+\b', name))
        if id != '':
            primary_type = dict[id].type1
            if primary_type in type_dict:
                type_dict[primary_type].append(pngfile)
            else:
                type_dict[primary_type] = [pngfile]
    for key in type_dict:
        values = type_dict[key]
        numpy.random.shuffle(values)
        train, test = train_test_split(values, test_size = 0.2)
        sort(key, train, 'train')
        sort(key, test, 'test')

def sort (type, dataset, datatype):
    for img in dataset:
        name = str(img).split('/')[2]
        dst_dir = 'type1_sorted/' + datatype + '/' + type + '/' + name 
        if not os.path.exists(os.path.dirname(dst_dir)):
            os.makedirs(os.path.dirname(dst_dir))
        shutil.copy(img, dst_dir)

# divides the sprite images into their respective types
shutil.rmtree('type1_sorted') # deletes the directory and reshuffles images each time 
typing = types('data/Pokemon-2.csv')
load(typing, 'data/icons')
