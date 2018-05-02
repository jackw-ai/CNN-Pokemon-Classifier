# (c) 2018 Tongyu Zhou, Tingda Wang
# preprocesses data found in /data and divides all images for test and training

import glob, shutil
import os, re, sys
import numpy
from sklearn.model_selection import train_test_split
from collections import namedtuple

# tuple for each line of data
Pokemon = namedtuple('Pokemon', 'name, type1, type2')

def types(path):
    ''' 
    Reads the csv file to generate a namedtuple Pokemon for each line 
    returns a dictionary of pokemon no. as key and (name, type1, type2) as value
    '''
    file = open(path, 'r').read().splitlines()
    dict = {}
    file.pop(0)
    for f in file:
        info = f.split(',')
        info[1] = info[1].split('Mega')[0]
        if info[3] == "":
            info[3] = "None"
        dict[info[0]] = Pokemon(info[1], info[2], info[3])
    return dict

# for checking accuracy 
type_dict = types('data/Pokemon-2.csv')

def get_pokemon(filepath):
    ''' returns the Pokemon tuple based on file path '''
    filename = filepath.split('/')[-1]
    id = ''.join(re.findall(r'\b\d+\b', filename))
    return type_dict[id]

def load(dict, path, primary = True, testsize = 0.2):
    ''' 
    loads dataset and divides them by type and test, training
    primary denotes whether to divide based on primary or secondary types
    testsize denotes the proportion devoted to the test batch
    '''
    src_dir = path
    dataset = list(glob.iglob(os.path.join(src_dir, "*.png")))
    type_dict = {}
    for pngfile in dataset:
        name = str(pngfile).split('/')[-1]
        id = ''.join(re.findall(r'\b\d+\b', name))
        if id != '':
            try:
                primary_type = dict[id].type1 if primary else dict[id].type2
                if primary_type in type_dict:
                    type_dict[primary_type].append(pngfile)
                else:
                    type_dict[primary_type] = [pngfile]
            except KeyError: # there is some mysterious 0.png...
                print("ID: "+ str(id) + " file: " + str(pngfile))
                
    for key in type_dict:
        values = type_dict[key]
        numpy.random.shuffle(values)
        train, test = train_test_split(values, test_size = testsize)
        sort(key, train, 'train', primary)
        sort(key, test, 'test', primary)

def sort(type, dataset, datatype, primary = True):
    '''
    divide the pokemon into folders corresponding to their type 
    given a datatype of test or training and the dataset of images
    primary determines whether we sort type1 or type2 of a pokemon
    Outputs a test or training directory of the sorted pokemon images
    '''
    
    folder = 'type1_sorted/' if primary else 'type2_sorted/'
        
    for img in dataset:
        name = str(img).split('/')[-1]
        pic_source = str(img).split('/')[-2]
        full_name = pic_source + "-" + name
        dst_dir = folder + datatype + '/' + type + '/' + full_name 
        if not os.path.exists(os.path.dirname(dst_dir)):
            os.makedirs(os.path.dirname(dst_dir))
        shutil.copy(img, dst_dir)


if __name__ == "__main__":        
    # divides the sprite images into their respective types

    # deletes the directory and reshuffles images each time 
    try:
        shutil.rmtree('type1_sorted')
    except FileNotFoundError:
        pass

    try:
        shutil.rmtree('type1_sorted')
    except FileNotFoundError:
        pass

    # reads the csv file to build type dict
    typing = types('data/Pokemon-2.csv')

    # loads icon dataset first
    load(typing, 'data/icons')
    load(typing, 'data/icons', primary = False)
    print("icons loaded")
    
    # load sprites from all games
    game_sprites = [x[0] for x in os.walk('data/main-sprites')]
    for game in game_sprites:
        # we only load the main sprites, excluding shinies or backviews
        if len(str(game).split('/')) <= 3: 
            load(typing, game) 
            load(typing, game, primary = False)
            print(str(game).split('/')[-1], "loaded")
