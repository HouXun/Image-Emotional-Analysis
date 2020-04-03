import os
import cv2
def loaddata(base_dir):
    emotion_list=os.listdir(base_dir)
    kinds=len(emotion_list)
    data=[]
    labels=[]
    for i,emotion in enumerate(emotion_list):
        emotion_path=os.path.join(base_dir,emotion)
        print(emotion_path)
        image_path_list=os.listdir(emotion_path)
        for image_name in image_path_list:
            image_path=os.path.join(emotion_path,image_name)
            image=cv2.imread(image_path)
            image = cv2.resize(image, (100, 100), interpolation=cv2.INTER_CUBIC)
            data.append(image)
            label=[0]*kinds
            label[i]=1
            labels.append(label)
    return data,labels


#emotion_list = ['Happy', 'Calm', 'Sad', 'Scared', 'Bored', 'Angry', 'Annoyed', 'Love', 'Excited', 'Surprised','Optimistic', 'Amazed', 'Ashamed', 'Disgusted', 'Pensive']