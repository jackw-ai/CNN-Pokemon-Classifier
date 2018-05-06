# Pokemon Type Classifier
This project aims to classify pokemon types given an pokemon image using convolutional neural networks.

# Dataset
The image dataset comes from [veekun](https://veekun.com/dex/downloads) containing pokemon sprite images from games spanning Generation I to V, as well as icons, Global-Link artwork, and the spinoff Pokemon Conquest.

The pokemon stat and type data comes from [kaggle](https://www.kaggle.com/abcsds/pokemon) and contains id, stats, type, and legendary status information on all the pokemon to date.

# Package requirements
To run the code, use `python3`, and ensure the following packages are installed:
Tensorflow,
Keras,
Matplotlib,
Numpy,
Pandas,

There have been some issues with loading the models in the `anaconda` environment due to serialization, but packages installed with `pip3` should work fine. If an issue occurs, one can always retrain the models by running ``` python3 cnn.py ```

# Running the code
## Preprocessing The Data
`preprocess.py` contains the necessary functions to preprocess the image and pokemon type data necessary for training. Running 
 ```python3 preprocess.py```
 will create new sets of training and test data taken from the `data/` directory divided into primary and secondary types in `type1_sorted` and `type2_sorted` respectively. `preprocess.py` also contains an image resizing function by Hemagso taken from his repo [here](https://github.com/hemagso/neuralmon/blob/master/utility/preprocessing.py). The necessary functions to extract pokemon name and type information from the pokemon csv dataset from [kaggle](https://www.kaggle.com/abcsds/pokemon) are all contained in this program as well.
 
 ## Data Visualization
 `visualization.py` contains the necessary functions to visualize the dataset as well as various model performance metrics. Running the program will print some same plots. However, these functions are intended for use in other parts of the project as well as for generating figures for the final writeup.
 
 ## Model Training
 `cnn.py` contains the functions to build, train, and save the convolutional neural network models. Running 
 ```python3 cnn.py```
 will begin training the primary and secondary type models on the test and training data sets. The classifiers, after training for 20 epochs, will be saved to `\model` as `.h5` files. Optional training accuracy and loss charts will be generated as well as a `.png` representation of the model architecture such as 
 
 ![Classifier](/model/classifier1.png)
 
 ## Running Predictions and Evaluations on the Models
 `run.py
