# Algorithm and Development of Speech-based Speaker Recognition Model

### About Us
We are senior students of Hanyang University, Department of Mathematics. We formed our team in Math Capstone PBL Course. We are trying to implement a Speaker and Speech Recognition model using Deep Learning. We will keep writing what we have studied and implemented code here during this semester.

### Research Purpose


### About Sound Wave
Sound is produced by the vibration of an object. This vibrations determine oscillation of air molecules which basically creates an alternation of air pressure. This high pressure alternated with low pressure causes a wave. And this wave can be represented using continuous Wave Form. Take a look at the following example.

![example](https://user-images.githubusercontent.com/68213812/113739382-b37ad100-973a-11eb-8520-7cabcae8fab6.png)

The wave form can be represented using an amplitude and a time. We define __period__(or wavelength) as a distance between consecutive corresponding points of the same phase on the wave, and __amplitude__ as a distance of a peak point from zero.
<br>
In this case, period is 25 seconds and amplitude is 1. __Frequency__ is the inverse of period, which is 1/4Hz in this case.
<br>
Frequency and amplitude have relationship with pitch and loudness. Note that pitch and loudness are not some physical quantities, but relative perceptions. The higher frequencies are perceived as higher pitch, and higher amplitudes are perceived as louder sound.
<br>
Since the sound wave is continuous, we should perform analog digital conversion. By __Sampling__, wave is sampled by specific time intervals and amplitude will be quantised by with limited number of bits. In the example, number of red stems in 1 second is __sampling rate__, and wave is converted into array of projected amplitudes(y values of blue dots).


### [FFT,Spectrogram](https://github.com/imeunu/Capstone_PBL/blob/main/initiate/Visualize.ipynb)
If we add following two sine waves, we'll obtain some wave like this.

![ex](https://user-images.githubusercontent.com/68213812/113825060-7c003900-97bb-11eb-9ae9-bfb6069710fd.png)

The frequency and amplitude of the first wave is 4 and 1, and the second wave is 11,2.
<br>
By Fourier Transform, we can decompose this periodic sound into sum of sine waves oscilliating at different frequencies. Following picture is a power spectrum of added sine wave.
