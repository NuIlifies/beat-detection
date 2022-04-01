from processing import processAudio

try:
    a = processAudio("edit.wav", "output.wav")

    a.writeToFile()

    print("Successfully filtered and output to ./output.wav")
    
except Exception as error:
    print("Error occured: " + repr(error))
