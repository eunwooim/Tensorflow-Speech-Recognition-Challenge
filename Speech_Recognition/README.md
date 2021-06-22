# Speech Recognition

## Goal
Goal of Tensorflow Speech Recognition Challenge is recognizing 10 speech commands (yes, no, up, down, left, right, on, off, stop, go). Everything else should be considered either unknown or silence. In order to achieve this, we need to classify a speech commands in 11 class. There are many ways to classify commands. For example, train a neural network which is trained to predict into 30 classes since there are 30 different words in the dataset. However, this method cannot properly recognize untrained words. To meet the original intent, we applied __'Open Set Recognition'__ to this work.

![temp](https://user-images.githubusercontent.com/68213812/122737143-b6a64780-d2bb-11eb-8f7b-3588acfb77e1.png)

## Convolutional Neural Networks
With preprocessed MFCC, we built CNN model for classification. The model has 3 convolutional layers, and 2 dense layers. Between convolutional layers, we added batch normalization. For purpose of lightweight, we used depthwise convolution.

![temp](https://user-images.githubusercontent.com/68213812/122908116-c04caf80-d38e-11eb-8305-1a77844896ac.png)

## Open Set Recognition

## Result
