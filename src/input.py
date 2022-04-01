# Import libraries
import processing
import sys, getopt

# Main function for processing arguments provided in command
def parseInput():

    output_file = None
    input_file = None
    frame_length = None
    sigma_multiplier = None
    time_diff = None

    # Parse through provided arguments, excluding initial call to file (input.py)
    try:
        opts = getopt.getopt(sys.argv[1:], 'o:i:f:s:t:')
    except getopt.GetoptError:
        print("Usage: -i <input file> -o <output file> -f <frame length> (optional, default 512) -s <sigma_multiplier> (optional, default 2) -t <min time between each beat, in seconds> (optional, default .5)")
        sys.exit(1)

    # Setting values to corresponding variables provided keys
    for k,v in opts[0]:
        if k == "-i":
            input_file = v
        elif k == "-o":
            output_file = v
        elif k=="-f":
            frame_length = v
        elif k == "-s":
            sigma_multiplier = v
        elif k == "-t":
            time_diff = v

    # Automatically assign frame_length and sigma_multiplier values if none are given
    if frame_length == None:
        frame_length = 512
    if sigma_multiplier == None:
        sigma_multiplier = 2
    if time_diff == None:
        time_diff = 0.5

    return input_file, output_file, frame_length, sigma_multiplier, time_diff
 
if __name__=="__main__":
    input_file, output_file, frame_length, sigma_multiplier, time_diff = parseInput()

    try:
        onset.detect_onset(input_file, output_file, frame_length, sigma_multiplier, time_diff)
    except Exception as error:
        print("Error occured: " + repr(error))
        sys.exit(1)