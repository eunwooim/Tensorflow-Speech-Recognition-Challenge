
clear all; close all; clc

%%
default_path = 'C:\Users\Desktop\audio'; % 분석할 데이터가 있는 폴더의 위치 설정
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
        for tt = 0 : 15          % trial이 최대 15개까지 있다고 가정
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
                temp_audio = filtfilt(b, a, temp_audio);
                
                temp_reject = temp_audio;
                zero_tracker = temp_data == 0; % 데이터가 들어오지 않은 구간 분석 제외
                temp_audio(:,zero_tracker==1) = NaN;
        
                NaN_tracker{ii} = isnan(temp_reject); % 나머지 noise로 판별된 구간 temp_audio에 적용
                temp_audio(NaN_tracker{ii}==1) = NaN;
        
                Epoch_length = 0.008; % 0.008초 윈도우 사용 128 points, overlap 0.004초
                snr_th = 100;    % 데이터 확인 후 경험적으로 결정한 snr noise 판별 threshold
 
                    iter = 1;
                    while(1)
                        starttime = round(iter * 0.004 * audio_Fs) ; % 초반 0.004초는 음성이 비어있기 때문에 제외 
                        try
                            Epoch{iter,1} = temp_audio([1:Epoch_length*audio_Fs]+starttime,1);
                        catch; break; end
                        temp_nan = mean(isnan(Epoch{iter,1})) > 0; % 윈도우마다 NaN이 하나라도 포함되면 제외
                        Epoch{iter,1}(repmat(temp_nan, Epoch_length*audio_Fs, 1)) = NaN;
                        
                            if min(temp_nan)
                            else
                               [temp_power, F] = periodogram(Epoch{iter,1}, rectwin(Epoch_length*audio_Fs), Epoch_length*audio_Fs, audio_Fs);    
                               [~, temp_peak] = findpeaks(temp_power(3+1:audio_Fs*Epoch_length/2-1,1), 'Npeaks', 1, 'sortstr', 'descend'); % 3 이후 peak 탐색 (freq domain)
                               temp_snr = temp_power(temp_peak+3, 1) * (4-1) /... % peak power * (+-2 내의 point 개수 -1) / (peak power를 제외한 +-2 내의 power 평균)
                                  (sum(temp_power((temp_peak-2:temp_peak+2)+3, 1))-temp_power(temp_peak+3, 1)); % +- 2 이내 SNR 구함
                               if temp_snr >= snr_th
                                    Epoch{iter,1}(:,:) = NaN; 
                               end    
                            end 
                            
                        survive_epochs(iter,:) = mean(isnan(Epoch{iter,1})) == 0;  % 최종적으로 살아남은 Epoch 체크함
                        iter = iter +1;
                      end
                    clearvars temp_nan 
            
                % 살아남은 epoch 개수 count
                Epoch(~survive_epochs,:)=[]; 
                n_Epochs = length(Epoch);
                num_nan = 248 - n_Epochs; 
                
                if n_Epochs == 248 % zero padding right
                else
                    for ss = n_Epochs +1 : 248
                        Epoch{ss} = zeros(128,1);
                    end
                end
                       
                if  n_Epochs < 90   % reject가 158 (60 percents)이상 일어난 것은 정상적인 음성이 아닌 것으로 분류 
                    continue
                end
                % save files
                save_name = ['preprocessed_', words{ww},'_', hash_list{ii}, '_', num2str(tt), '.mat'];
                spect_name = ['preprocessed_', words{ww},'_', hash_list{ii}, '_', num2str(tt), '_spect.csv'];
                mfcc_name = ['preprocessed_', words{ww},'_', hash_list{ii}, '_', num2str(tt), '_mfcc.csv'];
                
                % save mat
                cd([default_path, '\Preprocessed_mat\',words{ww}])
                save(save_name, 'Epoch', 'n_Epochs', 'num_nan');
                
                % spectrogram 생성 248*65 (Time*Frequence)
                cd([default_path, '\Preprocessed_spect\',words{ww}])
                temp_mat = cell2mat(Epoch);
                temp_spe = spectrogram(temp_mat, rectwin(Epoch_length*audio_Fs), 0 , Epoch_length*audio_Fs,audio_Fs);
                temp_spect = abs(temp_spe)';
                xlswrite(spect_name,temp_spect)
                             
                % mfcc 생성 196*14 (Time * index)
                cd([default_path, '\Preprocessed_mfcc\',words{ww}])
                temp_mfcc =  mfcc(temp_mat,audio_Fs);
                xlswrite(mfcc_name,temp_mfcc)
              
            disp(ii)
        end
    end
end
