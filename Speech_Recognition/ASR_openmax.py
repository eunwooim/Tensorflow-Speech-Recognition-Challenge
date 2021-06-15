import os
import keras
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score

from numpy.linalg import norm
def cos_sim(A,B):
    return np.dot(A, B)/(norm(A)*norm(B))

def distance(vector1, vector2):
    return -10*cos_sim(vector1,vector2)

def openmax_param(model,trainx,trainy):
    import pandas as pd
    import keras
    from tensorflow.keras import optimizers
    class_num = len(np.array(model.weights[-1])) # Number of Class
    if len(np.shape(trainx))!=4:
        trainx = np.expand_dims(trainx,axis=-1)
    if len(trainy[0])==1:
        from keras.utils import to_categorical
        trainy = to_categorical(trainy,class_num)
    #x_predict = model.predict(trainx)
    corr_ind = np.where(np.argmax(trainy,axis=-1)==np.argmax(x_predict,axis=-1))
    ver_X_train = trainx[corr_ind]
    ver_Y_train = trainy[corr_ind] # Step1 Data classified correctly
    new_model = keras.models.Sequential(model.layers[:-1])
    new_model.compile(optimizer='adam',loss='categorical_crossentropy',
                        metrics=['accuracy'])
    logit_vector = np.array(new_model.predict(ver_X_train))
    logit_matrix = [[]]*class_num
    for i in range(len(ver_X_train)): # Save Logit Vector by its class
        idx = np.argmax(ver_Y_train[i])
        logit_matrix[idx] = logit_matrix[idx]+[logit_vector[i]]
    mean_vector = []
    for i in range(len(logit_matrix)): # Compute Mean Vector
        mean_vector.append(np.array(logit_matrix[i]).mean(axis=0))
    distance_matrix=[[]]*class_num
    for idx in range(len(logit_matrix)):
        for logit in logit_matrix[idx]: # Save the distance
            distance_ = distance(logit,mean_vector[idx])
            distance_matrix[idx] = distance_matrix[idx]+[distance_]
    for i in range(len(distance_matrix)): # Sort
        distance_matrix[i] = np.array(distance_matrix[i])
        distance_matrix[i] = np.sort(distance_matrix[i])
    hyparam=[[]]*class_num;w=[[]]*class_num
    from scipy.stats import weibull_min
    for i in range(len(distance_matrix)): # Generate Weibull Distribution
        temp = weibull_min.fit(distance_matrix[i][-20:])
        hyparam[i] = hyparam[i]+list(temp)
    return hyparam, new_model, class_num, mean_vector

def openmax(xdata,returnvalue):
    from scipy.stats import weibull_min
    hyparam = returnvalue[0]; new_model = returnvalue[1]
    class_num = returnvalue[2]; mean_vector = returnvalue[3]
    pred = new_model.predict(xdata)
    new_logits=[]
    for idx in range(len(pred)):
        new_logit=[];unknown=0
        logit=pred[idx]
        for ind in range(class_num):
            distance_=distance(logit,mean_vector[ind])
            weight=weibull_min.cdf(distance_,hyparam[ind][0],
                                   hyparam[ind][1],hyparam[ind][2])
            new_logit.append(logit[ind]*(1-weight))
            unknown+=logit[ind]*weight
        new_logit.append(unknown)
        new_logits.append(new_logit)
    output = []
    for i in new_logits:
        output.append(np.argmax(i))
    return output

def load_model(jsonpath,weightpath):
    with open(jsonpath) as f:
        json = f.read()
    model = tf.keras.models.model_from_json(json)
    model.load_weights(weightpath)
    return model

# Input the json, weight path
json = 
weight = 
model = load_model(json,weight)

# Input .npy file path
X_data = np.load(X_10.npy path)
X_data = np.expand_dims(X_data,axis=-1)
uknX = np.load(X_30.npy path)
uknX = np.expand_dims(uknX,axis=-1)
totalX = np.concatenate((X_data,uknX),axis=0)
Y_data = np.load(Y_.npy path)
uknY = np.load(Y_30.npy path)
totalY = np.concatenate((Y_data,uknY),axis=0)
test_ix = pd.read_csv(test idx path,header=None)[0]
train_ix = list(set(range(len(Y_data)))-set(test_ix))
train_X = X_data[train_ix]
train_Y = Y_data[train_ix]

temp = openmax_param(model,train_X,train_Y)
res = openmax(totalX,temp)
print(confusion_matrix(totalY, res))
print('Accuracy:',accuracy_score(totalY,res))