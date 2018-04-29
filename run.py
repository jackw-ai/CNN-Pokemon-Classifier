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
from keras.models import model_from_json
import numpy as np
import os,random, sys, re

from preprocess import types

# for checking accuracy
type_dict = types('data/Pokemon-2.csv')

def get_type(filepath):
    ''' returns the Pokemon tuple based on file path '''
    filename = filepath.split('/')[-1]
    id = ''.join(re.findall(r'\b\d+\b', filename))
    return type_dict[id]
    
# load json and create model
json_file = open('model/classifier1.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
classifier = model_from_json(loaded_model_json)
# load weights into new model
classifier.load_weights("model/classifier1.h5")

json_file = open('model/classifier2.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
classifier2 = model_from_json(loaded_model_json)
# load weights into new model
classifier2.load_weights("model/classifier2.h5")
print("Loaded classifiers from disk")

# tests
test = 'type1_sorted/test'
path = test
path += '/' + random.choice([x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))])
imagepath = path + '/' + random.choice(os.listdir(path))

test_image = image.load_img(imagepath, target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result1 = classifier.predict_classes(test_image)
result2 = classifier2.predict_classes(test_image)

test_datagen = ImageDataGenerator(rescale = 1./255)
test_set = test_datagen.flow_from_directory(test, target_size = (64, 64), batch_size = 32,
                                            class_mode = 'categorical')
predicted_type = [type for type, index in test_set.class_indices.items() if index == result1[0]][0]

test_set2 = test_datagen.flow_from_directory('type2_sorted/test', target_size = (64, 64), batch_size = 32, class_mode = 'categorical')
predicted_type2 = [type for type, index in test_set2.class_indices.items() if index == result2[0]][0]

pokemon = get_type(imagepath)
second = "" if pokemon.type2 == 'None' else " and type " + pokemon.type2
pred_sec = "" if predicted_type2 == 'None' else " and " + predicted_type2
print("The Pokemon " + pokemon.name + " has type " + pokemon.type1 + second)
print("The predicted type is " + predicted_type + second)
