
clear all; close all; clc

%%
default_path = 'C:\Users\HIT\Desktop\timit'; % 분석할 데이터가 있는 폴더의 위치 설정
train_path = 'C:\Users\HIT\Desktop\timit\data\TRAIN\TEMP';
test_path = 'C:\Users\HIT\Desktop\timit\data\TEST\TEMP';
cd(default_path)
   
[~, txt_train, ~] = xlsread('train_data.csv');
train_hash_list = txt_train(2:end, 4);
train_sen_list = txt_train(2:end, 5);
empty_list = cellfun('isempty',train_hash_list);
train_hash_list(empty_list,:) = [];
clear empty*
empty_list = cellfun('isempty',train_sen_list);
train_sen_list(empty_list,:) = [];
clear empty*
train_hash_list = unique(train_hash_list);
train_hash_list{1} = 'MARC0';
temp_list = contains(train_sen_list,'.wav');
train_sen_list = train_sen_list(temp_list);
train_sen_list = unique(train_sen_list);
clear temp_list

[~, txt_test, ~] = xlsread('test_data.csv');
test_hash_list = txt_test(2:end, 4);
test_sen_list = txt_test(2:end, 5);
empty_list = cellfun('isempty',test_hash_list);
test_hash_list(empty_list,:) = [];
clear empty*
empty_list = cellfun('isempty',test_sen_list);
test_sen_list(empty_list,:) = [];
clear empty*
test_hash_list = unique(test_hash_list);
temp_list = contains(test_sen_list,'.wav');
test_sen_list = test_sen_list(temp_list);
test_sen_list = unique(test_sen_list);
clear temp_list

%%
%TRAIN
for ww = 1 : length(train_hash_list)
    word_path = [train_path, '\', train_hash_list{ww}];
    for ii = 1:length(train_sen_list) % 각 문장마다 
            clearvars -except default_path train_path test_path train_hash_list train_sen_list test_hash_list test_sen_list word_path ww ii
            close all
            
            cd(word_path)
            if exist(train_sen_list{ii}) == 0
               continue
            end     
     
                [temp_data temp_Fs] = audioread(train_sen_list{ii});
                temp_audio = temp_data;
                
                [b_notch_50, a_notch_50] = butter(3, [48 52]/(temp_Fs/2), 'stop');       % 50 Hz notch filter
                [b_notch_100, a_notch_100] = butter(3, [98 102]/(temp_Fs/2), 'stop');    % 100 Hz notch filter
                [b, a] = butter(3, [300 4000]/(temp_Fs/2), 'bandpass');  % 300~4000 Hz 구간만 사용

                temp_audio = filtfilt(b_notch_50, a_notch_50, temp_audio);
                temp_audio = filtfilt(b_notch_100, a_notch_100, temp_audio);

%                temp_audio = sgolayfilt(temp_audio , 3, 21);
                temp_audio = filtfilt(b, a, temp_audio);
                
                snr_th = 10;    % 데이터 확인 후 경험적으로 결정한 snr noise 판별 threshold
                temp_f_audio = fft(temp_audio);
                temp_power = abs(temp_f_audio);
                temp_power(2:end) = temp_power(2:end).^2;
                half_line = floor(length(temp_power)/2)-1;
                for pp = 3 : half_line
                    temp_snr = temp_power(pp) * (5-1) /... % peak power * (+-2 내의 point 개수 -1) / (peak power를 제외한 +-2 내의 power 평균)
                    (sum(temp_power(pp-2:pp+2))-temp_power(pp)); % +- 2 이내 SNR 구함
                    if temp_snr >= snr_th
                        temp_f_audio(pp) = 0;
                        temp_f_audio(length(temp_f_audio)-pp+2) = 0;
                        pp = pp + 2;
                        if pp >= half_line
                            break
                        end
                    end
                end
                
                temp_clear = ifft(temp_f_audio);
                half_leng = half_line + 2;
                n_nan = length(find(temp_f_audio(1:half_leng)));
                if  n_nan < floor(half_leng/4)   % reject가 75% 이상 일어난 것은 정상적인 음성이 아닌 것으로 분류 
                    continue
                end
                
                temp_sen = strrep(train_sen_list{ii}, '.WAV.wav','_');
                temp_rep = floor(length(temp_clear)/temp_Fs)*2 -2;
                for bb = 0 : temp_rep
                    % save files
    %                save_name = ['preprocessed_', words{ww},'_', hash_list{ii}, '_', num2str(tt), '.mat'];
                    mfcc_name = ['preprocessed_', train_hash_list{ww}, '_', temp_sen, num2str(bb),'_mfcc.csv'];
                    % save mat
    %                cd([default_path, '\Preprocessed_mat\',words{ww}])
    %                save(save_name, 'n_nan', 'temp_f_audio');

                    % mfcc 생성
                    cd('C:\Users\HIT\Desktop\TIMIT_preprocessed\TRAIN')
                    st_time = 1 + bb*temp_Fs/2;
                    ter_time = temp_Fs + bb*temp_Fs/2;
                    temp_mfcc =  mfcc(temp_clear(st_time:ter_time),temp_Fs,'NumCoeffs',39);
%                     temp_mfcc_padding = zeros(135, 40);
%                     temp_mfcc_padding(1:size(temp_mfcc,1),:) = temp_mfcc; %zero padding
                    csvwrite(mfcc_name,temp_mfcc)
                end
              
            disp(ii)
    end
end

%%
%TEST
for ww = 1 : length(test_hash_list)
    word_path = [test_path, '\', test_hash_list{ww}];
    for ii = 1:length(test_sen_list) % 각 문장마다 
            clearvars -except default_path train_path test_path train_hash_list train_sen_list test_hash_list test_sen_list word_path ww ii
            close all
            
            cd(word_path)
            if exist(test_sen_list{ii}) == 0
               continue
            end     
     
                [temp_data temp_Fs] = audioread(test_sen_list{ii});
                temp_audio = temp_data;
                
                [b_notch_50, a_notch_50] = butter(3, [48 52]/(temp_Fs/2), 'stop');       % 50 Hz notch filter
                [b_notch_100, a_notch_100] = butter(3, [98 102]/(temp_Fs/2), 'stop');    % 100 Hz notch filter
                [b, a] = butter(3, [300 4000]/(temp_Fs/2), 'bandpass');  % 300~4000 Hz 구간만 사용

                temp_audio = filtfilt(b_notch_50, a_notch_50, temp_audio);
                temp_audio = filtfilt(b_notch_100, a_notch_100, temp_audio);

%                temp_audio = sgolayfilt(temp_audio , 3, 21);
                temp_audio = filtfilt(b, a, temp_audio);
                
                snr_th = 10;    % 데이터 확인 후 경험적으로 결정한 snr noise 판별 threshold
                temp_f_audio = fft(temp_audio);
                temp_power = abs(temp_f_audio);
                temp_power(2:end) = temp_power(2:end).^2;
                half_line = floor(length(temp_power)/2)-1;
                for pp = 3 : half_line
                    temp_snr = temp_power(pp) * (5-1) /... % peak power * (+-2 내의 point 개수 -1) / (peak power를 제외한 +-2 내의 power 평균)
                    (sum(temp_power(pp-2:pp+2))-temp_power(pp)); % +- 2 이내 SNR 구함
                    if temp_snr >= snr_th
                        temp_f_audio(pp) = 0;
                        temp_f_audio(length(temp_f_audio)-pp+2) = 0;
                        pp = pp + 2;
                        if pp >= half_line
                            break
                        end
                    end
                end
                
                temp_clear = ifft(temp_f_audio);
                half_leng = half_line + 2;
                n_nan = length(find(temp_f_audio(1:half_leng)));
                if  n_nan < floor(half_leng/4)   % reject가 75% 이상 일어난 것은 정상적인 음성이 아닌 것으로 분류 
                    continue
                end
                
                temp_sen = strrep(test_sen_list{ii}, '.WAV.wav','_');
                temp_rep = floor(length(temp_clear)/temp_Fs)*2 -2;
                for bb = 0 : temp_rep
                    % save files
    %                save_name = ['preprocessed_', words{ww},'_', hash_list{ii}, '_', num2str(tt), '.mat'];
                    mfcc_name = ['preprocessed_', test_hash_list{ww}, '_', temp_sen, num2str(bb),'_mfcc.csv'];
                    % save mat
    %                cd([default_path, '\Preprocessed_mat\',words{ww}])
    %                save(save_name, 'n_nan', 'temp_f_audio');

                    % mfcc 생성
                    cd('C:\Users\HIT\Desktop\TIMIT_preprocessed\TEST')
                    st_time = 1 + bb*temp_Fs/2;
                    ter_time = temp_Fs + bb*temp_Fs/2;
                    temp_mfcc =  mfcc(temp_clear(st_time:ter_time),temp_Fs,'NumCoeffs',39);
%                     temp_mfcc_padding = zeros(135, 40);
%                     temp_mfcc_padding(1:size(temp_mfcc,1),:) = temp_mfcc; %zero padding
                    csvwrite(mfcc_name,temp_mfcc)
                end
              
            disp(ii)
    end
end











