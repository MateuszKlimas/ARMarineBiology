#Script used to start detections on a video file passes as an argument
import sys
import os

if __name__ == "__main__":
    #Args = [path, confidence, mode]
    if (len(sys.argv) < 4) or (len(sys.argv) > 4):
        print("ERROR: wrong number of arguments.")
        sys.exit(1)

    filename = sys.argv[1]
    confidence = sys.argv[2]
    mode = sys.argv[3]

    if not os.path.isfile(filename):
        print("ERROR: no such file.")
        sys.exit(1)
   