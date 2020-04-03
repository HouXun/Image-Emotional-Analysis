import os
import csv
import numpy as np
import pandas as pd
from keras.applications import InceptionV3
from keras.preprocessing.image import ImageDataGenerator
from keras import models,layers

emotion_list=['Happy','Calm','Sad','Scared','Bored','Angry','Annoyed','Love','Excited','Surprised','Optimistic','Amazed','Ashamed','Disgusted','Pensive']

train_num=5144
val_num=2575
test_num=2575
train_dir='D:/tumblr/photos_small/train'
validation_dir='D:/tumblr/photos_small/validation'
test_dir='D:/tumblr/photos_small/test'

conv_base=InceptionV3(weights='imagenet',include_top=False,input_shape=(224,224,3))

datagen=ImageDataGenerator(rescale=1./255)
batch_size=20

def extract_features(directory,sample_count):
    features=np.zeros(shape=(sample_count,5,5,2048))
    labels=np.zeros(shape=(sample_count,15))
    generator=datagen.flow_from_directory(directory,
                                          target_size=(224,224),
                                          batch_size=batch_size,
                                          class_mode='categorical')
    i=0
    for inputs_batch,labels_batch in generator:
        #print(labels_batch)
        features_batch=conv_base.predict(inputs_batch)
        features[i*batch_size:(i+1)*batch_size]=features_batch
        labels[i*batch_size:(i+1)*batch_size]=labels_batch
        i+=1
        if i*batch_size>=sample_count:
            break
    return features,labels

train_features,train_labels=extract_features(train_dir,train_num)
validation_features,validation_labels=extract_features(validation_dir,val_num)
test_features,test_labels=extract_features(test_dir,test_num)

train_features=np.reshape(train_features,(train_num,5*5*2048))
validation_features=np.reshape(validation_features,(val_num,5*5*2048))
test_features=np.reshape(test_features,(test_num,5*5*2048))


model=models.Sequential()
model.add(layers.Dense(1024,activation='relu',input_dim=5*5*2048))

train_features=model.predict(train_features)
validation_features=model.predict(validation_features)
test_features=model.predict(test_features)

def load_data(features_path):
    data=pd.read_csv(features_path,header=None)
    features=data.values
    return features

train_features=np.append(train_features,
                    load_data('D:/tumblr/hsv_glcm_hog_lbp/train/combine_features.csv')
                         ,axis=1)
validation_features=np.append(validation_features,
                    load_data('D:/tumblr/hsv_glcm_hog_lbp/validation/combine_features.csv')
                         ,axis=1)
test_features=np.append(test_features,
                    load_data('D:/tumblr/hsv_glcm_hog_lbp/test/combine_features.csv')
                         ,axis=1)

def saveAsCsv(data,path):
    csvFile = open(path, 'w', newline='')  # 设置newline，否则两行之间会空一行
    writer = csv.writer(csvFile)
    for row in data:
        writer.writerow(row)
    csvFile.close()

saveAsCsv(train_features,'G:/train_features.csv')
saveAsCsv(validation_features,'G:/validation_features.csv')
saveAsCsv(test_features,'G:/test_features.csv')
saveAsCsv(train_labels,'G:/train_labels.csv')
saveAsCsv(validation_labels,'G:/validation_labels.csv')
saveAsCsv(test_labels,'G:/test_labels.csv')