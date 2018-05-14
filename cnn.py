# (c) 2018 Tongyu Zhou, Tingda Wang, Xuanzhen Zhang
# trains ConvNet pokemon typ classifier and saves to .h5 file in \models

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import plot_model
from keras import optimizers
from keras import applications
from keras.layers.normalization import BatchNormalization
from keras.layers import Activation, Dense
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D



import numpy as np
import os,random, sys

from visualization import plot_loss

# shape of img: SHAPE x SHAPE
SHAPE = 32
FINE_TUNE_SHAPE = 48

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
    classifier.add(MaxPooling2D(pool_size = (2, 2)))
    classifier.add(Dropout(0.25))
    
    classifier.add(Conv2D(64, (3, 3), padding = 'same', activation = 'relu'))
    classifier.add(Conv2D(64, (3, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size = (2, 2)))
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
    classifier.summary()

    # returns built CNN
    return classifier

def create_cnn2(primary = True):
    ''' 
    creates the convolutional neural network classifier 
    returns the classfier for primary or secondary types
    '''

    # sequential layers
    model = Sequential()

    model.add(Conv2D(64, (3, 3),
                          padding = 'same',
                          input_shape = (SHAPE, SHAPE, 3),
                          activation = 'relu'))

    # add convolutional layers
    ''' 
    3 Convolutional Layers, maxpool layer follows 2 Conv2D layers
    3 Dropout layers to prevent overfitting
    after flatten, 2 dense layers to return output
    '''
   

    # we can think of this chunk as the input layer
    model.add(Dropout(0.5))

    # we can think of this chunk as the hidden layer    
    model.add(Dense(64, init='uniform'))
    model.add(BatchNormalization())
    model.add(Activation('tanh'))
    model.add(Dropout(0.5))

    # we can think of this chunk as the output layer
    categories = 18 if primary else 19

    model.add(Flatten())
    model.add(Dense(categories))
    model.add(BatchNormalization())
    model.add(Activation('softmax'))

    # returns built CNN
    return model

def fine_tune(primary = True):
    categories = 18 if primary else 19

    '''
    resnetmd = applications.resnet50.ResNet50(# include_top = False, input_shape = (FINE_TUNE_SHAPE,FINE_TUNE_SHAPE,3),weights='imagenet'
                                       )
    ftmodel = Sequential()
    
    for layer in resnetmd.layers:
        ftmodel.add(layer)
    ftmodel.layers.pop()
    
    for layer in ftmodel.layers:
        layer.trainable = False
        
    ftmodel.add(Flatten())

    ftmodel.add(Dense(categories, activation = 'softmax'))
    ftmodel.summary()
    '''
    
    
    vgg16md = applications.vgg16.VGG16(include_top = False, input_shape = (FINE_TUNE_SHAPE,FINE_TUNE_SHAPE,3),weights='imagenet'
                                       )
    
    
    # vgg16md.summary()
    ftmodel = Sequential()
    
    for layer in vgg16md.layers[:-8]:
        ftmodel.add(layer)
    # ftmodel.layers.pop()
    
    # for layer in ftmodel.layers[:-2]:
        # layer.trainable = False
    
    # ftmodel.summary()

    ftmodel.add(Flatten())
    ftmodel.add(Dropout(0.5))
    ftmodel.add(Dense(categories, activation = 'softmax'))

    ftmodel.summary()
    

    '''
    mbNet = applications.mobilenet.MobileNet(include_top = False, input_shape = (FINE_TUNE_SHAPE,FINE_TUNE_SHAPE,3),
                                       )
    
    
    ftmodel = Sequential()
    
    for layer in mbNet.layers:
        ftmodel.add(layer)
    # ftmodel.layers.pop()
    for layer in ftmodel.layers:
        layer.trainable = False

    # ftmodel.summary()

    ftmodel.add(Flatten())
    ftmodel.add(Dense(categories, activation = 'softmax'))

    ftmodel.summary()
    '''
    
    
    '''
    xceptionmd = applications.xception.Xception(include_top = False, input_shape = (FINE_TUNE_SHAPE,FINE_TUNE_SHAPE,3),weights='imagenet'
                                                )

    # xceptionmd.summary()
    
                                               
    ftmodel = Sequential()
    
    for layer in xceptionmd.layers:
        ftmodel.add(layer)
    
    # ftmodel.layers.pop()
    for layer in ftmodel.layers:
        layer.trainable = False

    ftmodel.summary()
    
    ftmodel.add(Flatten())
    ftmodel.add(layers.Dense(categories, activation = 'softmax'))

    ftmodel.summary()
    '''

    return ftmodel

def train_fine_tune(primary = True, save = True, plot_classifier = False):
    # get model
    ftmodel = fine_tune(primary)

    # batch size
    BATCH_SIZE = 64

    # number of training epochs
    EPOCHS = 20
    
    # uses adam optimizer and crossentropy loss function
    ftmodel.compile(optimizers.Adam(lr = 0.1),
                       loss = 'categorical_crossentropy',
                       metrics = ['accuracy'])

    # data augmentation: prevent overfitting by randomly transforming the training images
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

    # CreateImageGenerator
    

    # retrieve datasets
    training_set = train_datagen.flow_from_directory(train,
                                                     target_size = (FINE_TUNE_SHAPE, FINE_TUNE_SHAPE),
                                                     batch_size = BATCH_SIZE,
                                                     class_mode = 'categorical'
                                                            )
    
    test_set = train_datagen.flow_from_directory(test,
                                                target_size = (FINE_TUNE_SHAPE, FINE_TUNE_SHAPE),
                                                batch_size = BATCH_SIZE,
                                                class_mode = 'categorical'
                                                        )

    
    # training
    history = ftmodel.fit_generator(training_set,
                                       #steps_per_epoch = 752,
                                       #validation_steps = 188,
                                       epochs = EPOCHS, 
                                       validation_data = test_set,
                                       verbose = 2)

    
    # plots the model
    if plot_classifier:
        filepath = 'model/ftmodel1.png' if primary else 'model/ftmodel2.png'
        plot_model(ftmodel, to_file = filepath)
        print("Model plots saved to model/")

    # save the ftmodel
    if save:
        if not os.path.exists(os.path.dirname("model/")):
            os.makedirs(os.path.dirname("model/"))
        filename = "ftmodel1" if primary else "ftmodel2"
        ftmodel.save("model/" + filename + ".h5")
        print("Saved model to disk")

    # return classifier, history


def train(primary = True, save = True, plot_classifier = False):
    '''
    trains the model for primary or secondary types.
    Supports saving the model and plotting the model.
    Returns the classifier as well as history object for plotting.
    '''

    # get model
    classifier = create_cnn2(primary)

    # batch size
    BATCH_SIZE = 64

    # number of training epochs
    EPOCHS = 20
    
    # uses adam optimizer and crossentropy loss function
    classifier.compile(optimizer = 'adam',
                       loss = 'categorical_crossentropy',
                       metrics = ['accuracy'])

    # data augmentation: prevent further overfit by randomly transforming the training images
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
                                       validation_data = test_set)


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

    # fine_tune()
    
    # build classifier for type 1 and 2
    # _, h = train(primary = True, save = s, plot_classifier = plt)    
    _, h2 = train(primary = False, save = s, plot_classifier = plt)

    if plt: # plots accuracy and loss curves
        plot_loss(h)
        plot_loss(h2)



