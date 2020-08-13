# -*- coding: utf-8 -*-

from ctypes import *
import math
import random
import os
import sys
import cv2
import numpy as np
import time
import json
import darknet
import fishClassificator
import VideoCapturer

class Yolo:
    def __init__(self, cnn, videoSource, cfgPath, weightPath, dataPath, mode=0, interval=0):
        #Mode will determine the output. With mode 1, the output will be 
        self._mode = mode
        if self._mode == 1:
            self._interval = interval
        elif self._mode != 0:
            raise ValueError("Invalid mode")

 
        self._cnn = cnn
        self._video = videoSource
        self._videoFps = self._video.getFps()
        self._numberFramesVideo = self._video.getNumberFrames()
        self._video.setWidth(1280)
        self._video.setHeight(720)

        self._netMain = None
        self._metaMain = None
        self._altNames = None

        self.loadConfig(cfgPath, weightPath, dataPath)

        self._fishDetections =[]

        if self._mode == 0:
            self.processVideoMode0()
            self._video.releaseCapture()
        else:
            self.processVideoMode1()
            self.storeVideoInfo()
            self._video.releaseCapture()


    
    def loadConfig(self, cfgPath, weightPath, dataPath):
        if not os.path.exists(cfgPath):
            raise ValueError("Invalid cfg path `" + os.path.abspath(cfgPath)+"`")
        if not os.path.exists(weightPath):
            raise ValueError("Invalid weight path `" + os.path.abspath(weightPath)+"`")
        if not os.path.exists(dataPath):
            raise ValueError("Invalid data file path `" + os.path.abspath(dataPath)+"`")
        if self._netMain is None:
            self._netMain = darknet.load_net_custom(cfgPath.encode(
                "ascii"), weightPath.encode("ascii"), 0, 1)  
        if self._metaMain is None:
            self._metaMain = darknet.load_meta(dataPath.encode("ascii"))
        if self._altNames is None:
            try:
                with open(dataPath) as metaFH:
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
                                self._altNames = [x.strip() for x in namesList]
                    except TypeError:
                        pass
            except Exception:
                pass

    def convertBack(self, x, y, w, h):
        #We use this lamba function to ensure that no negative result is returned which can lead to an error
        f=lambda a: (abs(a)+a)/2
        xmin = int(round(x - (w / 2)))
        xmax = int(round(x + (w / 2)))
        ymin = int(round(y - (h / 2)))
        ymax = int(round(y + (h / 2)))
        return int(f(xmin)), int(f(ymin)), int(f(xmax)), int(f(ymax))

    def drawBoxes(self, image, detections):
        for detection in detections:
            x, y, w, h = detection[2][0],\
                detection[2][1],\
                detection[2][2],\
                detection[2][3]
            xmin, ymin, xmax, ymax = self.convertBack(
                float(x), float(y), float(w), float(h))
            pt1 = (xmin, ymin)
            pt2 = (xmax, ymax)
            cv2.rectangle(image, pt1, pt2, (0, 255, 0), 1)
            """cv2.putText(image,
                        detection[0].decode() +
                        " [" + str(round(detection[1] * 100, 2)) + "]",
                        (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        [0, 255, 0], 2)"""
        return image

    def extractDetections(self, image, detections):
        results =[]
        for detection in detections:
            x, y, w, h = int(detection[2][0]),\
                int(detection[2][1]),\
                int(detection[2][2]),\
                int(detection[2][3])
            xmin, ymin, xmax, ymax = self.convertBack(
                float(x), float(y), float(w), float(h))
            #Cutting detection from the image
            cutImage = image[ymin:ymax, xmin:xmax]
            #Convert image from BGR to RGB
            cutImage = cv2.cvtColor(cutImage, cv2.COLOR_BGR2RGB)
            
            #Resizing to cnn format
            cutImage= cv2.resize(cutImage,(224,224))
            #numpy array has to be converted to float array in order to feed it to the cnn
            cutImage = cutImage.astype(float)

            info = cnn.predictImage(cutImage)
            if(info is not None):
                results.append(info)

        return results

    def drawBoxesAndInfo(self, image, detections):
        for detection in detections:
            x, y, w, h = int(detection[2][0]),\
                int(detection[2][1]),\
                int(detection[2][2]),\
                int(detection[2][3])
            xmin, ymin, xmax, ymax = self.convertBack(
                float(x), float(y), float(w), float(h))
            #Cutting detection from the image
            cutImage = image[ymin:ymax, xmin:xmax]
            #Convert image from BGR to RGB
            cutImage = cv2.cvtColor(cutImage, cv2.COLOR_BGR2RGB)        
            #Resizing to cnn format
            cutImage= cv2.resize(cutImage,(224,224))
            #numpy array has to be converted to float array in order to feed it to the cnn
            cutImage = cutImage.astype(float)
            info = cnn.predictImage(cutImage)
            pt1 = (xmin, ymin)
            pt2 = (xmax, ymax)
            cv2.rectangle(image, pt1, pt2, (0, 255, 0), 1)
            if(info is not None):
                cv2.putText(image,"{} - {}".format(info[1], info[2]), (pt1[0], pt1[1] - 5), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, [0, 255, 0], 2)
                cv2.putText(image, "Family: {}".format(info[3]), (pt1[0] + 5, pt1[1] + 15), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, [0, 255, 0], 1)   
                cv2.putText(image, "Deep range: {}-{}m".format(info[4][0], info[4][1]), (pt1[0] + 5, pt1[1] + 30), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, [0, 255, 0], 1)
            else:
                cv2.putText(image, "¿?", (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 
                0.5, [0, 255, 0], 2)
        return image


    def storeVideoInfo(self):
        information ={}
        information['cnnInterval'] = self._video.getFps() * self._interval
        information['fps'] = self._videoFps
        information['classifications'] = self._fishDetections
        with open('data.json', 'w') as fp:
            json.dump(information, fp)

    def processVideoMode0(self):
        darknet_image = darknet.make_image(darknet.network_width(self._netMain),
                                    darknet.network_height(self._netMain),3)
        out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), self._videoFps,
        (darknet.network_width(self._netMain), darknet.network_height(self._netMain)))

        frameCounter = 0

        while True:
            #print("{}/{}".format(frameCounter, self._numberFramesVideo))
            ret, frame = self._video.getNextFrame()
            if frameCounter == self._numberFramesVideo: break

            if frame is not None:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(frame_rgb,
                                        (darknet.network_width(self._netMain),
                                            darknet.network_height(self._netMain)),
                                        interpolation=cv2.INTER_LINEAR)

                darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())
                detections = darknet.detect_image(self._netMain, self._metaMain, darknet_image, thresh=0.20)
                image = self.drawBoxesAndInfo(frame_resized, detections)

            self.progressBar(self._numberFramesVideo, frameCounter, 50)
            #cv2.imshow('Demo', image)
            out.write(image)
            frameCounter+=1
            cv2.waitKey(1)
        
    def processVideoMode1(self):
        darknet_image = darknet.make_image(darknet.network_width(self._netMain),
                                    darknet.network_height(self._netMain),3)
        out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 10,
        (darknet.network_width(self._netMain), darknet.network_height(self._netMain)))


        frameCounter = 0
        count = 0
        while True:
            ret, frame = self._video.getNextFrame()
            if frameCounter == self._numberFramesVideo: break

            if frame is not None:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_resized = cv2.resize(frame_rgb,
                                        (darknet.network_width(self._netMain),
                                            darknet.network_height(self._netMain)),
                                        interpolation=cv2.INTER_LINEAR)

                darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())

                detections = darknet.detect_image(self._netMain, self._metaMain, darknet_image, thresh=0.20)

                if count == (self._videoFps*self._interval):
                    image = self.drawBoxes(frame_resized, detections)
                    preds = self.extractDetections(frame_resized, detections)
                    self._fishDetections.append(preds)
                    count = 0
                else:
                    count +=1
                    image = self.drawBoxes(frame_resized, detections)
                    #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.progressBar(self._numberFramesVideo, frameCounter, 50)
            #cv2.imshow('Demo', image)
            out.write(image)
            frameCounter+=1
            cv2.waitKey(1)

    def adaptFps(self):
        out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), self._videoFps,
        (darknet.network_width(self._netMain), darknet.network_height(self._netMain)))
        tempVideo = VideoCapturer.Video("temp-output.avi")
        delay = tempVideo.calculateDelay(tempVideo.getFps(), self._videoFps)
        frames = tempVideo.getNumberFrames()
        frameCounter = 0
        while True:
            ret, frame = tempVideo.getNextFrame()
            #print("{}/{}".format(frameCounter, frames))
            if frameCounter == self._numberFramesVideo: break
            if (frame is not None):
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                out.write(frame)
                cv2.imshow("DEMO", frame)
            frameCounter+=1
            #Average time of displaying a frame is 5ms, so me substract it from the calcultated delay
            cv2.waitKey(delay-5)
        out.release()
        tempVideo.releaseCapture()

    def progressBar(self, size, progress, barLength):
        progress = float(progress)
        block = int(round(barLength*(progress/size)))
        text = "\rProgress: [{}] {} %".format( "#"*block + "-"*(barLength-block), round((int(progress)/size)*100))
        sys.stdout.write(text)
        sys.stdout.flush()

if __name__ == "__main__":
    cnn = fishClassificator.Cnn()
    cnn.startCnn()
    cnn.setConfidence(85)

    vid = VideoCapturer.Video('test4.MP4')

    cfg = "./cfg/yolov3.cfg"
    weight = "./backup/LastWeights/yolov3_2000.weights"
    data = "./data/fish.data"
    detector = Yolo(cnn, vid, cfg, weight, data, mode=0, interval=0.5)