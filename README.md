# iNaturalistClassifier

The main purpose of this repo is to help iNaturalist observers classify images into correct categories. This will allow users to easily create data sets from projects that have unclassified images, and run models on them.
I will utilize Artificial Intelligence and Machine Learning models to classify different fly datasets into male and female categories. The images will also be labeled according to whether or not the fly is eating a prey.

This project works by accessing the Inaturalist [API](https://api.inaturalist.org/v1/docs) with python in order to download the desired images / metadata. Then the images will be classified with simple ai.

## How to run

Requires python 3.12+

setup the virtual env:

```sh
python -m venv ./env

# On Windows
. ./env/Scripts/activate 
# On Linux
./env/bin/activate

pip install -r requirements.txt
pip install -e .
```
