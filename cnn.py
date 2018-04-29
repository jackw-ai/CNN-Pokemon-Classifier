# (c) 2018 Tongyu Zhou, Tingda Wang
# trains CNN and saves classifier to .json and .h5

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import model_from_json
import numpy as np
import os,random, sys

def create_cnn(primary = True):
    ''' builds a model for primary or secondary types and saves the model '''
    classifier = Sequential()
    classifier.add(Conv2D(32, (3, 3), input_shape = (64, 64, 3), activation = 'relu'))
    classifier.add(MaxPooling2D(pool_size = (2, 2)))
    classifier.add(Flatten())
    #classifier.add(Dense(units = 128, activation = 'relu'))
    #classifier.add(Dense(units = 1, activation = 'sigmoid'))
    classifier.add(Dense(128, input_dim=4, activation='relu'))

    categories = 18 if primary else 19

    classifier.add(Dense(categories, activation='softmax'))
    classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

    train_datagen = ImageDataGenerator(rescale = 1./255, shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True)
    test_datagen = ImageDataGenerator(rescale = 1./255)

    train = 'type1_sorted/train' if primary else 'type2_sorted/train' 
    test = 'type1_sorted/test' if primary else 'type2_sorted/test' 

    training_set = train_datagen.flow_from_directory(train, target_size = (64, 64), batch_size = 32, class_mode = 'categorical')
    test_set = test_datagen.flow_from_directory(test, target_size = (64, 64), batch_size = 32, class_mode = 'categorical')

    classifier.fit_generator(training_set, steps_per_epoch = 752, epochs = 5, 
                         validation_data = test_set, validation_steps = 188)

    # save the classifier
    classifier_json = classifier.to_json()

    if not os.path.exists(os.path.dirname("model/")):
        os.makedirs(os.path.dirname("model/"))
    filename = "classifier1" if primary else "classifier2"
    with open("model/" + filename + ".json", "w") as json_file:
        json_file.write(classifier_json)

    # serialize weights to HDF5
    classifier.save_weights("model/" + filename + ".h5")
    print("Saved model to disk")

# build classifier for type 2
create_cnn(False)
