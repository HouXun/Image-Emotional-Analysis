import cv2
import numpy as np
import os
import shutil

class Filter():
    def filterByHist(self,orig_dir,dst_dir):
        fnames = os.listdir(orig_dir)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
        for fname in fnames:
            fpath = os.path.join(orig_dir, fname)
            image = cv2.imread(fpath, 0)
            array = image.flatten()
            hist, bins = np.histogram(array, bins=10)
            total = np.sum(hist)
            hist = [h / total for h in hist]
            if max(hist) > 0.7:
                # print(fname)
                shutil.move(fpath, dst_dir)

filter_obj=Filter()
base_dir='D:/tumblr/photos'
filter_dir='D:/tumblr/filter'
emotion_list = ['Happy', 'Calm', 'Sad', 'Scared', 'Bored', 'Angry', 'Annoyed', 'Love', 'Excited', 'Surprised','Optimistic', 'Amazed', 'Ashamed', 'Disgusted', 'Pensive']
for emotion in emotion_list:
    print(emotion)
    orig_dir=os.path.join(base_dir,emotion)
    dst_dir=os.path.join(filter_dir,emotion)
    filter_obj.filterByHist(orig_dir,dst_dir)