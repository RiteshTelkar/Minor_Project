import time
import tensorflow
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
from tkinter import *

try:
    import Tkinter as tk
except:
    import tkinter as tk
import PIL
from PIL import ImageTk


class Tk_Manage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, StoV):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Two Way Sign Langage Translator", font=("Verdana", 12))
        label.pack(pady=10, padx=10)
        button = tk.Button(self, text=" sign to text",command=lambda: controller.show_frame(StoV))
        button.pack()
        button2 = tk.Button(self, text=" text to sign ")
        button2.pack()
        button3 = tk.Button(self, text="Voice to text", command=lambda: controller.show_frame(StartPage))
        button3.pack()
        button4 = tk.Button(self, text="text to voice", command=lambda: controller.show_frame(StartPage))
        button4.pack()
        load = PIL.Image.open("projectimg.jpg")
        load = load.resize((620, 450))
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=400, y=200)


class StoV(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Sign to text", font=("Verdana", 12))
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = tk.Button(self, text="text to Sign")
        button2.pack()
        disp_txt = tk.Text(self, height=4, width=25)

        def start_video():
                cap = cv2.VideoCapture(0)
                detector = HandDetector(maxHands=1)
                classifier = Classifier("Model/keras_model.h5","Model/labels.txt")
                offset = 20
                imgSize = 300

                folder = "Data/C"
                counter = 0

                labels = ["A","B","C"]
                while True:
                    success, img = cap.read()
                    imgOutput = img.copy()
                    hands, img = detector.findHands(img)
                    if hands:
                        hand = hands[0]
                        x,y,w,h = hand['bbox']

                        imgWhite = np.ones((imgSize,imgSize,3),np.int8)*255
                        imgcrop = img[y-offset:y + h+offset, x-offset:x + w+offset]
                        imgCropShape = imgcrop.shape


                        aspectRatio = h/w

                        if aspectRatio>1:
                            k = imgSize/h
                            wCal = math.ceil(k*w)
                            if imgcrop.size>0:
                                imgResize = cv2.resize(imgcrop, (wCal, imgSize))
                            else:
                                continue
                            imgResizeShape = imgResize.shape
                            wGap = math.ceil((imgSize-wCal)/2)
                            imgWhite[:, wGap:wCal + wGap] = imgResize
                            prediction, index =  classifier.getPrediction(imgWhite)
                            print(prediction,index)


                        else:
                            k = imgSize/w
                            hCal = math.ceil(k*h)
                            if imgcrop.size>0:
                                imgResize = cv2.resize(imgcrop, (imgSize, hCal))
                            else:
                                continue
                            imgResizeShape = imgResize.shape
                            hGap = math.ceil((imgSize-hCal)/2)
                            imgWhite[hGap:hCal + hGap, :] = imgResize
                        cv2.putText(imgOutput,labels[index],(x,y-20),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),2)
                        cv2.rectangle(imgOutput,(x-offset,y-offset),(x+w+offset,y+h+offset),(255,0,255),4)
                        cv2.imshow("Image",imgcrop)
                        cv2.imshow("ImageWhite",imgWhite)
                    cv2.imshow("Image",imgOutput)
                    cv2.waitKey(1)

        start_vid = tk.Button(self, height=2, width=20, text="Start Video", command=lambda: start_video())
        start_vid.pack()

app = Tk_Manage()
app.geometry("800x750")
app.mainloop()

# cap = cv2.VideoCapture(0)
# detector = HandDetector(maxHands=1)
# classifier = Classifier("Model/keras_model.h5","Model/labels.txt")
# offset = 20
# imgSize = 300
#
# folder = "Data/C"
# counter = 0
#
# labels = ["A","B","C"]
# while True:
#     success, img = cap.read()
#     imgOutput = img.copy()
#     hands, img = detector.findHands(img)
#     if hands:
#         hand = hands[0]
#         x,y,w,h = hand['bbox']
#
#         imgWhite = np.ones((imgSize,imgSize,3),np.int8)*255
#         imgcrop = img[y-offset:y + h+offset, x-offset:x + w+offset]
#         imgCropShape = imgcrop.shape
#
#
#         aspectRatio = h/w
#
#         if aspectRatio>1:
#             k = imgSize/h
#             wCal = math.ceil(k*w)
#             if imgcrop.size>0:
#                 imgResize = cv2.resize(imgcrop, (wCal, imgSize))
#             else:
#                 continue
#             imgResizeShape = imgResize.shape
#             wGap = math.ceil((imgSize-wCal)/2)
#             imgWhite[:, wGap:wCal + wGap] = imgResize
#             prediction, index =  classifier.getPrediction(imgWhite)
#             print(prediction,index)
#
#
#         else:
#             k = imgSize/w
#             hCal = math.ceil(k*h)
#             if imgcrop.size>0:
#                 imgResize = cv2.resize(imgcrop, (imgSize, hCal))
#             else:
#                 continue
#             imgResizeShape = imgResize.shape
#             hGap = math.ceil((imgSize-hCal)/2)
#             imgWhite[hGap:hCal + hGap, :] = imgResize
#         cv2.putText(imgOutput,labels[index],(x,y-20),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),2)
#         cv2.rectangle(imgOutput,(x-offset,y-offset),(x+w+offset,y+h+offset),(255,0,255),4)
#         cv2.imshow("Image",imgcrop)
#         cv2.imshow("ImageWhite",imgWhite)
#     cv2.imshow("Image",imgOutput)
#     cv2.waitKey(1)
