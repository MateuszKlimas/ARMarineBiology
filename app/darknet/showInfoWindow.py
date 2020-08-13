from tkinter import *
import VideoCapturer
import PIL.Image, PIL.ImageTk
from operator import itemgetter
import time
import json
import cv2


class App:
    def __init__(self, windowName, video, js):
        self._pathInfoImages =['infoImages/acanthurus_sohal.jpg', 'infoImages/amphiprion_ocellaris.jpg', 'infoImages/coris_formosa.jpg',
                            'infoImages/halichoeres_adustus.jpg', 'infoImages/naso_elegans.jpg', 'infoImages/naso_vlamingii.jpg',
                            'infoImages/paracanthurus_hepatus.jpeg', 'infoImages/pseudanthias_squamipinnis.jpeg', 'infoImages/pterapogon_kauderni.jpg',
                            'infoImages/siganus_vulpinus.jpg', 'infoImages/sphaeramia_nematoptera.jpg', 'infoImages/zebrasoma_flavescens.jpg',
                            'infoImages/zebrasoma_veliferum.jpg']
        self._window = Tk()
        self._window.title(windowName)

        # ----VIDEO INFORMATION----
        self._video = video
        #Get all information and detections from it through the json file
        self._videoData = self.loadInfoParameters(js)
        #Interval of frames between each CNN classification
        self._classificationInterval = self._videoData['cnnInterval']
        #Delay calculated to display video in the appropiate velocity. 5 is substracted because it's the average time of processing
        self._delay = self._video.calculateDelay(int(self._video.getFps()), int(self._videoData['fps'])) - 5
        #print("Actual fps: {} Desired fps: {} Delay: {}".format(int(self._video.getFps()), int(self._videoData['fps']), self._delay))
        #All classifications of the video
        self._classifications = self._videoData['classifications']

        self._counter = 0
        #infoItems is used to display in the right way the info
        self._infoItems = 0
        self._images =[]

        #self._screenWidth = self._window.winfo_screenwidth()
        #self._screenHeight = self._window.winfo_screenheight()
        #self._window.geometry("{}x{}".format(self._screenWidth,self._screenHeight))
        
        self._leftContainer = Frame(self._window, borderwidth=1, relief="raised", width=self._video.getWidth(), height=self._video.getHeight())
        self._rightContainer = Frame(self._window, borderwidth=1, relief="raised", width=self._video.getWidth()/2, height=self._video.getHeight())
        self._rightContainer['bg'] = '#a0a0a0'
        self._leftContainer.pack(side="left", expand=True, fill="both")
        self._rightContainer.pack(side="right", expand=True, fill="both")

        self._rightContainer.grid_columnconfigure(0, weight=1)
        self._rightContainer.grid_columnconfigure(1, weight=1)
        self._rightContainer.grid_rowconfigure(0, weight=1)

        self._videoCanvas = Canvas(self._leftContainer, width=self._video.getWidth(), height=self._video.getHeight())
        self._videoCanvas.pack()
        
        self._canvas = Canvas(self._rightContainer, heigh=self._video.getHeight(), width=self._video.getWidth()/2)
        self._canvas.grid(row=0, column=0)
        self._scrollbar = Scrollbar(self._rightContainer, orient='vertical', command=self._canvas.yview)
        self._scrollbar.grid(row=0, column=1, sticky='ns')
        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        self._infoFrame = Frame(self._canvas)
        self._canvas.create_window(0,0, window=self._infoFrame, anchor=NW)

        self._infoFrame.update_idletasks()
        self._canvas.config(scrollregion=self._canvas.bbox("all"))
        
        self.nextFrame()

        self._window.mainloop()

    def nextFrame(self):
        ret, frame = self._video.getNextFrame()
        if ret:
            self.image = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self._videoCanvas.create_image(0, 0, anchor = NW, image=self.image)

            if (self._counter == self._classificationInterval):
                if not self._classifications:
                    self._counter=0
                else:
                    fishes = self._classifications.pop(0)
                    if not fishes:
                        self.removeInfo()
                        self._counter=0
                    else:
                        self.removeInfo()
                        #fishes = list(fishes for fishes,_ in itertools.groupby(fishes))
                        fishes = dict((x[0], x) for x in fishes).values()
                        fishes = sorted(fishes, key=itemgetter(0))
                        for fish in fishes:
                            self.addFishInfo(fish)
                        self._counter=0
            else:
                self._counter+=1
            self._leftContainer.after(self._delay, self.nextFrame)

        else:
            time.sleep(5)
            self._window.destroy()


    def addFishInfo(self, info):
        #Image frame is created to display image of the fish
        self.infoImage = Frame(self._infoFrame, background='white', width=self._video.getWidth()/6, height=100)
        self.photoCanvas = Canvas(self.infoImage, background='white', width=self._video.getWidth()/6 -1, height=100 - 1)
        self.photoCanvas.pack()
        self.img = PIL.Image.open(self._pathInfoImages[info[0]])
        self.photo = PIL.ImageTk.PhotoImage(self.img)
        #We need to keep a list with the images displayed, otherwise it will be overwritten
        self._images.append(self.photo)
        self.photoCanvas.create_image(0,0,anchor=NW,image=self._images[self._infoItems])
        self.infoImage.grid(row=self._infoItems,column=0, sticky=NW)

        #Text frame is created to display name of the fish
        self.infoText = Frame(self._infoFrame, borderwidth=1, relief='raised', background='#FFC300', width=self._video.getWidth()/3, height=100)
        self.infoText.grid(row=self._infoItems, column=1, sticky=NW)
        self.label = Label(self.infoText, text=info[1], background='#FFC300', font=('Helvetica', 16))
        self.label.place(x=self._video.getWidth()/6,y=30, anchor=CENTER)

        self.infoText1 = Frame(self._infoFrame, borderwidth=1, relief='raised', background='#FFC300', width=self._video.getWidth()/3, height=100)
        self.infoText1.grid(row=self._infoItems, column=2, sticky=NW)
        self.label1 = Label(self.infoText, text="Family: {}\nDepth location: {}-{} meters".format(info[3], info[4][0], info[4][1]), background='#FFC300', font=('Helvetica', 10))
        self.label1.place(x=self._video.getWidth()/6,y=65, anchor=CENTER)

        self._infoItems+=1       

        self._infoFrame.update_idletasks()
        self._canvas.config(scrollregion=self._canvas.bbox("all"))

    def removeInfo(self):
        for child in self._infoFrame.winfo_children():
            child.grid_forget()
            self._infoFrame.update_idletasks()
            self._canvas.config(scrollregion=self._canvas.bbox("all"))
        self._images.clear()
        self._infoItems = 0

    def loadInfoParameters(self, js):
        with open(js) as fp:
            data = json.load(fp)
        return data


    
vid = VideoCapturer.Video("output.avi")
app = App("Fish detector © Mateusz Klimas", vid, 'data.json')
