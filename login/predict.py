import cv2
import os
import numpy as np
import keras
from keras import models,layers
from keras.models import load_model
from keras.applications import InceptionV3
from login.feature import getCombineFeatures

def getImages(url_list):
    images=[]
    for url in url_list:
        image=cv2.imread(url)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_CUBIC)
        images.append(image)
    images=np.asarray(images).astype('float32')
    print("images.shape: ",images.shape)
    return images

def getLabels(images):
    keras.backend.clear_session()
    emotion_list=['Happy', 'Calm', 'Sad', 'Scared', 'Bored', 'Angry', 'Annoyed', 'Love', 'Excited', 'Surprised','Optimistic', 'Amazed', 'Ashamed', 'Disgusted', 'Pensive']
    conv_base = InceptionV3(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

    test_features=conv_base.predict(images)
    test_features = np.reshape(test_features, (len(images), 5 * 5 * 2048))
    print("test_features.shape: ",test_features.shape)

    model=load_model('D:/mysite/Inception_15types.h5')
    predictions=model.predict(test_features)
    labels=[]
    for prediction in predictions:
        prediction=list(prediction)
        index=prediction.index(max(prediction))
        labels.append(emotion_list[index])
    return labels

def getLabelsInnovation(images,url_list):
    keras.backend.clear_session()
    emotion_list = ['Happy', 'Calm', 'Sad', 'Scared', 'Bored', 'Angry', 'Annoyed', 'Love', 'Excited', 'Surprised',
                    'Optimistic', 'Amazed', 'Ashamed', 'Disgusted', 'Pensive']
    conv_base = InceptionV3(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    test_features = conv_base.predict(images)
    test_features = np.reshape(test_features, (len(images), 5 * 5 * 2048))
    model = models.Sequential()
    model.add(layers.Dense(1024, activation='relu', input_dim=5 * 5 * 2048))
    test_features=model.predict(test_features)

    combine_features = getCombineFeatures(url_list)
    test_features=np.append(test_features,combine_features,axis=1)
    print('test_features: ',test_features.shape)

    model = load_model('D:/mysite/Innovation_15types.h5')
    predictions = model.predict(test_features)
    labels = []
    for prediction in predictions:
        prediction = list(prediction)
        index = prediction.index(max(prediction))
        labels.append(emotion_list[index])
    return labels