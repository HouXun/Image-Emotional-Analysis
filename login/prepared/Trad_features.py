from login.HSV import HSV
from login.GLCM import GLCM
from login.HOG import HOG
from login.LBP import LBP
from .load import loaddata

import cv2
import csv
import numpy as np
from sklearn import preprocessing
from sklearn.decomposition import PCA

def extractfeature(data):
    print("[feature] start")
    hsv_obj = HSV()
    glcm_obj = GLCM()
    hog_obj=HOG()
    lbp_obj=LBP(8,1)

    print("[feature] hsv")
    print("[feature] glcm")
    hsv_features = []
    glcm_features = []

    data_vstack=[]
    for image in data:
        hsv_feature=hsv_obj.getFeatures(image)
        glcm_feature = glcm_obj.glcmFeature(image)
        hsv_features.append(hsv_feature)
        glcm_features.append(glcm_feature)

        b, g, r = cv2.split(image)
        temp = np.vstack((r,g,b))
        data_vstack.append(temp)


    print("[feature] hog")
    hog_features=hog_obj.getFeatVecs(data_vstack)
    print("[feature] lbp")
    lbp_features=lbp_obj.getFeatVecs(data_vstack)
    lbp_features=[feature[:10] for feature in lbp_features]
    print("[feature] end")
    return hsv_features,glcm_features,hog_features,lbp_features

def postpreprocessing(features):
    normalizer = preprocessing.Normalizer().fit(features)
    features = normalizer.transform(features)
    return features

def combine(features_list):
    output=features_list[0]
    for features in features_list[1:]:
        output=np.append(output,features,axis=1)
    return output

def saveAsCsv(data,path):
    csvFile = open(path, 'w', newline='')  # 设置newline，否则两行之间会空一行
    writer = csv.writer(csvFile)
    for row in data:
        writer.writerow(row)
    csvFile.close()

def start(base_dir,dst_dir):
    data,labels=loaddata(base_dir)

    hsv_features,glcm_features,hog_features,lbp_features=extractfeature(data)

    hsv_features=postpreprocessing(hsv_features)
    glcm_features=postpreprocessing(glcm_features)
    hog_features=postpreprocessing(hog_features)
    lbp_features=postpreprocessing(lbp_features)

    combine_features=combine([hsv_features,glcm_features,hog_features,lbp_features])

    saveAsCsv(combine_features,dst_dir+'/'+'combine_features.csv')
    saveAsCsv(labels,dst_dir+'/'+'labels.csv')

dir_list=['train','validation','test']
base_dir='D:/tumblr/photos_small/'
dst_dir='D:/tumblr/hsv_glcm_hog_lbp/'
for dir in dir_list:
    print(dir)
    start(base_dir+dir,dst_dir+dir)

