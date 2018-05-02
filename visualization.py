# (c) 2018 Tingda Wang
# Functions for visualizing the data set and model

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os, random

from preprocess import get_pokemon

def plot_pokemon(id = random.randint(1, 700)):
    ''' 
    plots images of a pokemon given id 
    across all generations of games and data available
    '''
    path = "data/main-sprites/"
    game_folders = sorted([x for x in os.listdir(path) if not x.startswith('.')])
    image = "{n}.png".format(n = id)
    plt.figure(figsize = (20, 4))

    # plot pokemon from all folders
    counter = 1
    for folder in game_folders:            
        try:
            img = mpimg.imread(os.path.join(path, folder, image))
            plt.subplot(2, 8, counter)
            plt.imshow(img)
            plt.title(str(folder))
            counter += 1
        except FileNotFoundError:
            pass

    # can't forget the icon
    img = mpimg.imread(os.path.join("data/icons/", image))
    plt.subplot(2,8,counter)
    plt.imshow(img)
    plt.title("icon")

    # we'll tell you the name as well
    plt.suptitle("Pokemon #" + str(id) + " " + get_pokemon(str(id)).name)
    plt.show()

def plot_game(game, pokemons = random.sample(range(1, 152), 10)):
    ''' 
    plots list of pokemons in a given game or the icons folder
    '''
    path = "data/main-sprites/"
    full_path = os.path.join(path, game) if game is not "icons" else "data/icons"
    batch = len(pokemons)
    plt.figure(figsize = (20, 4))

    # plot the pokemon from pokemons
    counter = 1
    for id in pokemons:
        try:
            image = "{n}.png".format(n = id)
            img = mpimg.imread(os.path.join(full_path, image))
            plt.subplot(1, batch, counter)
            plt.imshow(img)
            plt.title(get_pokemon(str(id)).name)
            counter += 1
        except FileNotFoundError:
            pass
    plt.suptitle("Pokemons from " + str(game))
    plt.show()

def plot_loss(history):
    # loss
    plt.figure(figsize = (8, 6))
    plt.plot(history.history['loss'], 'r', linewidth = 3.0)
    plt.plot(history.history['val_loss'], 'b', linewidth = 3.0)
    plt.legend(['Training loss', 'Validation Loss'], fontsize = 18)
    plt.xlabel('Epochs ', fontsize = 16)
    plt.ylabel('Loss', fontsize = 16)
    plt.title('Loss Curves', fontsize = 16)
 
    # accuracy
    plt.figure(figsize = (8, 6])
    plt.plot(history.history['acc'], 'r', linewidth = 3.0)
    plt.plot(history.history['val_acc'], 'b', linewidth = 3.0)
    plt.legend(['Training Accuracy', 'Validation Accuracy'], fontsize = 18)
    plt.xlabel('Epochs ', fontsize = 16)
    plt.ylabel('Accuracy', fontsize = 16)
    plt.title('Accuracy Curves',fontsize = 16)

    plt.suptitle('Loss & Accuracy')
    plt.show()
    
if __name__ == "__main__":
    plot_pokemon(150)
    plot_game("platinum")
    plot_game("icons")
    plot_game("conquest")
