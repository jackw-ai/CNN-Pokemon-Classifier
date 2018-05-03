# (c) 2018 Tingda Wang, Tongyu Zhou
# loads model from training and performs prediction on random test image

# Importing the Keras libraries and packages                                                 
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import plot_model
from keras.models import load_model

import numpy as np
import os,random, sys, re

from preprocess import get_pokemon

# shape of image (SHAPE, SHAPE)
SHAPE = 32

def load_models():
    ''' loads the models '''
    classifier = load_model("model/classifier1.h5")
    classifier2 = load_model("model/classifier2.h5")
    print("Loaded classifiers from disk")
    return classifier, classifier2

def load_image(imagepath):
    ''' helper to load image '''
    test_image = image.load_img(imagepath, target_size = (32, 32))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    return test_image

def run(evaluate = True, predict = True):
    
    classifier, classifier2 = load_models()

    # tests
    test = 'type1_sorted/test'
    path = test + '/' + random.choice([x for x in os.listdir(test) if os.path.isdir(os.path.join(test, x))])
    imagepath = path + '/' + random.choice(os.listdir(path))

    # load test sets
    test_datagen = ImageDataGenerator(rescale = 1./255)
    test_set = test_datagen.flow_from_directory(test, target_size = (32, 32), batch_size = 32, class_mode = 'categorical')
    test_set2 = test_datagen.flow_from_directory('type2_sorted/test', target_size = (32, 32), batch_size = 32, class_mode = 'categorical')
    
    if predict:
        test_image = load_image(imagepath)
        result1 = classifier.predict_classes(test_image)
        result2 = classifier2.predict_classes(test_image)

        predicted_type = [type for type, index in test_set.class_indices.items() if index == result1[0]][0]
    
        predicted_type2 = [type for type, index in test_set2.class_indices.items() if index == result2[0]][0]
 
        pokemon = get_pokemon(imagepath)
        second = "" if pokemon.type2 == 'None' else " and type " + pokemon.type2
        pred_sec = "" if predicted_type2 == 'None' else " and " + predicted_type2
        print("The Pokemon " + pokemon.name + " has type " + pokemon.type1 + second)
        print("The predicted type is " + predicted_type + second)

    if evaluate:
        print("Primary Type:")
        accuracy = classifier.evaluate_generator(test_set)
        print("Loss: ", accuracy[0])
        print("Accuracy: ", accuracy[1])

        print("Secondary:")
        accuracy2 = classifier2.evaluate_generator(test_set2)
        print("Loss: ", accuracy2[0])
        print("Accuracy: ", accuracy2[1])

if __name__ == "__main__":
    run()
