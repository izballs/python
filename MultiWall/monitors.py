from gi.repository import Gio, Gdk
from wand.image import Image, COMPOSITE_OPERATORS
from wand.drawing import Drawing
from wand.display import display
from wand.color import Color
from pathlib import Path
from os import system
class Monitor:
    def __init__(self, width, height, scaling, offset_x, offset_y, index, name, primary=False):
        self.width = int(width)
        self.height = int(height)
        self.scaling = int(scaling)
        self.primary = primary
        self.offset_x = int(offset_x)
        self.offset_y = int(offset_y)
        self.index = index
        self.name = name
        self.wallpaper = None

    def __repr__(self):
        return f'''{self.name}
{self.width} x {self.height}
{self.offset_x} x {self.offset_y}
'''

def sortMonitors(val):
    return val.offset_x;


class fullSize():
    def __init__(self, x, y,c):
        self.x = int(x)
        self.y = int(y)
        self.count = int(c)
    def __repr__(self):
        return f'''You have {self.count } Monitors
{self.x} x {self.y}'''
def isImageLargeEnough(imagePath, monitorFullSize):
    img = Image(filename=imagePath)
    print(img.size)
    if img.height >= monitorFullSize.y:
        if img.width >= monitorFullSize.x:
            return True
        else:
            return False
    else:
        return False

def resizeImage(imagePath, fullsize):
    mon_aspect = fullsize.x / fullsize.y
    img = Image(filename=imagePath)
    img_aspect = img.width / img.height
    if img_aspect > mon_aspect:
        if img.height >= fullsize.y:
            img.transform(resize='x'+str(fullsize.y))
            leftc = (img.width - fullsize.x) / 2
            leftc = round(leftc)
            print("everything trueee")
            img.crop(leftc, 0, width=fullsize.x, height=fullsize.y)
        else:
            print("img.height < fullsize.y")
    else:
        img.transform(resize=str(fullsize.x)+'x')
        topc = (img.height - fullsize.y) / 2
        topc = round(topc)
        img.crop(0, topc, width=fullsize.x, height=fullsize.y)
    return img
def makeItWork(imagePath, monitors, fullsize):
    img = resizeImage(imagePath, fullsize)
    images = []
    for mon in monitors:
        images.append(img.clone())
    i = 0
    for mon in monitors:
        print(mon)
        print(mon.offset_x)
        print(mon.offset_y)
        print(mon.width)
        print(mon.height)
        images[i].crop(mon.offset_x,mon.offset_y,width=mon.width,height=mon.height)
        i += 1
    fullImage = Image(width=fullsize.x, height=fullsize.y, background=Color('black'))
    print(fullImage.size)
    with Drawing() as draw:
        for idx,im in enumerate(images):
            draw.composite(operator='atop', left=monitors[idx].offset_x, top=monitors[idx].offset_y,
                    width=monitors[idx].width, height=monitors[idx].height, image=im)
            draw(fullImage)
            filenam = "image" + str(idx) + ".jpg"
            im.save(filename=filenam)
        fullImage.save(filename="fullImage.jpg") 
    system("feh --bg-scale --no-xinerama ./fullImage.jpg")
def calculateFullsize(monitors):
    x = 0
    y = 0
    c = 0
    for mon in monitors:
        x += mon.width
        if mon.height > y:
            y = mon.height
        c += 1
    full = fullSize(x, y, c)
    return full

def createThumbnail(path, monitors, fullsize):
    img = resizeImage(path, fullsize)
    with Drawing() as draw:
        draw.fill_color = Color("transparent")
        draw.stroke_color = Color("red")
        draw.stroke_width = 24
        lastL = 0
        for mon in monitors:
            draw.rectangle(left=mon.offset_x, top=mon.offset_y, right=mon.offset_x + mon.width, bottom=mon.offset_y + mon.height, radius=3)
            draw(img)
    img.transform(resize="500x")
    img.save(filename='thumbnail.jpg')
    size = [img.width, img.height]
    return size

def monitorInfo():
    display = Gdk.Display.get_default()
    monitorCount = display.get_n_monitors()
    get_monitor_rect = lambda i: display.get_monitor(i).get_geometry()
    monitors = [ ]
    for i in range(0, monitorCount):
        monitors.append(
            Monitor(
                display.get_monitor(i).get_geometry().width,
                display.get_monitor(i).get_geometry().height,
                display.get_monitor(i).get_scale_factor(),
                display.get_monitor(i).get_geometry().x,
                display.get_monitor(i).get_geometry().y,
                i,
                f'Monitor {i} ({display.get_monitor(i).get_model()})',
                display.get_monitor(i).is_primary()
            )
        )
    monitors.sort(key = sortMonitors) 
    return monitors
