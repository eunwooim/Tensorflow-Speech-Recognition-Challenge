import os
import re
import librosa
import numpy as np

#Generate training, test set
def walk(folder):
    '''Walk through every files in a directory'''
    for dirpath, dirs, files in os.walk(folder):
        for filename in files:
            yield dirpath, filename

def iswav(ext):
    csvlist = ['.wav']
    if ext in csvlist:
        return True
    else:
        return False

def ismax(length, new):
    if length<new:
        return True
    else:
        return False
  
def count_ext(path, ext):
    count = 0
    for folder, filename in walk(path):
        if filename[-len(ext):] == ext:
            count += 1
    return count

destpath = 'E:/imeunu/ASMR/train/train/audio/'
save_path = 'E:/imeunu/ASMR/train/train/result/'
try:
    os.mkdir(save_path)
except:
    pass
keywords = ('yes', 'no', 'up', 'down', 'left', 'right', 'on', 'off', 'stop','go')

# Check maximum length among the data
max_ = 0;from tqdm import tqdm
with tqdm(total = count_ext(destpath,'wav')) as pbar:
    for folder, filename in walk(destpath):
        signal, sr = librosa.load(folder+'/'+filename, sr=22050)
        length = len(signal)
        if ismax(max_, length):
            max_ = length
            keyword = re.split('/',folder)[-1]
            filename_ = filename
        pbar.update(1)
print(max_)

# Zeropadding, MFCC
X_10 = [];Y_10 = [];X_30 = [];Y_30 = []
total = count_ext(destpath, '.wav')
with tqdm(total=total) as pbar:
    for folder, filename in walk(destpath):
        sample, sr = librosa.load(folder+'/'+filename,sr=22050)
        sample = librosa.util.fix_length(sample,max_)
        mfcc = librosa.feature.mfcc(sample,n_fft=2048,hop_length=512,n_mfcc=40)
        try:
            y = keywords.index(re.split('/',folder)[-1])
            X_10.append(mfcc)
            Y_10.append(y)
        except:
            y = 10
            X_30.append(mfcc)
            Y_30.append(y)
        pbar.update(1)
np.save(save_path+'X_30.npy',X_30)
np.save(save_path+'Y_30.npy',Y_30)
np.save(save_path+'X_10.npy',X_10)
np.save(save_path+'Y_10.npy',Y_10)