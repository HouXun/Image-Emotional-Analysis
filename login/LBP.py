import numpy as np
from skimage import feature
from sklearn import preprocessing
import cv2
class LBP:
    def __init__(self,p,r):
        self.p=p
        self.r=r

    def getVecLength(self):
        return 2**self.p

    def getFeature(self,imgMat):
        feat=feature.local_binary_pattern(imgMat,self.p,self.r,method='uniform')
        re,_=np.histogram(feat,bins=range(256),range=(0,self.getVecLength()),normed=True)
        return re

    def getFeatVecs(self,imgList):
        feats=None
        for mat in imgList:
            feat=self.getFeature(mat)
            if feats is None:
                feats=feat.reshape((1,-1))
            else:
                feats=np.append(feats,feat.reshape((1,-1)),axis=0)
        return feats
