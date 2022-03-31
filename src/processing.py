from xml.dom import xmlbuilder
import librosa
import numpy as np
from scipy.io.wavfile import write
# Removed scipy, unnecessary import--librosa can write .wav files itself.


class audioProcessingClass:
    def __init__(self, audioData, samplingRate):
        # Minimum time between onset detections, in seconds
        self.minOnsetInterval = 0.5
        # If None, will use sampling rate of given wav. Otherwise, will use specified sampling rate as integer
        self.forceSamplingRate = None  

        self.audioData = audioData
        self.sr = samplingRate if self.ForceSamplingRate == None else int(self.forceSamplingRate)

    def isolateBackground(self, audioData):
        # taken from https://librosa.org/doc/latest/auto_examples/plot_vocal_separation.html?highlight=background
        # solely for cutting out vocals
        sliceFull, phase = librosa.magphase(librosa.stft(audioData))
        sliceFilter = librosa.decompose.nn_filter(sliceFull, aggregate=np.median, metric='cosine', width=int(librosa.time_to_frames(2, sr=self.sr)))
        sliceFilter = np.minimum(sliceFull, sliceFilter)

        margin_i, margin_v = 2, 10
        power = 2

        mask_i = librosa.util.softmask(sliceFilter, margin_i * (sliceFull - sliceFilter), power=power)

        sBackground = mask_i * sliceFull
        
        return librosa.istft(sBackground * phase)

    def overlayIntervalFilter(self, overlayData):
        overlayDataFiltered = []
        # Ensure that interval between detected onset matches variable set in minOnsetInterval in secs
        i = 0
        overlayDataFiltered.append(overlayData[0])
        while i < (len(overlayData) - 1):
            x = i + 1
            while i != x and x < len(overlayData):
                i = x if (overlayData[x] - overlayData[i]) >= float(self.minOnsetInterval) else i
                x = x + 1 if i !=x else x
                if i == x:
                    overlayDataFiltered.append(overlayData[x])

        return np.array(overlayDataFiltered) 



        




def processAudio(audio):

    # Load audio file and apply built-in librosa 'percussive' frequency EQ
    originalAudioData, samplingRate = librosa.core.load(audio)
    filteredArr = librosa.effects.percussive(y=audio)

    # init class
    apc = audioProcessingClass()

    filteredOverlay = overlayFilter(librosa.onset.onset_detect(y = filteredArr, sr=samplingRate, units='time').tolist())

    write(outputFile, samplingRate, audioData + librosa.clicks(times=overlayData,sr=samplingRate, length=len(audioData)))
 
    return filteredArr, filteredOverlay, samplingRate
    




