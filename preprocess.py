# (c) 2018 Tongyu Zhou, Tingda Wang
# preprocesses data found in /data and divides all images for test and training

import glob, shutil
import os, re, sys
import numpy
import matplotlib.image as mpimg
from skimage import color, filters, measure, morphology, transform
from scipy import ndimage
from functools import reduce
from math import ceil, floor
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

# box modification code by hemagso
def bbox_reducer(a,b):
    """Reduces two bounding boxes tuples to a bounding box
    encompassing both. The bounding box format expected is
    
    (min_row, min_col, max_row, max_col)
    
    Used with the reduce function to merge bounding boxes
    
    """
    min_row = min(a[0],b[0])
    min_col = min(a[1],b[1])
    max_row = max(a[2],b[2])
    max_col = max(a[3],b[3])
    return (min_row, min_col, max_row, max_col)

# optimization code by hemagso
def optimize(image,new_size = (64,64),plot=False,square=True, id = None):
    image_bw = color.rgb2gray(image)
    image_countour = filters.sobel(image_bw)
    image_filled = ndimage.binary_fill_holes(image_countour)
    
    image_mask = morphology.convex_hull_image(image_filled)
    
    labels, n_objects = ndimage.label(image_mask)
    regions = measure.regionprops(labels)
    slices = ndimage.find_objects(labels)

    #Get border
    bbox_list = [r.bbox for r in regions]
    min_row, min_col, max_row, max_col = reduce(bbox_reducer,bbox_list)
    
    #If the bounding box is not squared, make it so
    if square:
        len_row = max_row - min_row
        len_col = max_col - min_col

        if len_row > len_col:
            min_col -= ceil((len_row - len_col)/2)
            max_col += floor((len_row - len_col)/2)
        else:
            min_row -= ceil((len_col - len_row)/2)
            max_row += floor((len_col - len_row)/2)      
    

    #We may have some out of bound stuff hapenning here
#    if (max_row - min_row) > image.shape[0]:
#        raise ValueError("ID = {id} - Bounding box height is greater than image height".format(id=id))
#    if (max_col - min_col) > image.shape[1]:
#        raise ValueError("ID = {id} - Bounding box width is greater than image width".format(id=id))

    #If Bounding box exceeds image limits, we shift it inside
    if min_row < 0:
        max_row += abs(min_row)
        min_row = 0
    if min_col < 0:
        max_col += abs(min_col)
        min_col = 0
    if max_row >= image.shape[1]:
        min_row -= max_row - image.shape[1] + 1
        max_row = image.shape[0]-1
    if max_col >= image.shape[1]:
        min_col -= max_col - image.shape[1] + 1
        max_col = image.shape[1]-1    
    
    image_slice = (
        slice(min_row,max_row,None) ,
        slice(min_col,max_col,None)               
    )
    
    image_bounded = image[image_slice]
    
    image_resize = transform.resize(image_bounded,new_size)
    
    if plot:
        image_box = patches.Rectangle(
            (min_col,min_row),
            max_row - min_row,  
            max_col - min_col,  
            fc = "none",
            ec = "red"
        )
        img_arr = [
            (image,None,None),
            (image_bw,"gray",None),
            (image_countour,"gray",None),
            (image_filled,"gray",None),
            (image_mask,"gray",None),
            (image,None,image_box),
            (image_resize,None,None)
        ]
        plot_intermediate_steps(img_arr)
    
    return image_resize    

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
        img_file = mpimg.imread(dst_dir)
        img_file = optimize(img_file)
        mpimg.imsave(dst_dir, img_file)

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
