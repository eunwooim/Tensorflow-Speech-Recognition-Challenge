import numpy as np
import pandas as pd
destpath = 
save_path = 

# Load MFCC
X_data = np.load(destpath+'X_10.npy')
Y_data = np.load(destpath+'Y_10.npy')

# Split train, test dataset
def split_dataset(Y,ratio=0.2):
    test_ix = np.array([])
    for i in np.unique(Y):
        idx = np.reshape(np.where(Y==i),-1)
        idx = np.random.choice(idx,int(len(idx)*ratio),False)
        test_ix = np.concatenate((test_ix,idx),axis=None)
    test_ix = np.sort(test_ix.astype(int))
    train_ix = list(set(range(len(temp)))-set(test_ix))
    return train_ix, test_ix

train_ix, test_ix = split_dataset(Y_data,0.1)
df = pd.DataFrame(test_ix)
df.to_csv(destpath+'testidx.csv',sep=',',header=False,
          float_format='%.2f',index=False)

csvpath = destpath+'testidx.csv'
test_ix = pd.read_csv(csvpath,header=None)[0]
train_ix = list(set(range(len(Y_data)))-set(test_ix))
train_X = X_data[train_ix]
train_Y = Y_data[train_ix]
test_X = X_data[test_ix]
test_Y = Y_data[test_ix]

# Shuffle data before training
tot_ix = range(len(train_X))
rand_ix = np.random.choice(tot_ix,len(train_X),False)
train_X = train_X[rand_ix]
train_Y = train_Y[rand_ix]

from keras.utils.np_utils import to_categorical
train_X = np.expand_dims(train_X,-1)
test_X = np.expand_dims(test_X,-1)
num_class = len(np.unique(Y_data))
train_Y = to_categorical(train_Y,num_class)
test_Y = to_categorical(test_Y,num_class)

import tensorflow as tf
from tensorflow.keras import optimizers,regularizers
from tensorflow.keras.models import Sequential, load_model, model_from_json 
from tensorflow.keras.layers import Conv2D,Dense,Activation,Flatten,Dropout,AveragePooling2D,BatchNormalization,Softmax,DepthwiseConv2D,LeakyReLU
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint
inp_shape = np.shape(train_X)[1:]

#Model building
def build_model():
    model = Sequential()
    model.add(Conv2D(filters=70, kernel_size=(3,3), strides = 1, padding ='same', input_shape=inp_shape, activation = 'relu'))
    model.add(AveragePooling2D(pool_size=(3,3), strides=2))
    model.add(DepthwiseConv2D(kernel_size=(3,3),strides=(1,1),padding='same'))
    model.add(Conv2D(filters=50, kernel_size=(3,3), strides = 1, padding ='same', activation = 'relu'))
    model.add(BatchNormalization())
    model.add(DepthwiseConv2D(kernel_size=(3,3),strides=(1,1),padding='same'))
    model.add(Conv2D(filters=30, kernel_size=(3,3), strides = 1, padding ='same', activation = 'relu'))
    model.add(BatchNormalization())    
    model.add(AveragePooling2D(pool_size=(3,3), strides=None))
    model.add(Flatten())
    model.add(Dense(50, activation = 'relu',kernel_regularizer=regularizers.l2(0.001)))
    model.add(Dropout(0.1))
    model.add(Dense(10, activation = 'linear'))
    model.add(LeakyReLU())
    model.add(Softmax())
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

callbacks_list  = [
    EarlyStopping( monitor = 'loss',  min_delta=0.0001, patience=30,
                  verbose=1, mode='auto'),
    ModelCheckpoint(filepath = save_path+"/weights.{epoch:02d}-{val_loss:.4f}-{val_accuracy:.4f}.hdf5",
                    monitor = 'val_loss', save_best_only=True ),
    ReduceLROnPlateau(monitor='val_loss', factor=0.9, patience=10, verbose=1, mode='min', min_delta=1e-4)]

model = build_model()
model.summary()
history = model.fit(train_X,train_Y,epochs=200,batch_size=64,validation_data=(test_X,test_Y),callbacks=callbacks_list)
pd.DataFrame(history.history).to_csv(save_path+"/history.csv")

# Save Architecture
model_json = model.to_json()
output = model.predict(test_X)
predicted_classes = output.argmax(axis=1)
answer_classes = test_Y.argmax(axis=1)
acc = accuracy_score(answer_classes, predicted_classes)
with open(save_path+"/model_acc_{:.4f}.json".format(acc), 'w') as json_file:
    json_file.write(model_json)

# Save Weight
model.save_weights(save_path +"/final_weight.h5")
model_json = model.to_json()
with open(save_path+"/model.json".format(acc), 'w') as json_file:
    json_file.write(model_json)