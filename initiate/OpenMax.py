import numpy as np
def distance(vector1,vector2):
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    vector1 = vector1 - vector2
    vector1 = vector1**2
    return vector1.sum()

    '''Convert Close Set Classification into Open Set Classification
    Parameters
    ----------
    model: Pretrained close set classification model which will used for open set recognition.
            The higher the accuracy, the higher the performance.
            Model should have seperate Softmax layer.
    trainx: Data that was used for the training of the pretrained model.
    trainy: Label of the trainx which is used for the training.
    xdata: Data which includes 'unknown' class.
    ydata: Label of the data which includes 'unknown' class.

    Return
    ------
    hyparam: Hyper parameters of Weibull Distribution.
    new_model: Model without Softmax Layer.

    Algorithm
    ---------
    1. Select the data classified correctly among the training data.
    2. Seperate the X data by class.
    3. Compute Logit Vector for each class.
    4. Compute Mean Vector of Logit Vector.
    5. Compute distance between Logit Vectors and Mean Vector.
    6. Select n(=20) data that has longest distance for each class.
    7. Generate Weibull Distribution with outliers.
    8. Weight with the probability of the given data is an outlier.
    9. Apply Softmax.
    '''
    
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

def openmax(xdata,ydata,returnvalue):
    from scipy.stats import weibull_min
    hyparam = returnvalue[0]; new_model = returnvalue[1]
    class_num = returnvalue[2]; mean_vector = returnvalue[3]
    pred = new_model.predict(xdata)
    new_logits=[]
    for idx in range(len(pred)):
        new_logit=[];unknown=0
        for ind in range(class_num):
            logit=pred[idx]
            distance_=distance(logit,mean_vector[ind])
            weight=weibull_min.cdf(distance_,hyparam[ind][0],
                                   hyparam[ind][1],hyparam[ind][2])
            new_logit.append(logit[ind]*(1-weight))
            unknown+=pred[idx][ind]*weight
        new_logit.append(unknown)
        new_logits.append(new_logit)
    output = []
    for i in new_logits:
        output.append(np.argmax(i))
    return output
