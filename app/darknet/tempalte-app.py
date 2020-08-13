from tkinter import *
import VideoCapturer
import PIL.Image, PIL.ImageTk
import time
import cv2


class App:
    def __init__(self, windowName, video):
        self._window = Tk()
        self._window.title(windowName)
        self._video = video
        self._delay = 1
        self._counter = 0

        #self._screenWidth = self._window.winfo_screenwidth()
        #self._screenHeight = self._window.winfo_screenheight()
        #self._window.geometry("{}x{}".format(self._screenWidth,self._screenHeight))
        
        self._leftContainer = Frame(self._window, borderwidth=1, relief="raised", width=self._video.getWidth(), height=self._video.getHeight())
        self._rightContainer = Frame(self._window, borderwidth=1, relief="raised", width=self._video.getWidth()/2, height=self._video.getHeight())
        self._rightContainer['bg'] = '#a0a0a0'
        self._leftContainer.pack(side="left", expand=True, fill="both")
        self._rightContainer.pack(side="right", expand=True, fill="both")

        self._videoCanvas = Canvas(self._leftContainer, width=self._video.getWidth(), height=self._video.getHeight())
        self._videoCanvas.pack()
        """
        self._infoCanvas = Canvas(self._rightContainer, width=self._video.getWidth()/2, height=self._video.getHeight())
        self._scrollbar = Scrollbar(self._rightContainer, command=self._infoCanvas.yview)
        self._infoCanvas.config(yscrollcommand=self._scrollbar.set)
        self._scrollbar.pack(side=RIGHT, fill=Y)
        self._infoCanvas.pack(expand=YES, fill=BOTH)"""

        self.nextFrame()

        self._window.mainloop()

    def nextFrame(self):
        ret, frame = self._video.getNextFrame()
        if ret:
            #We need to indicate self in image in order to refer to the actual frame
            self.image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self._videoCanvas.create_image(0, 0, anchor = NW, image=self.image)

            if self._counter == 60:
                time.sleep(5)
                self.addFishInfo()

            elif self._counter == 120:
                time.sleep(5)
                self.addFishInfo()

            elif self._counter == 180:
                self.removeInfo()
            self._counter+=1

            """if self._counter == 0:
                print("HERE")
                self.photo = PIL.ImageTk.PhotoImage(file='image.jpg')
                self._infoCanvas.create_image(0,0,anchor=NW,image=self.photo)
            if self._counter == 60:
                print("THERE")
                self.photo = PIL.ImageTk.PhotoImage(file='photo1.png')
                self._infoCanvas.create_image(0,0,anchor=NW,image=self.photo)
                self._counter+=1
            self._counter+=1"""
            self._leftContainer.after(self._delay, self.nextFrame)
        else:
            #Wait 5 seconds and close window
            time.sleep(5)
            self._window.destroy()

    def addFishInfo(self):
        info = Frame(self._rightContainer, borderwidth=1, relief='raised', background="bisque", width=self._video.getWidth()/2, height=100)
        info.grid(column=0, sticky=NW)
        #self._rightContainer.grid_columnconfigure(0, weight=0)
        #self._rightContainer.grid_columnconfigure(1, weight=0)


    def updateInfo(self):
        
        self.nextFrame()

    def removeInfo(self):
        for child in self._rightContainer.winfo_children():
            child.destroy()


    
"""
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

    def getFrame(self):
        
        ret, frame = self._cap.read()
        if ret:
            if (frame is not None):
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) )             
            else: 
                return (ret, None)
        else: return (ret, None)

    def releaseCapture(self):
        self._cap.release()
"""

vid = VideoCapturer.Video("output-test3.avi")
app = App("Fish detector © Mateusz Klimas",vid)
