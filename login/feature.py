from login.HSV import HSV
from login.GLCM import GLCM
from login.HOG import HOG
from login.LBP import LBP

import cv2
import numpy as np
from sklearn import preprocessing

def extractfeature(data):
    print("[feature] start")
    hsv_obj = HSV()
    glcm_obj = GLCM()
    hog_obj=HOG()
    lbp_obj=LBP(8,1)

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

    hog_features=hog_obj.getFeatVecs(data_vstack)
    lbp_features=lbp_obj.getFeatVecs(data_vstack)
    lbp_features = [feature[0:10] for feature in lbp_features]
    print("[feature] end")
    return hsv_features,glcm_features,hog_features,lbp_features

def postprocessing(features):
    normalizer = preprocessing.Normalizer().fit(features)
    features = normalizer.transform(features)
    return features

def combine(features_list):
    output=features_list[0]
    for features in features_list[1:]:
        output=np.append(output,features,axis=1)
    return output

def getCombineFeatures(url_list):
    data=[]
    for url in url_list:
        image = cv2.imread(url)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (100, 100), interpolation=cv2.INTER_CUBIC)
        data.append(image)

    hsv_features,glcm_features,hog_features,lbp_features=extractfeature(data)
    """
    hsv_features=postprocessing(hsv_features)
    glcm_features=postprocessing(glcm_features)
    hog_features=postprocessing(hog_features)
    lbp_features=postprocessing(lbp_features)

    """

    combine_features=combine([hsv_features,glcm_features,hog_features,lbp_features])
    print('combine_features.shape: ',combine_features.shape)
    return combine_features

