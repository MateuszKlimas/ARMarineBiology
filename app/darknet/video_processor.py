import cv2
import time

def getFPS(video):
    return video.get(cv2.CAP_PROP_FPS)

def calculateDelay(actualFps, desiredFps):
    """
    Calculates the delays if the FPS are lowers than 30, to avoid the video going faster
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
 
if __name__ == '__main__' :
 
    # Start default camera
    video = cv2.VideoCapture('output.avi')
    fps = getFPS(video)
    print("FPS: {}".format(fps))
    delay = int(calculateDelay(fps, 50))
    print("Delay: {}".format(delay))
    ret = True
    frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Frames: {}".format(frames))

    while ret:
        s = time.time()
        ret, frame_read = video.read()
        if (frame_read is not None):
            cv2.imshow('Demos', frame_read)
            #Average time of displaying a frame is 5ms, so me substract it from the calcultated dela
            cv2.waitKey(delay-5)


    cv2.waitKey(3000)
    video.release()
    """
    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
     
    # With webcam get(CV_CAP_PROP_FPS) does not work.
    # Let's see for ourselves.
     d
    if int(major_ver)  < 3 :
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else :
        fps = video.get(cv2.CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
     
 
    # Number of frames to capture
    num_frames = 120;
     
     
    print("Capturing {0} frames".format(num_frames))
 
    # Start time
    start = time.time()
     
    # Grab a few frames
    for i in xrange(0, num_frames) :
        ret, frame = video.read()
 
     
    # End time
    end = time.time()
 
    # Time elapsed
    seconds = end - start
    print("Time taken : {0} seconds".format(seconds))
 
    # Calculate frames per second
    fps  = num_frames / seconds;
    print("Estimated frames per second : {0}".format(fps));
 
    # Release video
    video.release()
    """