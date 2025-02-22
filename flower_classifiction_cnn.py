# -*- coding: utf-8 -*-

# Setting the data
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pickle

data_dir = "../data/train/"

categories = ["daisy", "dandelion", "rose", "sunflower", "tulip"]

data = []

def make_data():
    for category in categories:
        path = os.path.join(data_dir, category)
        label = categories.index(category)

        for img_name in os.listdir(path):
            image_path = os.path.join(path, img_name)
            image = cv2.imread(image_path)

            try:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                image = cv2.resize(image, (224, 224))

                image = np.array(image, dtype=np.float32)

                data.append([image, label])

            except Exception as e:
                pass

    print(len(data))

    pik = open("data.pickle", "wb")
    pickle.dump(data, pik)
    pik.close()

make_data()

def load_data():
    pick = open('data.pickle','rb')
    data = pickle.load(pick)
    pick.close()

    np.random.shuffle(data)

    feature = []
    labels = []

    for img,label in data:
        feature.append(img)
        labels.append(label)

    feature = np.array(feature, dtype=np.float32)
    labels = np.array(labels)

    feature = feature/255.0

    return [feature,labels]

"""# Making the CNN Model"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

(feature,labels) = load_data()

xtrain,xtest,ytrain,ytest = train_test_split(feature, labels, test_size = 0.1)

categories = ["daisy", "dandelion", "rose", "sunflower", "tulip"]

input_layer = tf.keras.layers.Input([224,224,3])

conv1= tf.keras.layers.Conv2D(filters=32, kernel_size=(5,5), activation='relu',padding='same')(input_layer)
pool1 = tf.keras.layers.MaxPooling2D(pool_size=(2,2))(conv1)

conv2= tf.keras.layers.Conv2D(filters=64, kernel_size=(3,3), activation='relu',padding='same')(pool1)
pool2 = tf.keras.layers.MaxPooling2D(pool_size=(2,2),strides=(2,2))(conv2)

conv3= tf.keras.layers.Conv2D(filters=64, kernel_size=(3,3), activation='relu',padding='same')(pool2)
pool3 = tf.keras.layers.MaxPooling2D(pool_size=(2,2),strides=(2,2))(conv3)

conv4= tf.keras.layers.Conv2D(filters=96, kernel_size=(3,3), activation='relu',padding='same')(pool3)
pool4 = tf.keras.layers.MaxPooling2D(pool_size=(2,2),strides=(2,2))(conv4)

"""Flattening the convolution"""

flt1= tf.keras.layers.Flatten()(pool4)

"""Now making an ANN

"""

dn1= tf.keras.layers.Dense(512, activation='relu')(flt1)
output= tf.keras.layers.Dense(5,activation = 'softmax')(dn1)

model = tf.keras.Model(input_layer,output)

model.compile(optimizer='adam', loss = 'sparse_categorical_crossentropy',metrics=['accuracy'])

model.fit(xtrain,ytrain,batch_size=80,epochs=15)
model.save('mymodel.keras')

"""# Training done, now we will move towards testing

"""

model = tf.keras.models.load_model('mymodel.keras')

model.evaluate(xtest,ytest,verbose=1)

prediction = model.predict(xtest)

plt.figure(figsize=(15,15))

for i in range(25):
  plt.subplot(5,5,i+1)
  plt.imshow(xtest[i])
  plt.xlabel('Actual :' + categories[ytest[i]]+'\n'+ 'Predicted:'+ categories[np.argmax(prediction[i])])

  plt.xticks([])
plt.show()

