# -*- coding: utf-8 -*-

import numpy as np 
import keras
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img 
from keras.models import Sequential 
from keras import optimizers
from keras.preprocessing import image
from keras.layers import Dropout, Flatten, Dense 
from keras import applications 
from keras.layers.advanced_activations import LeakyReLU



class Cnn:
   def __init__(self):
      self._vgg16 = None
      self._model = None
      self._classes = ['Acanthurus Sohal','Amphiprion Ocellaris','Coris Formosa','Halichoeres Adustrus','Naso Elegans','Naso Vlamingi',
            'Paracanthurus Hepatus','Pseudathias Squamipinnis','Pterapogon Kauderni','Siganus Vulpinus','Sphaeramia Nematoptera',
            'Zebrasoma Flavescens','Zebrasoma Veliferum']
      self._classFamily = ['Acanthuridae', 'Pomacentridae', 'Labridae', 'Labridae', 'Acanthuridae', 'Acanthuridae', 'Acanthuridae',
                          'Serranidae', 'Apogonidae', 'Siganidae', 'Apogonidae', 'Acanthuridae', 'Acanthuridae']
      self._classDeepRange = [[0,20], [3,15], [2,50], [1,3], [5,30], [1,50], [2,40], [2,20], [1,3], [1,30], [1,14],
                         [2,40], [2,30]]
      #Default confidence to accept a prediction is 90
      self._confidence=90

   def setConfidence(self,confidence):
      self._confidence = confidence

   def startCnn(self):
      self._vgg16 = applications.VGG16(include_top=False, weights='imagenet')
      model = Sequential() 
      model.add(Flatten(input_shape=(7, 7, 512))) 
      model.add(Dense(100, activation=LeakyReLU(alpha=0.3))) 
      model.add(Dropout(0.5)) 
      model.add(Dense(50, activation=LeakyReLU(alpha=0.3))) 
      model.add(Dropout(0.3)) 
      model.add(Dense(13, activation='softmax'))
      model.compile(loss='categorical_crossentropy',
         optimizer=optimizers.RMSprop(lr=1e-4),
         metrics=['acc'])
      model.load_weights('cnn_weights.h5')
      self._model = model

   def readImage(self, img):
      #This is used if image from path is load
      #image = load_img(path, target_size=(224, 224)) 
      #print(type(image))
      #image = img_to_array(image) 
      #print(type(image))
      image = img
      image = np.expand_dims(image, axis=0)
      image /= 255. 
      return image

   def predictImage(self, image):
      vggPredictions = self._vgg16.predict(self.readImage(image)) 
      predictions = self._model.predict_proba(vggPredictions)

      #ID of the fish with the higher score is extracted
      predictedFish = list(predictions[0]).index(max(predictions[0]))
      #Score is calculated for the prediction in 100 scale
      score = np.round(100*predictions[0][predictedFish],2)

      #If the score if bigger than the confidence, then the predicition is returned
      if (score >= self._confidence):
         #print("ID: {}  Name: {} Percentage: {}".format(predictedFish,self._classes[predictedFish],100*predictions[0][predictedFish]))
         return [predictedFish, self._classes[predictedFish], score, self._classFamily[predictedFish], self._classDeepRange[predictedFish]]
      #Otherwise, nothing is returned
      else:
         #print("Nothing")
         return None
