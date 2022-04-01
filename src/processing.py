import librosa
import numpy as np
from scipy.io.wavfile import write
# Removed scipy, unnecessary import--librosa can write .wav files itself.


class processAudio:
    def __init__(self, inputFileName):
        # Minimum time between onset detections, in seconds
        self.minOnsetInterval = 0.5
        # If None, will use sampling rate of given wav. Otherwise, will use specified sampling rate as integer
        self.forceSamplingRate = None  
        # Isolate background track, good if
        self.removeVocals = True

        self.audioData, tempsr = librosa.core.load(inputFileName)
        self.sr = tempsr if self.ForceSamplingRate == None else int(self.forceSamplingRate)


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
  
        diff = np.insert(np.diff(overlayData),0,np.inf)
        for i in range(len(diff)):
            if diff[i] < self.minOnsetInterval:
                diff[i + 1] += diff[i]
            overlayDAtaFiltered = overlayData[diff >= self.minOnsetInterval]

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
    




