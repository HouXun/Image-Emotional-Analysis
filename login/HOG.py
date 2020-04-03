import numpy as np
from skimage import feature
from sklearn import preprocessing
import cv2

class HOG:

    def getVecLength(self):
        return 1764

    def getFeature(self,imgMat):
        feat=feature.hog(imgMat,orientations=9,pixels_per_cell=(16,16),cells_per_block=(2,2),block_norm='L2-Hys')
        feat=feat.reshape((1,-1))
        feat=preprocessing.normalize(feat)
        return feat

    def getFeatVecs(self,imgList):

        feats=None
        for mat in imgList:

            feat=self.getFeature(mat)
            if feats is None:
                feats=feat.copy()
            else:
                feats=np.append(feats,feat,axis=0)
        return feats



