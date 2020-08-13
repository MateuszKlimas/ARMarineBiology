import cv2

class Video:
    def __init__(self, videoFile):
        self._cap = cv2.VideoCapture(videoFile)
        #Check if file has been opened right
        if not self._cap.isOpened():
            raise ValueError("Couldn't open %s",videoFile)
        
        self._videoWidth = self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self._videoHeight = self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        #print("WIDTH: {} HEIGHT: {}".format(self._videoWidth, self._videoHeight))

    def getWidth(self):
        return self._videoWidth

    def getHeight(self):
        return self._videoHeight

    def getNextFrame(self):
        
        ret, frame = self._cap.read()
        if ret:
            if (frame is not None):
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) )             
            else: 
                return (ret, None)
        else: return (ret, None)

    def releaseCapture(self):
        self._cap.release()

    def setWidth(self, width):
        self._cap.set(3, width)

    def setHeight(self, height):
        self._cap.set(4, height)

    def getFps(self):
        return self._cap.get(cv2.CAP_PROP_FPS)

    def getNumberFrames(self):
        return int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def calculateDelay(self, actualFps, desiredFps):
        """
        Calculates the delays for a desired FPS, to slow a video in case it goes faster
        1 sec --> 1000ms
        1 sec --> 30fps      EACH FRAME 33ms aprox.

        EXAMPLE
        30 fps --> 1000/30 = 33ms each frame
        10 fps --> 1000/10 = 100ms         
        """
        frameTime = int(1000/desiredFps)
        if actualFps >= desiredFps:
            return 1
        else:
            return frameTime

