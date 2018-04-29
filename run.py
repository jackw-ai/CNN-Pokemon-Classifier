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
import os,random, sys

# load json and create model
json_file = open('model/classifier.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
classifier = model_from_json(loaded_model_json)
# load weights into new model
classifier.load_weights("model/classifier.h5")
print("Loaded classifier from disk")

# tests
test = 'type1_sorted/test'
path = test
path += '/' + random.choice([x for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))])
a = random.choice(os.listdir(path))

test_image = image.load_img(path+'/'+a, target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = classifier.predict_classes(test_image)

test_datagen = ImageDataGenerator(rescale = 1./255)
test_set = test_datagen.flow_from_directory(test, target_size = (64, 64), batch_size = 32,
                                            class_mode = 'categorical')

# print(test_set.class_indices)
# print(a)
predicted_type = [type for type, index in test_set.class_indices.items() if index == result[0]][0]
print("The actual type is " + path.split('/')[-1])
print("The predicted type is " + predicted_type)
