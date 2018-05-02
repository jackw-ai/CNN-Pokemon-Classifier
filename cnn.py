# (c) 2018 Tongyu Zhou, Tingda Wang
# trains CNN and saves classifier to .h5 file

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import plot_model

import numpy as np
import os,random, sys

from visualization import plot_loss

def create_cnn(primary = True):
    ''' creates the convolutional neural network '''
    classifier = Sequential()
    classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))
    classifier.add(MaxPooling2D(pool_size = (2, 2)))
    classifier.add(Flatten())
    #classifier.add(Dense(units = 128, activation = 'relu'))
    #classifier.add(Dense(units = 1, activation = 'sigmoid'))
    classifier.add(Dense(128, input_dim=4, activation='relu'))

    # one more category for None type 2
    categories = 18 if primary else 19

    classifier.add(Dense(categories, activation='softmax'))
    return classifier

def train(primary = True, save = True, plot_classifier = False):
    '''
    trains the model for primary or secondary types.
    Supports saving the model and plotting the model.
    Returns the classifier as well as history object for plotting.
    '''
    classifier = create_cnn(primary)
    
    classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

    train_datagen = ImageDataGenerator(
        rescale = 1./255,
        #rotation_range = 10,
        shear_range = 0.2,
        zoom_range = 0.2,
        #width_shift_range = 0.1,
        #height_shift_range = 0.1,
        horizontal_flip = True)
    
    test_datagen = ImageDataGenerator(rescale = 1./255)

    train = 'type1_sorted/train' if primary else 'type2_sorted/train' 
    test = 'type1_sorted/test' if primary else 'type2_sorted/test' 

    training_set = train_datagen.flow_from_directory(train, target_size = (64, 64), batch_size = 32, class_mode = 'categorical')
    test_set = test_datagen.flow_from_directory(test, target_size = (64, 64), batch_size = 32, class_mode = 'categorical')

    history = classifier.fit_generator(training_set, steps_per_epoch = 752, epochs = 5, 
                                       validation_data = test_set, validation_steps = 188)

    # plots the model
    if plot_classifier:
        plot_model(classifier, to_file='model/classifier1.png')
        plot_model(classifier2, to_file='model/classifier2.png')
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
    # build classifier for type 1 and 2
    _, h = train(primary = True)
    plot_loss(h)
    _, h2 = train(primary = False)
    plot_loss(h2)
