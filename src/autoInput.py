from processing import processAudio

try:
    aD, oA, sr = processAudio('edit.wav')

    y = toWavOutput("output.wav", sr, aD, oA)

    print("Successfully filtered and output to ./output.wav")
    
except Exception as error:
    print("Error occured: " + repr(error))
