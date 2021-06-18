# defining function
def get_far(threshold, confusion_matrix):
  total_accept=0
  false_accept=0
  for i in range(len(confusion_matrix)):
    for j in range(len(confusion_matrix)):
      if i<=j:
        total_accept+=confusion_matrix[i][j]
      if i<j:
        false_accept+=confusion_matrix[i][j]

  return false_accept/ total_accept

def get_frr(threshold, confusion_matrix):
  total_reject=0
  false_reject=0
  for i in range(len(confusion_matrix)):
    for j in range(len(confusion_matrix)):
      if i>=j:
        total_reject+=confusion_matrix[i][j]
      if i>j:
        false_reject+=confusion_matrix[i][j]

  return false_reject/ total_reject

def get_predict(threshold, eval_X, num_class):
  real_pred=[]
  for ind in range(len(eval_X)):
    each_cos_sim_val= []
    for idx in range(num_class):
      each_cos_sim_val.append(globals()['cos_sim_list_'+str(idx)][ind])
    each_cos_sim_val.append(threshold)
    max_index= each_cos_sim_val.index(max(each_cos_sim_val))
    real_pred.append(max_index)

  return real_pred

from numpy import dot
from numpy.linalg import norm
def cos_sim(A, B):
       return dot(A, B)/(norm(A)*norm(B))

from sklearn.metrics import accuracy_score, confusion_matrix


import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import optimizers,regularizers
from tensorflow.keras.models import Sequential, load_model, model_from_json 
from tensorflow.keras.layers import Input,Conv2D,MaxPooling2D,Dense,Activation,Flatten,GlobalAveragePooling2D,GlobalMaxPooling2D,Dropout,AveragePooling2D,BatchNormalization,Softmax
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint
from tensorflow.python.framework.ops import disable_eager_execution
from sklearn.metrics import accuracy_score
from tensorflow.python.client import device_lib

# load data from numpy
X_data= np.load('/content/drive/MyDrive/Speaker_verification/data/raw_data/train_X.npy')
Y_data= np.load('/content/drive/MyDrive/Speaker_verification/data/raw_data/train_Y.npy')

# split data for training
from sklearn.model_selection import train_test_split
train_X, test_X, train_Y, test_Y= train_test_split(X_data, Y_data, test_size= 0.2,
                                                   stratify= Y_data, random_state= 200)

save_path= '/content/drive/MyDrive/Speaker_verification/result/raw_e2e_ASV/'

import tensorflow as tf
# Build Model
inp_shape = train_X.shape[1:]
def generate_model_cnn(mode='words', pooling=0, layers=3, kernel=11):
    model = Sequential()
    print("=================================Densenet=====================================")
    model.add(tf.keras.applications.DenseNet121(weights= None, include_top= False, input_shape= inp_shape))
    model.add(Flatten())
    model.add(Dense(128, activation = 'relu',kernel_regularizer=regularizers.l2(0.001)))
    model.add(Dropout(0.1))
    model.add(Dense(len(np.unique(train_Y)), activation = 'linear'))
    model.add(Softmax())
    return model

def generate_model(mode='words', summary=True):
    model = generate_model_cnn(mode=mode, pooling=0)
    if summary:
        model.summary()
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

callbacks_list  = [
    EarlyStopping( monitor = 'loss',  min_delta=0.001, patience=100,
                  verbose=1, mode='auto'),
    ModelCheckpoint(filepath = save_path+"/weights.{epoch:02d}-{val_loss:.4f}-{val_accuracy:.4f}.hdf5",
                    monitor = 'val_loss', save_best_only=True ),
    ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=7, verbose=1, min_delta=1e-4)]

model = generate_model(mode='words',summary=True)
history = model.fit(train_X, train_Y, epochs=300, batch_size=64, validation_data=(test_X,test_Y),callbacks=callbacks_list)

model_json = model.to_json()
output = model.predict(test_X)
predicted_classes = output.argmax(axis=1)
acc = accuracy_score(test_Y, predicted_classes)
with open(save_path+"/model_acc_{:.4f}.json".format(acc), 'w') as json_file:
    json_file.write(model_json)

#Weight save
model.save_weights(save_path +"/final_weight.h5")
model_json = model.to_json()
with open(save_path+"/model.json".format(acc), 'w') as json_file:
    json_file.write(model_json)

import keras
model= keras.models.Sequential(model.layers[:-3])


acc_list=[]
eer_list=[]
for z in range(1, 11):
  enroll_X= np.load('/content/drive/MyDrive/Speaker_verification/data/upgrade/enroll_{}/enroll_X.npy'.format(z)) # for verifying
  enroll_Y= np.load('/content/drive/MyDrive/Speaker_verification/data/upgrade/enroll_{}/enroll_Y.npy'.format(z))
  eval_X=np.load('/content/drive/MyDrive/Speaker_verification/data/upgrade/enroll_{}/eval_X.npy'.format(z)) # unknown
  eval_Y=np.load('/content/drive/MyDrive/Speaker_verification/data/upgrade/enroll_{}/eval_Y.npy'.format(z))

  enroll_X, temp_X, enroll_Y, temp_Y= train_test_split(enroll_X, enroll_Y, test_size= 0.75, stratify= enroll_Y, random_state= 10) # 3:1 로 데이터 나눔 3-> enroll / 1 -> eval
  
  eval_X= np.concatenate((eval_X, temp_X), axis=0)
  eval_Y= np.concatenate((eval_Y, temp_Y), axis=0)

  predict_enroll= model.predict(enroll_X)
  predict_eval= model.predict(eval_X)


  enroll_speaker= list(enroll_Y)
  for ind in range(len(np.unique(enroll_Y))):
    globals()['class_X_'+str(ind)]=[]

  for ind, speaker in enumerate(enroll_Y):
    globals()['class_X_'+str(speaker)].append(predict_enroll[ind])

  for i in range(len(np.unique(enroll_Y))):
    globals()['mean_vector_'+str(i)]= np.mean(globals()['class_X_'+str(i)], axis=0)

  for ind in range(len(np.unique(enroll_Y))):
    globals()['cos_sim_list_'+str(ind)]= np.array([])
    for i in predict_eval:
      tmp= cos_sim(i, globals()['mean_vector_'+str(ind)])
      globals()['cos_sim_list_'+str(ind)]=np.append(globals()['cos_sim_list_'+str(ind)], tmp)
    globals()['cos_sim_list_'+str(ind)]= globals()['cos_sim_list_'+str(ind)].reshape(-1,1)


  thresholds= np.arange(0., 1., 0.01)
  accuracy_list=[]
  far_list=[]
  frr_list=[]
  for i in thresholds:
    accuracy_list.append(accuracy_score(eval_Y, get_predict(i, eval_X, len(set(enroll_Y)))))
    far_list.append(get_far(i, confusion_matrix(eval_Y,  get_predict(i, eval_X, len(set(enroll_Y))))))
    frr_list.append(get_frr(i, confusion_matrix(eval_Y,  get_predict(i, eval_X, len(set(enroll_Y))))))


  for i in range(len(thresholds)):
    if far_list[i]<=frr_list[i]:
      final_index=i


  from sklearn.metrics import confusion_matrix, accuracy_score
  print(confusion_matrix(eval_Y, get_predict(thresholds[final_index], eval_X, len(set(enroll_Y)))))
  print()
  print('accuracy:',accuracy_score(eval_Y, get_predict(thresholds[final_index], eval_X, len(set(enroll_Y)))))
  print('EER:', far_list[final_index])
  print()
  acc_list.append(round(accuracy_score(eval_Y, get_predict(thresholds[final_index], eval_X, len(set(enroll_Y)))),4))
  eer_list.append(round(far_list[final_index],4))


print('acc_list:', acc_list)
print('eer_list:', eer_list)