# Pokemon Type Classifier
This project aims to classify pokemon types given an pokemon image using convolutional neural networks.

![Pokemon!](/figures/preds.png)

# Dataset
The image dataset comes from [veekun](https://veekun.com/dex/downloads) containing pokemon sprite images from games spanning Generation I to V, as well as icons, Global-Link artwork, and the spinoff Pokemon Conquest.

The pokemon stat and type data comes from [kaggle](https://www.kaggle.com/abcsds/pokemon) and contains id, stats, type, and legendary status information on all the pokemon to date.

# Package requirements
To run the code, use `python3`, and ensure the following packages are installed:
`Tensorflow`,
`Keras`,
`Matplotlib`,
`Numpy`,
`Pandas`,

There have been some issues with loading the models in the `anaconda` environment due to serialization, but packages installed with `pip3` should work fine. If an issue occurs, one can always retrain the models by running ``` python3 cnn.py ```

# Running the code
## Preprocessing The Data
`preprocess.py` contains the necessary functions to preprocess the image and pokemon type data necessary for training. Running 

 ```python3 preprocess.py```

will create new sets of training and test data taken from the `data/` directory divided into primary and secondary types in `type1_sorted` and `type2_sorted` respectively. `preprocess.py` also contains an image resizing function by Hemagso taken from his repo [here](https://github.com/hemagso/neuralmon/blob/master/utility/preprocessing.py). The necessary functions to extract pokemon name and type information from the pokemon csv dataset from [kaggle](https://www.kaggle.com/abcsds/pokemon) are all contained in this program as well.
 
 ## Data Visualization
 `visualization.py` contains the necessary functions to visualize the dataset as well as various model performance metrics. Running the program will print some same plots. However, these functions are intended for use in other parts of the project as well as for generating figures for the final writeup.
 
![Sample Figure(1)](/figures/Mewtwo.png)

![Sample Figure(2)](/figures/conquest.png)

 ## Model Training
 `cnn.py` contains the functions to build, train, and save the convolutional neural network models. Running 
 
 ```python3 cnn.py```
 
 will begin training the primary and secondary type models on the test and training data sets. The classifiers, after training for 20 epochs, will be saved to `\model` as `.h5` files. Optional training accuracy and loss charts will be generated as well as a `.png` representation of the model architecture such as:
 
 ![Classifier](/model/classifier1.png)
 
 ## Running Predictions and Evaluations on the Models
 `run.py` contains the necessary functions to load the model and preform predictions and evaluations. Running
 
 ```python3 run.py```
 
 will perform load the saved models and perform primary and secondary type predictions on a random pokemon image from the dataset such as 
 
 ![Sample Figure(3)](/figures/pred5.png)

The program will then perform evaluations on the test sets using the `evaluation_generator` function from `Keras` to return the test accuracy and loss in the writeup. Furthermore, the program will compute the precision, recall, and f-score metrics on the entire test set and print to the terminal screen. These statistics were included in the final writeup as well.

# Extension: Fun Pokemon Type Classification Game!!!
![Pokemon Type Classification Game!](/figures/GUI.png)

To aid in visualizing the project, we created a GUI that will pit the player against the model in predicting the type of random pokemon. As an advantage for the player, there will only be four options to choose from whereas the model must infer the type from all 18 possiblities. We hope this can be a fun way to evaluate the model performance and serve as a homage to the pokemon games of our childhood.

The GUI and game was made using the `Tkinter` package in `python3`. To play, simply launch:

```python3 GUI.py```
