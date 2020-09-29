#!/bin/python
# -*- coding: utf-8 -*-
from monitors import *
import os
import sys
#from PyQt5.QtWidgets import (QMainWindow, QGraphicsRectItem , QLabel, QAction, QMenu, QApplication, QWidget, QToolTip, QPushButton, QGridLayout)
#from PyQt5.QtGui import (QFont, QPainter)
#from PyQt5.QtCore import (QRectF, QRect)
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image as IMG

class MainWindow:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack()
        self.fullsizeLabel = StringVar()
        self.monitorSizes = []
        self.path = "./fullImage.jpg"
        self.initUI()

    def initUI(self):
        self.refreshMonitorInfo()
        idx = 0
        for mon in self.monitors:
            temp = StringVar()
            temp.set(mon)
            self.monitorSizes.append(temp)
            fgcolor = "black"
            if mon.primary:
                fgcolor = "red"
            Label(self.frame, fg=fgcolor, textvariable=temp).grid(row=1, column=idx)
            idx += 1
        center = int(len(self.monitorSizes) / 2)
        Label(self.frame, textvariable=self.fullsizeLabel).grid(row=2, column=center)
       
        self.thumbImg = ImageTk.PhotoImage(IMG.open("thumbnail.jpg"))
        size = self.reCreateThumb()
        
        self.thumb = Canvas(self.frame, width=size[0], height=size[1])
        self.thumb.grid(row=0,columnspan=len(self.monitorSizes))
        self.thumb.create_image(0,0,image=self.thumbImg, anchor='nw')
        
        self.browse = Button(self.frame, text="browse wallpaper", command=self.definePath)
        self.browse.grid(row=3, column=0)

        self.setImage = Button(self.frame, text="Set Wallpaper", command=self.setPaper)
        self.setImage.grid(row=3,column=len(self.monitorSizes) - 1)
    
    def setPaper(self):
        makeItWork(self.path, self.monitors, self.fullsize)
    def definePath(self):
        self.path = filedialog.askopenfilename(initialdir = "/", title = "Select Wallpaper", filetypes=(("Image files", "*.jpg,*.jpeg,*.png,*.bmp,*.gif"), ("All files", "*")))
        size = self.reCreateThumb()
        self.reSetThumb(size)
    def reCreateThumb(self):
        size = createThumbnail(self.path, self.monitors, self.fullsize)
        return size

    def reSetThumb(self, size):
        try:
            self.thumbImg = ImageTk.PhotoImage(IMG.open("thumbnail.jpg"))
        except IOError:
            self.thumbImg = ImageTk.PhotoImage()
        self.thumb.create_image(0,0,image=self.thumbImg, anchor='nw')

    def refreshMonitorInfo(self):
        self.monitors = monitorInfo()
        self.fullsize = calculateFullsize(self.monitors)
        self.fullsizeLabel.set(self.fullsize)


if __name__ == '__main__':

    root = Tk()

    mainWindow = MainWindow(root)

    root.mainloop()



    #monitors = monitorInfo()

    #check = isImageLargeEnough(path, fullsize)
    #if check:
    #    makeItWork(path, monitors, fullsize)
    #else:
    #    print("Image not large enough")

