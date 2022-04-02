# Standard imports
import librosa as lr
import numpy as np
from soundfile import write

class processAudio:
    
    def __init__(self, inputFileName, outputFileNAme):
        # Minimum time between onset detections, in seconds
        self.minOnsetInterval = 0.5
        # If None, will use sampling rate of given wav. Otherwise, will use specified sampling rate as integer
        self.forceSamplingRate = None  
        # If True, will attempt to remove vocals from given audio
        self.applyBackgroundIsolation = True

        self.outputFileName = outputFileNAme
        self.audioData, tempsr = lr.core.load(inputFileName)
        self.sr = tempsr if self.forceSamplingRate == None else int(self.forceSamplingRate)

        self.filteredOverlayData = self._overlayIntervalFilter(lr.onset.onset_detect(
            y = self.audioData if self.applyBackgroundIsolation == False else self._isolateBackground(self.audioData), 
            sr=self.sr, 
            units='time'
            )).tolist()


    def _isolateBackground(self):
        # taken from https://librosa.org/doc/latest/auto_examples/plot_vocal_separation.html?highlight=background
        # solely for cutting out vocals
        sliceFull, phase = lr.magphase(lr.stft(self.audioData))
        sliceFilter = lr.decompose.nn_filter(sliceFull, aggregate=np.median, metric='cosine', width=int(lr.time_to_frames(2, sr=self.sr)))
        sliceFilter = np.minimum(sliceFull, sliceFilter)

        margin_i, margin_v = 2, 10
        power = 2
        mask_i = lr.util.softmask(sliceFilter, margin_i * (sliceFull - sliceFilter), power=power)
        sBackground = mask_i * sliceFull
        
        return lr.istft(sBackground * phase)
    

    def _overlayIntervalFilter(self, detectedOnset):
        # Note: detectedOnset is librosa.onset.onset_detect output as a list, WITHOUT time interval filter.
        diff = np.insert(np.diff(detectedOnset),0,np.inf)
    
        for i in range(len(diff) - 1):
            if diff[i] < self.minOnsetInterval:
                diff[i + 1] += diff[i]
        
        detectedOnsetFiltered = detectedOnset[diff >= self.minOnsetInterval]

        return np.array(detectedOnsetFiltered) 


    def writeToFile(self):
        write(
            self.outputFileName,
            self.audioData + 
            lr.clicks(
                times=self.filteredOverlayData,sr=self.sr,
                length=len(self.audioData)),
            self.sr
        )
 