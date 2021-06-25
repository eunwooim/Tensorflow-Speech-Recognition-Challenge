destpath= 'C:/Users/junsu/Desktop/audio/' # saved file 

# import libraries
import os 
import numpy as np
import librosa


# feature extraction 
for ind in range(1, 11):
    speakers= set()
    speakers_list=[]

    word_list= os.listdir(destpath)
    for word in word_list:
        file_list= os.listdir(destpath+word)
        for file in file_list:
            speakers.add(file.split('_')[0])
            speakers_list.append(file.split('_')[0])

    tmp=[]
    for speaker in speakers:
        (a, b)= (speaker, speakers_list.count(speaker))
        tmp.append((a,b))

    train_speakers= set()
    enroll_speakers= set()
    eval_speakers= set()

    for i in tmp:
        if i[1]>=90:
            train_speakers.add(i[0])
            if len(train_speakers)==100: # 훈련을 위한 화자 데이터 
                break
    print(len(train_speakers))

    for j in tmp:
        if j[1]>=40 and j[0] not in train_speakers and j[0]!= '1b63157b':
            enroll_speakers.add(j[0]) 
            if len(enroll_speakers)==ind: # 등록할 화자 수
                break

    print(len(enroll_speakers))
    print(enroll_speakers)

    for k in  tmp:
        if k[1]>=30 and k[0] not in train_speakers.union(enroll_speakers):
            eval_speakers.add(k[0])
            if len(eval_speakers)==10:
                break
                
    enroll_X=[]
    enroll_Y=[]
    eval_X= []
    eval_Y= [] 
    enroll_speaker= list(enroll_speakers)

    word_list= os.listdir(destpath)

    for speaker in enroll_speakers:
        cnt=0
        for word in word_list:
            file_list= os.listdir(destpath+word)
            word_path= destpath+word
            for file in file_list:
                name= file.split('_')[0]
                if speaker==name:
                    sample, sr = librosa.load(word_path+'/'+file,sr=22050)
                    sample = librosa.util.fix_length(sample,22050)
                    mfcc = librosa.feature.mfcc(sample,n_fft=2048,hop_length=512,n_mfcc=40)
                    if not np.isnan(mfcc).any() and cnt<40:
                        enroll_X.append(mfcc)
                        enroll_Y.append(enroll_speaker.index(name))
                        cnt+=1


    for speaker in eval_speakers:
        cnt=0
        for word in word_list:
            word_path= destpath+word
            file_list= os.listdir(word_path)
            for file in file_list:
                name=file.split('_')[0]
                if speaker== name:
                    sample, sr = librosa.load(word_path+'/'+file,sr=22050)
                    sample = librosa.util.fix_length(sample,22050)
                    mfcc = librosa.feature.mfcc(sample,n_fft=2048,hop_length=512,n_mfcc=40)
                    if not np.isnan(mfcc).any() and cnt<10:
                        eval_X.append(mfcc)
                        eval_Y.append(len(np.unique(enroll_Y)))
                        cnt+=1
    # enroll 및 evaluation data 저장                    
    enroll_X= np.array(enroll_X)
    enroll_X= np.expand_dims(enroll_X, axis=-1)
    eval_X=np.array(eval_X)
    eval_X= np.expand_dims(eval_X, axis= -1)
    
    save_path='G:/내 드라이브/Speaker_verification/data/cv/enroll_'+str(ind)+'/'
    
    np.save(save_path+'enroll_X.npy', enroll_X)
    np.save(save_path+'enroll_Y.npy', enroll_Y)
    np.save(save_path+'eval_X.npy', eval_X)
    np.save(save_path+'eval_Y.npy', eval_Y)

# train data 저장
train_X=[]
train_Y=[]
train_speakers= list(train_speakers)
for speaker in train_speakers:
    for word in word_list:
        file_list= os.listdir(destpath+word)
        word_path= destpath+word
        for file in file_list:
            name= file.split('_')[0]
                          sample, sr = librosa.load(word_path+'/'+file,sr=22050)
                sample = librosa.util.fix_length(sample,22050)
                mfcc = librosa.feature.mfcc(sample,n_fft=2048,hop_length=512,n_mfcc=40)  if speaker==name:
                sample, sr = librosa.load(word_path+'/'+file,sr=22050)
                sample = librosa.util.fix_length(sample,22050)
                mfcc = librosa.feature.mfcc(sample,n_fft=2048,hop_length=512,n_mfcc=40)
                if not np.isnan(mfcc).any():
                    train_X.append(mfcc)
                    train_Y.append(train_speakers.index(speaker))

save_path= 'G:/내 드라이브/Speaker_verification/data/'
train_X= np.array(train_X)
train_X= np.expand_dims(train_X, axis=-1)
np.save(save_path+'train_X.npy', train_X)
np.save(save_path+'train_Y.npy', train_Y)