from xml.dom import xmlbuilder
import librosa
import numpy as np
from scipy.io.wavfile import write
# Removed scipy, unnecessary import--librosa can write .wav files itself.

minOnsetInterval = 1


def convertToArrays(audioFile):

    # Load audio file and apply built-in librosa 'percussive' frequency EQ
    originalAudioData, samplingRate = librosa.core.load(audioFile)
    filteredArr = librosa.effects.percussive(y=originalAudioData)

    filteredOverlay = overlayFilter(librosa.onset.onset_detect(y = filteredArr, sr=samplingRate, units='time').tolist())
 
    return filteredArr, filteredOverlay, samplingRate


def toWavOutput(outputFile, samplingRate, audioData, overlayData):
    write(outputFile, samplingRate, audioData + librosa.clicks(times=overlayData, sr=samplingRate, length=len(audioData)))


def overlayFilter(overlayData):
    overlayDataFiltered = []
    
    # Ensure that interval between detected onset matches variable set in minOnsetInterval in secs
    i = 0
    while i < (len(overlayData) - 1):
        x = i + 1
        while i != x and x < len(overlayData):
            i = x if (overlayData[x] - overlayData[i]) >= float(minOnsetInterval) else i
            if i != x:
                x += 1
            else:
                overlayDataFiltered.append(overlayData[x])

    return np.array(overlayDataFiltered) 




    
    # x = numpy.asarray([.06, .27, .44, .62, 1.2, 5.5, 9.3])
    # desired output: [.06, 1.2, 5.5, 9.3]
    # ind = numpy.indices([7])
    # numpy.where(x[ind - 1] - x[ind - 2] >= 1, x, 0)[ind] == 0
    # aa = numpy.where((x[ind] - x[ind - 1] >= 1) and (x[ind], x, 0)
    # if the one before me has a timestamp distance that is less than 1, then set to 0
    # numpy.where((overlayData[ind1] - overlayData[ind1 - 1] < 1) & (overlayData[ind1 - 1] - overlayData[ind1 - 2] >= 1), 0, overlayData)
    # output: [0, 0, 0, 0, 0, 5.5, 9.3]
    print(overlayDataFiltered)




