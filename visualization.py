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
    for i, folder in enumerate(game_folders):            
        img = mpimg.imread(os.path.join(path, folder, image))
        plt.subplot(2, 8, i + 1)
        plt.imshow(img)
        plt.title(str(folder))

    # can't forget the icon
    img = mpimg.imread(os.path.join("data/icons/", image))
    plt.subplot(2,8,15)
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
    for i, id in enumerate(pokemons):
        image = "{n}.png".format(n = id)
        img = mpimg.imread(os.path.join(full_path, image))
        plt.subplot(1, batch, i + 1)
        plt.imshow(img)
        plt.title(get_pokemon(str(id)).name)
    plt.suptitle("Pokemons from " + str(game))
    plt.show()

if __name__ == "__main__":
    plot_pokemon(151)
    plot_game("platinum")
    plot_game("icons")
