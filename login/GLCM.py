#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import math

# 定义最大灰度级数
gray_level = 16

class GLCM():
    def maxGrayLevel(self,img):
        max_gray_level = 0
        (height, width) = img.shape
        print
        height, width
        for y in range(height):
            for x in range(width):
                if img[y][x] > max_gray_level:
                    max_gray_level = img[y][x]
        return max_gray_level + 1


    def getGlcm(self,input, d_x, d_y):
        srcdata = input.copy()
        ret = [[0.0 for i in range(gray_level)] for j in range(gray_level)]
        (height, width) = input.shape

        max_gray_level = self.maxGrayLevel(input)

        # 若灰度级数大于gray_level，则将图像的灰度级缩小至gray_level，减小灰度共生矩阵的大小
        if max_gray_level > gray_level:
            for j in range(height):
                for i in range(width):
                    srcdata[j][i] = srcdata[j][i] * gray_level / max_gray_level

        for j in range(height - d_y):
            for i in range(width - d_x):
                rows = srcdata[j][i]
                cols = srcdata[j + d_y][i + d_x]
                ret[rows][cols] += 1.0

        for i in range(gray_level):
            for j in range(gray_level):
                ret[i][j] /= float(height * width)
        return ret


    def feature_computer(self,p):
        Con = 0.0
        Ent = 0.0
        Asm = 0.0
        Idm = 0.0
        for i in range(gray_level):
            for j in range(gray_level):
                Con += (i - j) * (i - j) * p[i][j]
                Asm += p[i][j] * p[i][j]
                Idm += p[i][j] / (1 + (i - j) * (i - j))
                if p[i][j] > 0.0:
                    Ent += p[i][j] * math.log(p[i][j])
        return [Asm, Con, -Ent, Idm]


    def glcmFeature(self,img):
        try:
            img_shape = img.shape
        except:
            print('imread error')
            return

        #img = cv2.resize(img, (int(img_shape[1] / 2), int(img_shape[0] / 2)), interpolation=cv2.INTER_CUBIC)
        #img = cv2.resize(img, (img_shape[1], img_shape[0]), interpolation=cv2.INTER_CUBIC)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        glcm_0=self.getGlcm(img_gray, 1,0)
        glcm_1=self.getGlcm(img_gray, 0,1)
        glcm_2=self.getGlcm(img_gray, 1,1)
        #glcm_3=getGlcm(src_gray, -1,1) error

        output=[]
        output.extend(self.feature_computer(glcm_0))
        output.extend(self.feature_computer(glcm_1))
        output.extend(self.feature_computer(glcm_2))
        return output

