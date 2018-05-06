# (c) 2018 Tongyu Zhou, Tingda Wang, Xuanzhen Zhang
# trains ConvNet pokemon typ classifier and saves to .h5 file in \models

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import plot_model

import numpy as np
import os,random, sys

from visualization import plot_loss

# shape of img: SHAPE x SHAPE
SHAPE = 32

def create_cnn(primary = True):
    ''' 
    creates the convolutional neural network classifier 
    returns the classfier for primary or secondary types
    '''

    # sequential layers
    classifier = Sequential()

    # add convolutional layers
    ''' 
    3 Convolutional Layers, maxpool layer follows 2 Conv2D layers
    3 Dropout layers to prevent overfitting
    after flatten, 2 dense layers to return output
    '''
    classifier.add(Conv2D(64, (3, 3),
                          padding = 'same',
                          input_shape = (SHAPE, SHAPE, 3),
                          activation = 'relu'))
    #classifier.add(Conv2D(32, (3, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size = (2, 2), strides = 2))
    classifier.add(Dropout(0.25))
    
    classifier.add(Conv2D(64, (3, 3), padding = 'same', activation = 'relu'))
    classifier.add(Conv2D(64, (3, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size = (2, 2), strides = 2))
    classifier.add(Dropout(0.25))

    #classifier.add(Conv2D(64, (3, 3), padding = 'same', activation = 'relu'))
    #classifier.add(Conv2D(64, (3, 3), activation='relu'))
    #classifier.add(MaxPooling2D(pool_size = (2, 2)))
    #classifier.add(Dropout(0.25))

    # flatten output and create fully connected layers
    classifier.add(Flatten())
    classifier.add(Dense(256, input_dim = 4, activation = 'relu'))
    classifier.add(Dropout(0.5))
    
    # one more category for None in secondary type
    categories = 18 if primary else 19

    classifier.add(Dense(categories, activation = 'softmax'))

    # returns built CNN
    return classifier

def train(primary = True, save = True, plot_classifier = False):
    '''
    trains the model for primary or secondary types.
    Supports saving the model and plotting the model.
    Returns the classifier as well as history object for plotting.
    '''

    # get model
    classifier = create_cnn(primary)

    # batch size
    BATCH_SIZE = 64

    # number of training epochs
    EPOCHS = 20
    
    # uses adam optimizer and crossentropy loss function
    classifier.compile(optimizer = 'adam',
                       loss = 'categorical_crossentropy',
                       metrics = ['accuracy'])

    # data augmentation: prevent further over
    
    by randomly transforming the training images
    train_datagen = ImageDataGenerator(
        rescale = 1./255,
        rotation_range = 10,
        shear_range = 0.2,
        zoom_range = 0.2,
        width_shift_range = 0.1,
        height_shift_range = 0.1,
        horizontal_flip = True,
        vertical_flip = True)
    
    test_datagen = ImageDataGenerator(rescale = 1./255)

    # file path depends on the model
    train = 'type1_sorted/train' if primary else 'type2_sorted/train' 
    test = 'type1_sorted/test' if primary else 'type2_sorted/test' 

    # retrieve datasets
    training_set = train_datagen.flow_from_directory(train,
                                                     target_size = (SHAPE, SHAPE),
                                                     batch_size = BATCH_SIZE,
                                                     class_mode = 'categorical')
    
    test_set = test_datagen.flow_from_directory(test,
                                                target_size = (SHAPE, SHAPE),
                                                batch_size = BATCH_SIZE,
                                                class_mode = 'categorical')

    # training
    history = classifier.fit_generator(training_set,
                                       #steps_per_epoch = 752,
                                       #validation_steps = 188,
                                       epochs = EPOCHS, 
                                       validation_data = test_set, shuffle = true)


    # plots the model
    if plot_classifier:
        filepath = 'model/classifier1.png' if primary else 'model/classifier2.png'
        plot_model(classifier, to_file = filepath)
        print("Model plots saved to model/")

    # save the classifier
    if save:
        if not os.path.exists(os.path.dirname("model/")):
            os.makedirs(os.path.dirname("model/"))
        filename = "classifier1" if primary else "classifier2"
        classifier.save("model/" + filename + ".h5")
        print("Saved model to disk")

    return classifier, history

if __name__ == "__main__":

    s = True # save model
    plt = True # plot model layers
    
    # build classifier for type 1 and 2
    _, h = train(primary = True, save = s, plot_classifier = plt)    
    _, h2 = train(primary = False, save = s, plot_classifier = plt)

    if plt: # plots accuracy and loss curves
        plot_loss(h)
        plot_loss(h2)
