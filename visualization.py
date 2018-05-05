# (c) 2018 Tingda Wang
# Functions for visualizing the data set and model

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec

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

def plot_type(imgpath = "", predicted = False, pred_types = []):
    ''' 
    plots the true type of the pokemon with its image 
    if predicted, then will plot the predicted types as well
    '''
    
    pkmn = get_pokemon(imgpath)
    dual_type = False if pkmn.type2 is "None" else True

    grid_rows = 3 if predicted else 2
    grid_cols = 2 if dual_type else 1
    figsize = (4, 4)        
    width_ratio = (1, 1) if dual_type else (1, )
    height_ratio = (12, 1, 1) if predicted else (12, 1)

    if dual_type:
        plt.figure(figsize = figsize)
        gs = gridspec.GridSpec(grid_rows, grid_cols, height_ratios = height_ratio, width_ratios = width_ratio)
        gs.update(wspace= 0.1, hspace= 0.5)
        ax0 = plt.subplot(gs[0, :])
        image = mpimg.imread(imgpath)
        img = ax0.imshow(image)
        plt.axis('off')
        
        ax1 = plt.subplot(gs[1, 0])
        typepath = "type_labels/{n}.png".format(n = pkmn.type1)
        typeicon = mpimg.imread(typepath)
        ax1.imshow(typeicon)
        plt.axis('off')
        
        ax1 = plt.subplot(gs[1, 1])
        type2path = "type_labels/{n}.png".format(n = pkmn.type2)
        type2icon = mpimg.imread(type2path)
        ax1.imshow(type2icon)
        plt.axis('off')
        
    else:
        plt.figure(figsize = figsize)
        gs = gridspec.GridSpec(grid_rows, grid_cols, height_ratios = height_ratio, width_ratios = width_ratio)
        gs.update(wspace= 0.25, hspace= 0.5)
        ax0 = plt.subplot(gs[0])
        image = mpimg.imread(imgpath)
        img = ax0.imshow(image)
        plt.axis('off')
    
        ax1 = plt.subplot(gs[1])
        typepath = "type_labels/{n}.png".format(n = pkmn.type1)
        typeicon = mpimg.imread(typepath)
        ax1.imshow(typeicon)
        plt.axis('off')

    if predicted:

        if dual_type:
            ax3 = plt.subplot(gs[2, 0])
            plt.text(-80, 12, "Predicted:")
            typepath = "type_labels/{n}.png".format(n = pred_types[0])
            typeicon = mpimg.imread(typepath)
            ax3.imshow(typeicon)
            plt.axis('off')

            ax4 = plt.subplot(gs[2, 1])
            try:
                typepath = "type_labels/{n}.png".format(n = pred_types[1])
                typeicon = mpimg.imread(typepath)
                ax4.imshow(typeicon)

            except FileNotFoundError:
                pass
            plt.axis('off')

        else:
            ax3 = plt.subplot(gs[2, :])
            plt.text(-80, 12, "Predicted:")
            typepath = "type_labels/{n}.png".format(n = pred_types[0])
            typeicon = mpimg.imread(typepath)
            ax3.imshow(typeicon)
            plt.axis('off')

    plt.suptitle(pkmn.name)
    plt.show()

def plot_loss(history):
    ''' plots the loss and accuracy history from training '''
    
    plt.figure(figsize = (20, 8))
    
    # loss
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], 'r', linewidth = 3.0)
    plt.plot(history.history['val_loss'], 'b', linewidth = 3.0)
    plt.legend(['Training loss', 'Validation Loss'], fontsize = 18)
    plt.xlabel('Epochs ', fontsize = 16)
    plt.ylabel('Loss', fontsize = 16)
    plt.title('Loss Curves', fontsize = 16)
 
    # accuracy
    plt.subplot(1, 2, 2)
    plt.plot(history.history['acc'], 'r', linewidth = 3.0)
    plt.plot(history.history['val_acc'], 'b', linewidth = 3.0)
    plt.legend(['Training Accuracy', 'Validation Accuracy'], fontsize = 18)
    plt.xlabel('Epochs ', fontsize = 16)
    plt.ylabel('Accuracy', fontsize = 16)
    plt.title('Accuracy Curves', fontsize = 16)

    plt.suptitle('Loss & Accuracy')
    plt.show()
    
if __name__ == "__main__":
    plot_type("data/main-sprites/platinum/3.png")
    plot_type("data/main-sprites/crystal/4.png")
    plot_type("data/main-sprites/crystal/4.png", predicted = True, pred_types = ["Grass"])
    '''
    plot_pokemon(150)
    plot_game("platinum")
    plot_game("icons")
    plot_game("conquest")
    '''
