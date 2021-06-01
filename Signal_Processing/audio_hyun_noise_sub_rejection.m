
clear all; close all; clc

%%
default_path = 'C:\Users\HIT\Desktop\audio'; % 분석할 데이터가 있는 폴더의 위치 설정
cd(default_path)

audio_Fs = 16000;     

words = {'bed','bird','cat','dog','down','eight','five','four','go','happy',...
    'house','left','marvin','nine','no','off','on','one','right','seven',...
    'sheila','six','stop','three','tree','two','up','wow','yes','zero'}; 

[~, txt_hash, ~] = xlsread('hash_key_trial.csv');
hash_list = txt_hash(:, 1);
empty_list = cellfun('isempty',hash_list);
hash_list(empty_list,:) = [];

clear empty*

    [b_notch_50, a_notch_50] = butter(3, [48 52]/(audio_Fs/2), 'stop');       % 50 Hz notch filter
    [b_notch_100, a_notch_100] = butter(3, [98 102]/(audio_Fs/2), 'stop');    % 100 Hz notch filter
    [b_notch_150, a_notch_150] = butter(3, [148 152]/(audio_Fs/2), 'stop');   % 150 Hz notch filter
    [b_notch_200, a_notch_200] = butter(3, [198 202]/(audio_Fs/2), 'stop');   % 200 Hz notch filter
    [b_notch_250, a_notch_250] = butter(3, [248 252]/(audio_Fs/2), 'stop');   % 250 Hz notch filter
    [b, a] = butter(3, [300 4000]/(audio_Fs/2), 'bandpass');  % 300~4000 Hz 구간만 사용

%%
for ww = 1 : length(words)
    word_path = [default_path, '\', words{ww}];
    for ii = 1:length(hash_list) % 각 인원마다 
        for tt = 0 : 11          % trial이 최대 11개까지 있다고 가정
            clearvars -except default_path audio_Fs words txt_hash hash_list b a word_path ww ii tt b_notch* a_notch*
            close all
            
            cd(word_path)
            word_sound = cellstr(ls([hash_list{ii}, '_*_', num2str(tt),'.wav' ]));
            if exist(word_sound{1}) == 0
               continue
            end     
     
                [temp_data temp_Fs] = audioread(word_sound{1});
                temp_audio = temp_data;
            
                temp_audio = filtfilt(b_notch_50, a_notch_50, temp_audio);
                temp_audio = filtfilt(b_notch_100, a_notch_100, temp_audio);
                temp_audio = filtfilt(b_notch_150, a_notch_150, temp_audio);
                temp_audio = filtfilt(b_notch_200, a_notch_200, temp_audio);
                temp_audio = filtfilt(b_notch_250, a_notch_250, temp_audio);
%                temp_audio = sgolayfilt(temp_audio , 3, 21);
                temp_audio = filtfilt(b, a, temp_audio);
                
                snr_th = 10;    % 데이터 확인 후 경험적으로 결정한 snr noise 판별 threshold
                temp_f_audio = fft(temp_audio);
                temp_power = abs(temp_f_audio);
                temp_power(2:end) = temp_power(2:end).^2;
                half_line = round(length(temp_power)/2)-1;
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
                if  n_nan < round(half_leng/4)   % reject가 75% 이상 일어난 것은 정상적인 음성이 아닌 것으로 분류 
                    continue
                end
                
                % save files
%                save_name = ['preprocessed_', words{ww},'_', hash_list{ii}, '_', num2str(tt), '.mat'];
                mfcc_name = ['preprocessed_', words{ww},'_', hash_list{ii}, '_', num2str(tt), '_mfcc.csv'];
                
                % save mat
%                cd([default_path, '\Preprocessed_mat\',words{ww}])
%                save(save_name, 'n_nan', 'temp_f_audio');
                
                % mfcc 생성
                cd([default_path, '\Preprocessed_mfcc\',words{ww}])
                temp_mfcc =  mfcc(temp_clear,audio_Fs,'NumCoeffs',39);
                temp_mfcc_padding = zeros(135, 40);
                temp_mfcc_padding(1:size(temp_mfcc,1),:) = temp_mfcc; %zero padding
                csvwrite(mfcc_name,temp_mfcc_padding)
              
            disp(ii)
        end
    end
end
