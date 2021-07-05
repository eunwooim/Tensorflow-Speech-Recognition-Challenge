### About Sound Wave
Sound is produced by the vibration of an object. This vibrations determine oscillation of air molecules which basically creates an alternation of air pressure. This high pressure alternated with low pressure causes a wave. And this wave can be represented using continuous Wave Form. Take a look at the following example.

![example](https://user-images.githubusercontent.com/68213812/113739382-b37ad100-973a-11eb-8520-7cabcae8fab6.png)

The wave form can be represented using an amplitude and a time. We define __period__(or wavelength) as a distance between consecutive corresponding points of the same phase on the wave, and __amplitude__ as a distance of a peak point from zero.
<br>
In this case, period is 25 seconds and amplitude is 1. __Frequency__ is the inverse of period, which is 1/4Hz in this case.
<br>

Frequency and amplitude have relationship with pitch and loudness. Note that pitch and loudness are not some physical quantities, but relative perceptions. The higher frequencies are perceived as higher pitch, and higher amplitudes are perceived as louder sound.
<br>

Since the sound wave is continuous, we should perform analog digital conversion. By __Sampling__, wave is sampled by specific time intervals and amplitude will be quantised by with limited number of bits. In the example, number of red stems in 1 second is __sampling rate__, and wave is converted into array of projected amplitudes(y values of blue dots). As a results of conversion, the wave form become discrete time signal. We need to apply discrete signal processing for analysis digital audio signals.


### [Fourier Transform, Spectrogram](https://github.com/imeunu/Capstone_PBL/blob/main/initiate/Visualize.ipynb)
If we add following two sine waves, we'll obtain some wave like this.

![ex](https://user-images.githubusercontent.com/68213812/113825060-7c003900-97bb-11eb-9ae9-bfb6069710fd.png)

The frequency and amplitude of the first wave is 4 and 1, and the second wave is 11,2.
<br>
By Fourier Transform, we can decompose signals into sum of sinusoidal waves with different frequencies. And also we can find out that which frequency of sinusiodal signal is more contributed to organize given signal. For the sake of figuring out contribution, there is needs to transform the domain form 'time' to 'frequency', known as FFT(fast fourier transform). Following picture is a power spectrum of added sine waves.

![ex](https://user-images.githubusercontent.com/68213812/113828672-a18f4180-97bf-11eb-8482-1ec4d230b611.png)

The spectrum gives us the magnitude(absolute value of output of FFT) as a function of frequency.
<br>
In this case, you can see that two sine waves are decomposed and represented as two peaks. 

There are several kind of applications of fourier transform technique, One of that is __Short Time Fourier Transform(STFT)__. It computes several FFT at different time intervals so that it can preserve time informations.
<br>

STFT computes several Fourier Transform at different intervals in given frame size.
<br>
The given frame size is called __Window__, which is some number of samples. By STFT, we obtain a __Spectrogram__ which represents how much frequencies contribute to make given signal at each moments. (For more details about STFT, visit the linked site in the reference.)

![ex](https://user-images.githubusercontent.com/68213812/113988351-5726c700-988a-11eb-9c30-d5feea970e67.png)

The spectrogram on the left side is presented as linear scale, and another one is presented as a log scale.
<br>
Therefore, from an audio data, we visualized features in both time and frequency domain by spectrogram.

## About MFCCs
MFCC is well prepared to imitate human hearing properties.


## [Signal Processing](https://github.com/imeunu/Capstone_PBL/tree/main/Signal_Processing)
Erase Power Frequency(60kHz) and background noise

## Reference
STFT: https://en.wikipedia.org/wiki/Short-time_Fourier_transform
