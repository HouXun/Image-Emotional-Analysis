import pandas as pd
import os
from keras import models,layers,optimizers

train_features_path='G:/train_features.csv'
validation_features_path='G:/validation_features.csv'
test_features_path='G:/test_features.csv'
train_labels_path='G:/train_labels.csv'
validation_labels_path='G:/validation_labels.csv'
test_labels_path='G:/test_labels.csv'

train_features=pd.read_csv(train_features_path,header=None)
validation_features=pd.read_csv(validation_features_path,header=None)
test_features=pd.read_csv(validation_features_path,header=None)
train_labels=pd.read_csv(train_labels_path,header=None)
validation_labels=pd.read_csv(validation_labels_path,header=None)
test_labels=pd.read_csv(validation_labels_path,header=None)



def getModel():
    model=models.Sequential()
    model.add(layers.Dense(256,activation='relu',input_dim=4394))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(15,activation='softmax'))

    model.compile(optimizer=optimizers.RMSprop(lr=2e-5),
              loss='categorical_crossentropy',
              metrics=['acc'])
    return model

model=getModel()
history=model.fit(train_features,
                  train_labels,epochs=100,verbose=0,
                  validation_data=(validation_features,validation_labels))

model.save('Inception_15types.h5')

import matplotlib.pyplot as plt
acc=history.history['acc']
val_acc=history.history['val_acc']
loss=history.history['loss']
val_loss=history.history['val_loss']
epochs=range(1,len(acc)+1)
plt.plot(epochs,acc,'bo',label='Training acc')
plt.plot(epochs,val_acc,'b',label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()
plt.figure()

plt.plot(epochs,loss,'bo',label='Training loss')
plt.plot(epochs,val_loss,'b',label='Validation loss')
plt.title('Training and validation loss')
plt.legend()
plt.show()

print(val_acc.index(max(val_acc)))
print(max(val_acc))
test_loss,test_acc=model.evaluate(test_features,test_labels)
print(test_acc)


emotion_list = ['Happy', 'Calm', 'Sad', 'Scared', 'Bored', 'Angry', 'Annoyed', 'Love', 'Excited', 'Surprised',
                    'Optimistic', 'Amazed', 'Ashamed', 'Disgusted', 'Pensive']
test_num_list=[]
for emotion in emotion_list:
    dst_dir=os.path.join('D:/tumblr/photos_small/test',emotion)
    fnames=os.listdir(dst_dir)
    test_num_list.append(len(fnames))

test_acc_list=[]
start=0
end=0
for num in test_num_list:
    end+=num
    test_loss,test_acc=model.evaluate(test_features[start:end],test_labels[start:end])
    start=end
    test_acc_list.append(test_acc)

plt.figure(figsize=(15, 8), dpi=80)
width = 0.5
p2 = plt.bar(emotion_list, test_acc_list, width, label="Accuracy", color="#87CEFA")
plt.xlabel('Emotion Type')
plt.ylabel('Testing Accuracy')
plt.title('Testing Result')
plt.legend(loc="upper right")
plt.show()