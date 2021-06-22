# Speech Recognition

## Goal
Goal of Tensorflow Speech Recognition Challenge is recognizing 10 speech commands (yes, no, up, down, left, right, on, off, stop, go). Everything else should be considered either unknown or silence. In order to achieve this, we need to classify a speech commands in 11 class. There are many ways to classify commands. For example, train a neural network which is trained to predict into 30 classes since there are 30 different words in the dataset. However, this method cannot properly recognize untrained words. To meet the original intent, we applied __'Open Set Recognition'__ to this work.

![temp](https://user-images.githubusercontent.com/68213812/122737143-b6a64780-d2bb-11eb-8f7b-3588acfb77e1.png)

## Convolutional Neural Networks
With preprocessed MFCC, we built CNN model for classification. The model has 3 convolutional layers, and 2 dense layers. Between convolutional layers, we added batch normalization. For purpose of lightweight, we used depthwise convolution.

![temp](https://user-images.githubusercontent.com/68213812/122908116-c04caf80-d38e-11eb-8305-1a77844896ac.png)

## Open Set Recognition
With our CNN model, we can only classify 10 words. In order to aim our goal, we should apply open set recognition to our classifier.
<br>
__OpenMax__ algorithm enabled us to apply open set recognition. The algorithm is described below.
Algorithm
<br>
1. Select the data classified correctly among the training data.
2. Seperate the X data by class.
3. Compute Logit Vector for each class.
4. Compute Mean Vector of Logit Vector.
5. Compute distance between Logit Vectors and Mean Vector.
6. Select n(=20) data that has longest distance for each class.
7. Generate Weibull Distribution with outliers.
8. Weight with the probability of the given data is an outlier.
9. Apply Softmax.


## Result
