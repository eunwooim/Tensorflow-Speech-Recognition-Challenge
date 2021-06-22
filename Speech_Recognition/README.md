# Speech Recognition

## Goal
Goal of Tensorflow Speech Recognition Challenge is recognizing 10 speech commands (yes, no, up, down, left, right, on, off, stop, go). Everything else should be considered either unknown or silence. In order to achieve this, we need to classify a speech commands in 11 class. There are many ways to classify commands. For example, train a neural network which is trained to predict into 30 classes since there are 30 different words in the dataset. However, this method cannot properly recognize untrained words. To meet the original intent, we applied __'Open Set Recognition'__ to this work.

![temp](https://user-images.githubusercontent.com/68213812/122737143-b6a64780-d2bb-11eb-8f7b-3588acfb77e1.png)

## [Convolutional Neural Networks](https://github.com/imeunu/Tensorflow_SpeechRecognition_Challenge/blob/main/Speech_Recognition/ASR_build_model.py)
With [preprocessed MFCC](https://github.com/imeunu/Tensorflow_SpeechRecognition_Challenge/blob/main/Speech_Recognition/ASR_preprocess.py), we built CNN model for classification. The model has 3 convolutional layers, and 2 dense layers. Between convolutional layers, we added batch normalization. For purpose of lightweight, we used depthwise convolution.

![temp](https://user-images.githubusercontent.com/68213812/122908116-c04caf80-d38e-11eb-8305-1a77844896ac.png)

## [Open Set Recognition](https://github.com/imeunu/Tensorflow_SpeechRecognition_Challenge/blob/main/Speech_Recognition/ASR_build_model.py)
With our CNN model, we can only classify 10 words. In order to aim our goal, we should apply open set recognition to our classifier.
<br>
__OpenMax__ algorithm enabled us to apply open set recognition. The algorithm is described below.

#### [__Algorithm__](https://ieeexplore.ieee.org/document/7780542)
<br>
1. Select the data classified correctly among the training data.
2. Seperate the X data by class.
3. Compute Logit Vector for each class.
4. Compute Mean Vector of Logit Vector.
5. Compute distance between Logit Vectors and Mean Vector.
6. Select n(=20) data that has longest distance for each class (Designate as outlier).
7. Generate Weibull Distribution with outliers ([Extreme Value Theorem](https://en.wikipedia.org/wiki/Fisher%E2%80%93Tippett%E2%80%93Gnedenko_theorem)).
8. Weight with the probability of the given data is an outlier.
9. Apply Softmax.
<br>
#### __Notation__
- Logit Vector: Voice Template(a vector which is input of Softmax Layer)
- Mean Vector: Mean of Euclidean distance of Logit Vectors
<br>
This method requires a CNN model that has very high accuracy performance (nearly 100% with training data). In addition, we did a lot of experiments in various condition. The highest performance showed when Euclidean distance is replaced into cosine similarity, and select 20 data as outlier. 

## Result & Discussion
As aforementioned method, we constructed 'Lightweight Open Set Command Recognizer' with 77.48% accuracy.
![temp](https://user-images.githubusercontent.com/68213812/122919376-20495300-d39b-11eb-96c9-2cc2652fd463.png)
<br>
0 to 10 corresponds to yes, no, up, down, left, right, on, off, stop, go, 'unknown'
We performed Phonetic Analysis with our result. 
![temp](https://user-images.githubusercontent.com/68213812/122924846-2f330400-d3a1-11eb-9245-430e43d84010.png)
<br>
Attached figure describes the phonemes of the words, and they are colored same if they have phones with similar pronounciation.
Note the number of the color and mispredictions. You'll find it interesting.

To further develop, I can come up with several ideas.
1. Apply another open set recognition algorithm.
2. Set a threshold for the openmax algorithm.
3. Replace Mean Vector into a Vector that causes the sum of the inner production to be maximum.
4. Replace Logit Vector into another Voice Template.

In summary, I preprocessed the sound wave into MFCC, built a CNN model, and applied OpenMax algorithm and achieved accuracy of 77.48%. I also highlighted an interesting phonetic analysis.
