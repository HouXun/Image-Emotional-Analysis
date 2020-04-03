from django.test import TestCase
from keras.models import load_model
'''
from keras.applications import InceptionV3
conv_base = InceptionV3(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
print('finish')
'''

model = load_model('D:/mysite/Innovation_15types.h5')
print(model.summary())

# Create your tests here.
