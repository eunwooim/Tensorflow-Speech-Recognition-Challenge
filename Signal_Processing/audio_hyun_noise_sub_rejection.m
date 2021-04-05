
clear all; close all; clc

%%
default_path = 'C:\Users\Desktop\audio'; % �м��� �����Ͱ� �ִ� ������ ��ġ ����
cd(default_path)

audio_Fs = 16000;     

words = {'bed','bird','cat','dog','down','eight','five','four','go','happy',...
    'house','left','marvin','nine','no','off','on','one','right','seven',...
    'shella','six','stop','three','tree','two','up','wow','yes','zero'}; 

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
    [b, a] = butter(3, [300 4000]/(audio_Fs/2), 'bandpass');  % 300~4000 Hz ������ ���

%%
for ww = 1 : length(words)
    word_path = [default_path, '\', words{ww}];
    for ii = 1:length(hash_list) % �� �ο����� 
        for tt = 0 : 15          % trial�� �ִ� 15������ �ִٰ� ����
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
                zero_tracker = temp_data == 0; % �����Ͱ� ������ ���� ���� �м� ����
                temp_audio(:,zero_tracker==1) = NaN;
        
                NaN_tracker{ii} = isnan(temp_reject); % ������ noise�� �Ǻ��� ���� temp_audio�� ����
                temp_audio(NaN_tracker{ii}==1) = NaN;
        
                Epoch_length = 0.004; % 0.004�� ������ ��� overlap 0.002��
                snr_th = 100;    % ������ Ȯ�� �� ���������� ������ snr noise �Ǻ� threshold
 
                    iter = 1;
                    while(1)
                        starttime = round(iter * 0.002 * audio_Fs) ; % �ʹ� 0.002�ʴ� ������ ����ֱ� ������ ���� 
                        try
                            Epoch{iter,1} = temp_audio([1:Epoch_length*audio_Fs]+starttime,1);
                        catch; break; end
                        temp_nan = mean(isnan(Epoch{iter,1})) > 0; % �����츶�� NaN�� �ϳ��� ���ԵǸ� ����
                        Epoch{iter,1}(repmat(temp_nan, Epoch_length*audio_Fs, 1)) = NaN;
                        try 
                            if min(temp_nan)
                            else
                               [temp_power, F] = periodogram(Epoch{iter,1}, rectwin(Epoch_length*audio_Fs), Epoch_length*audio_Fs, audio_Fs);    
                               [~, temp_peak] = findpeaks(temp_power(3+1:audio_Fs*Epoch_length/2+1,1), 'Npeaks', 1, 'sortstr', 'descend'); % 3 ���� peak Ž�� (freq domain)
                               temp_snr = temp_power(temp_peak+3, 1) * (4-1) /... % peak power * (+-2 ���� point ���� -1) / (peak power�� ������ +-2 ���� power ���)
                                  (sum(temp_power((temp_peak-2:temp_peak+2)+3, 1))-temp_power(temp_peak+3, 1)); % +- 2 �̳� SNR ����
                               if temp_snr >= snr_th
                                    Epoch{iter,1}(:,:) = NaN; 
                               end    
                            end % �������� ����� �ǳʶ�
                        catch; continue; end
                        survive_epochs(iter,:) = mean(isnan(Epoch{iter,1})) == 0;  % ���������� ��Ƴ��� Epoch üũ��
                        iter = iter +1;
                    end
                    clearvars temp_nan 
            
                % ��Ƴ��� epoch ���� count
                Epoch(~survive_epochs,:)=[]; 
                n_Epochs = length(Epoch);
                num_nan = 498 - n_Epochs; 
                if  n_Epochs < 98   % reject�� 400 (80 percents)�̻� �Ͼ ���� �������� ������ �ƴ� ������ �з� 
                    continue
                end
                % save files
                cd([default_path, '\Preprocessed'])
                save_name = ['preprocessed_', words{ww},'_', hash_list{ii}, '_', num2str(tt), '.mat'];
                fig_name = ['preprocessed_', words{ww},'_', hash_list{ii}, '_', num2str(tt), '.png'];
                % spectrogram ����
                temp_spect = cell2mat(Epoch);
                spectrogram(temp_spect, rectwin(Epoch_length*audio_Fs), 0 , Epoch_length*audio_Fs,audio_Fs,'yaxis')
                saveas(gcf, fig_name)
                save(save_name, 'Epoch', 'n_Epochs', 'num_nan');
            disp(ii)
        end
    end
end













