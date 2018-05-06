# Pokemon Type Classifier
This project aims to classify pokemon types given an pokemon image using convolutional neural networks.

# Dataset
The image dataset comes from [veekun](https://veekun.com/dex/downloads) containing pokemon sprite images from games spanning Generation I to V, as well as icons, Global-Link artwork, and the spinoff Pokemon Conquest.

The pokemon stat and type data comes from [kaggle](https://www.kaggle.com/abcsds/pokemon) and contains id, stats, type, and legendary status information on all the pokemon to date.

# Package requirements
To run the code, use `python3`, and ensure the following packages are installed:
Tensorflow
Keras
Matplotlib
Numpy
Pandas

There have been some issues with loading the models in the `anaconda` environment due to serialization, but packages installed with `pip3` should work fine. If an issue occurs, one can always retrain the models by running ``` python3 cnn.py ```

# Running the code
