# Standard imports
import librosa as lr
import numpy as np
from soundfile import write

class processAudio:
    
    def __init__(self, inputFileName, outputFileNAme):
        # Minimum time between onset detections, in seconds
        self.minOnsetInterval = 0.3
        # If None, will use sampling rate of given wav. Otherwise, will use specified sampling rate as integer
        self.forceSamplingRate = None  
        # If True, will attempt to remove vocals from given audio
        self.applyBackgroundIsolation = False

        self.outputFileName = outputFileNAme
        self.audioData, tempsr = lr.core.load(inputFileName)
        self.sr = tempsr if self.forceSamplingRate == None else int(self.forceSamplingRate)

        self.initialOverlayData = lr.onset.onset_detect(
            y = self._isolateBackground() if self.applyBackgroundIsolation == True else self.audioData, 
            sr=self.sr, 
            units='time'
            )

        self.correctedOverlayData = self._strengthThreshold()

        
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

    def _strengthThreshold(self):
        # https://stackoverflow.com/users/3083138/stachyra
        slicedAudio = self.audioData[2240:]

        # Calculate RMS energy per frame.  I shortened the frame length from the
        # default value in order to avoid ending up with too much smoothing
        rmse = lr.feature.rms(y=slicedAudio, frame_length=512)[0,]
        envtm = lr.frames_to_time(np.arange(len(rmse)), sr=self.sr, hop_length=512)
        # Use final 3 seconds of recording in order to estimate median noise level
        # and typical variation
    

        noiseidx = [envtm > envtm[-1] - 5.0] 
        print(envtm[-1] - 5.0)
       # print(noiseidx)
        noisemedian = np.percentile(rmse[noiseidx], 50)
        sigma = np.percentile(rmse[noiseidx], 84.1) - noisemedian

        # Set the minimum RMS energy threshold that is needed in order to declare
        # an "onset" event to be equal to 5 sigma above the median
        threshold = noisemedian + 4*sigma
        threshidx = [rmse > threshold]
        # Choose the corrected onset times as only those which meet the RMS energy
        # minimum threshold requirement



        
        return self.initialOverlayData[[tm in envtm[threshidx] for tm in self.initialOverlayData]]
        """

    def _overlayIntervalFilter(self, detectedOnset):
        # Note: detectedOnset is librosa.onset.onset_detect output as a list, WITHOUT time interval filter.
        diff = np.insert(np.diff(detectedOnset),0,np.inf)
    
        for i in range(len(diff) - 1):
            if diff[i] < self.minOnsetInterval:
                diff[i + 1] += diff[i]
        
        detectedOnsetFiltered = detectedOnset[diff >= self.minOnsetInterval]
        return np.array(detectedOnsetFiltered) 

"""
    def writeToFile(self):
        write(
            self.outputFileName,
            self.audioData + 
            lr.clicks(
                times=self.correctedOverlayData,sr=self.sr,
                length=len(self.audioData)),
            self.sr
        )
 