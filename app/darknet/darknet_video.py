from ctypes import *
import math
import random
import os
import cv2
import numpy as np
import time
import json
import darknet
import fishClassificator
import VideoCapturer
 

def convertBack(x, y, w, h):
    #We use this function to ensure that no negative result is returned which can lead to an error
    f=lambda a: (abs(a)+a)/2
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return int(f(xmin)), int(f(ymin)), int(f(xmax)), int(f(ymax))

def extractDetections(detections, img, cnn):
    results =[]
    print("\n\n")
    for detection in detections:
        x, y, w, h = int(detection[2][0]),\
            int(detection[2][1]),\
            int(detection[2][2]),\
            int(detection[2][3])
        xmin, ymin, xmax, ymax = convertBack(
            float(x), float(y), float(w), float(h))
        #Cutting detection from the image
        cutImage = img[ymin:ymax, xmin:xmax]
        #Convert image from BGR to RGB
        print("x:{} y:{} w:{} h:{}".format(x,y,w,h))
        print("ymin:{} ymax:{} xmin:{} xmax:{}".format(ymin,ymax,xmin,xmax))
        print(np.shape(cutImage))
        cutImage = cv2.cvtColor(cutImage, cv2.COLOR_BGR2RGB)
        
        #Resizing to cnn format
        cutImage= cv2.resize(cutImage,(224,224))
        #numpy array has to be converted to float array in order to feed it to the cnn
        cutImage = cutImage.astype(float)

        idImage, name = cnn.predictImage(cutImage)
        if(idImage is not None):
            results.append([idImage, name])

        #cv2.imwrite('captures/img{}.png'.format(x), cutImage)
    return results


def cvDrawBoxes(detections, img):
    for detection in detections:
        x, y, w, h = detection[2][0],\
            detection[2][1],\
            detection[2][2],\
            detection[2][3]
        xmin, ymin, xmax, ymax = convertBack(
            float(x), float(y), float(w), float(h))
        pt1 = (xmin, ymin)
        pt2 = (xmax, ymax)
        cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
        cv2.putText(img,
                    detection[0].decode() +
                    " [" + str(round(detection[1] * 100, 2)) + "]",
                    (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    [0, 255, 0], 2)
    return img




netMain = None
metaMain = None
altNames = None


def YOLO(video, interval, cnn):

    global metaMain, netMain, altNames
    configPath = "./cfg/yolov3.cfg"
    weightPath = "./backup/LastWeights/yolov3_2000.weights"
    metaPath = "./data/fish.data"
    if not os.path.exists(configPath):
        raise ValueError("Invalid config path `" +
                         os.path.abspath(configPath)+"`")
    if not os.path.exists(weightPath):
        raise ValueError("Invalid weight path `" +
                         os.path.abspath(weightPath)+"`")
    if not os.path.exists(metaPath):
        raise ValueError("Invalid data file path `" +
                         os.path.abspath(metaPath)+"`")
    if netMain is None:
        netMain = darknet.load_net_custom(configPath.encode(
            "ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
    if metaMain is None:
        metaMain = darknet.load_meta(metaPath.encode("ascii"))
    if altNames is None:
        try:
            with open(metaPath) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents,
                                  re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            namesList = namesFH.read().strip().split("\n")
                            altNames = [x.strip() for x in namesList]
                except TypeError:
                    pass
        except Exception:
            pass
    
    frames = video.getNumberFrames()
    print("Frames: {}".format(frames))
    fps = video.getFps()
    print("FPS: {}".format(fps))

    #All information is stored to use it for later display
    information = {}
    #cnnInterval is the interval of frames between each classification, expressing the interval in seconds, which is multiplied by the fps
    information['cnnInterval'] = interval*fps
    information['fps'] = fps
    #information['width'] = darknet.network_width(netMain)
    #classificationinformation['height'] = darknet.network_height(netMain)



    video.setWidth(1280)
    video.setHeight(720)
    #cap.set(3, 1280)
    #cap.set(4, 720)
    out = cv2.VideoWriter(
        "output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 10.0,
        (darknet.network_width(netMain), darknet.network_height(netMain)))
    print("Starting the YOLO loop...")

    # Create an image we reuse for each detect
    darknet_image = darknet.make_image(darknet.network_width(netMain),
                                    darknet.network_height(netMain),3)

    #Storing all detections for each interval in fishDetections
    fishDetections =[]
    extractions = 0
    count = 1
    sec = 0
    frameCounter=0
    while True:
        #prev_time = time.time()
        ret, frame_read = video.getNextFrame()
        
        #if np.shape(frame_read) == (): break
        print("Frames: {} FrameCounter:{}".format(frames, frameCounter))
        if frameCounter == frames: break

        if (frame_read is not None):
            frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb,
                                    (darknet.network_width(netMain),
                                        darknet.network_height(netMain)),
                                    interpolation=cv2.INTER_LINEAR)

            darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())

            detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.20)

            if count == fps:
                image = cvDrawBoxes(detections, frame_resized)
                preds = extractDetections(detections,frame_resized, cnn)
                fishDetections.append(preds)
                extractions+=1
                #time.sleep(5)
                count = 0
            else:
                count +=1
                print(detections)
                image = cvDrawBoxes(detections, frame_resized)
                #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        cv2.imshow('Demo', image)
        out.write(image)
        frameCounter+=1
        cv2.waitKey(1)

    print("Extractions: {}".format(extractions))
    information['classifications'] = fishDetections
    with open('data.json', 'w') as fp:
        json.dump(information, fp)
    video.releaseCapture()
    out.release()

if __name__ == "__main__":
    cnn = fishClassificator.Cnn()
    cnn.startCnn()
    cnn.set_confidence(85)

    vid = VideoCapturer.Video('test5.MP4')
    YOLO(vid, 1, cnn)
