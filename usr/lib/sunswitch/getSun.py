#!/usr/bin/env python

# The following two lines are a workaround if cv2 is not recognised when installed.  If you didn't have problems
# with importing cv2 otherwise, you can just comment them out.


try:
    import cv2
    print "cv2 found the normal way"
except ImportError as er:
    import sys
    sys.path.append('/usr/local/lib/python2.7/site-packages')
    sys.path.append('/usr/lib/python2.7/dist-packages')
    import cv2
    print "cv2 found with the workaround of adding usr/local/lib/....../site-packages"
    
    
#import Image #not used, no more need to convert gif to png or jpg

import urllib
import os
#sys.path.append(os.path.abspath("/usr/lib/sunswitch"))
import settingsIO


defaultSettings = {"update":True,"date":True,"resIndex":0,"typeIndex":0,"green":True}
settingsOrder =   ["update",     "date",     "resIndex",  "typeIndex",  "green"]

#Variables from config file
#autoUpdate = 0#True     #not used here
#decreaseGreen = 'e'#True
#imageRes = 0#"2048"
#whichPicture = '0' #"0171"

#Non-settable variables
class VariableHandler ():
    
    def __init__(self, settings):
        print settings
        self.reses =['2048','1024','512']
        self.pics = ['0171','0193','0304','0211','0131','0335','0094','1600','1700','HMIB']
        self.decreaseGreen = settings["green"]
        self.imageRes = int(self.reses[int(settings["resIndex"])])
        self.whichPicture = self.pics[int(settings["typeIndex"])]
        self.insertDate = settings["date"]
        
        self.mainAddress = "http://sdo.gsfc.nasa.gov/assets/img/latest/latest_"+str(self.imageRes)+"_"+self.whichPicture+".jpg"
        self.dateAddress = "http://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_"+self.whichPicture+".jpg"

        self.user = os.getlogin()
        self.finalFile = "/home/"+self.user+"/Pictures/Wallpapers/latest-sun-new.jpg"
        #print "Set " + self.finalFile + " as your desktop background with image viewer."
        self.mainFile = "/home/"+self.user+"/.config/sunswitch/latest-sun"#"/tmp/latest-sun"#"/home/"+self.user+"/.sunswitch/latest-sun"
        self.dateFile = "/home/"+self.user+"/.config/sunswitch/sun-date"#"/tmp/latest-sun"#"/home/"+self.user+"/.sunswitch/sun-date"




def monitorWidth(): #Helps put the date in the corner where it should be (sometimes)
    from gi.repository import Gtk
    screen = Gtk.Window().get_screen()
    if screen.get_n_monitors() > 1: #Multimonitor display; don't bother with date
        return "multiple monitors"
    firstMon = screen.get_monitor_geometry(0)
    return firstMon.width

def recolorAndDateMain(original, saveAs):#oldOneToo):
    imgName = original
    img = cv2.imread(imgName)
    if (img == None):
        print "******Invalid image.  Is it bad format or nonexistant?******"
        return False

    b = img[:,:,0]
    g = img[:,:,1]
    r = img[:,:,2]

    oldG = g
    #for line in g:
    #    print line 
    """
    for i in g:  # takes a super long time
        for th in i:
            if th <= 50:
                th *= 2 """
    #print s.decreaseGreen
    if s.decreaseGreen:
        g = g/2 + b/2 #Composite green as half green, half blue
    
    #Testing components of image by setting them (effectively) to zero
    #g/=200
    #b/=200
    #r/=200

    
    if s.imageRes > 1025 and s.insertDate: #Only bother inserting the date visibly if it's high enough rez
        #Insert the date, from the smaller 1024 image, on the lower right of the main img
        #print "Probs gonna insert date"

        dateImg = cv2.imread(s.dateFile+".jpg")
        date = dateImg[1006-20:1006, 200:500]  # 20 by 300 (by 3)

        if s.decreaseGreen:        
            #redden it
            print "Decreasing Green"
            dateR = date[:,:,2]
            dateB = date[:,:,0]
            dateG = date[:,:,1]/2 + dateB/2
            date = cv2.merge((dateB,dateG,dateR))

        width = monitorWidth()
        #print width
        #print s.imageRes
        if (width != "multiple monitors") and (width <= s.imageRes):
                print "Inserting Date"
                img[width-30:width-10, s.imageRes-300:s.imageRes] = date
            

    #if oldOneToo:
    #    imgOld = cv2.imread(mainFile+"-old.jpg")
    #    if imgOld.all() == img.all():
    #        print "Image unchanged"
    #        #return True #sometimes induces bugs?  Commented out
    
    img = cv2.merge((b,g,r))
    ehhy = cv2.imwrite(saveAs, img) #true if write success
    return ehhy



def printDate():
    from time import localtime
    #import calendar as ca  #BASH script handles this
    now_ = localtime()
    #date = str(now_[0]) + ' ' + str(ca.month_abbr[now_[1]]) + ' ' + str(now_[2]) + '\n'
    time = str(now_[3]) + ':' + str(now_[4])
    print time

def renameOld ():
    import Image
    try:    
        with Image.open(finalFile) as im:
            im.save(mainFile+"-old.jpg")
        return True    
    except IOError:
        print "Whoops!  There wasn't a pic from before."
        return False

def doStuff(settings=()):
    global s
    if settings == ():
        #settings = defaultSettings
        settings = settingsIO.readSettings()

    #for i in settings:
        #print i + "   :   " + str(dic[index])

    s = VariableHandler(settings)
    printDate()  # give the log some stuff
    #oldOneToo = renameOld() #unneeded
    #success = downloader.download(mainFile, mainAddress) and downloader.download(dateFile, dateAddress)
    urllib.urlretrieve(s.mainAddress, s.mainFile+".jpg")
    if settings["date"]:
        urllib.urlretrieve(s.dateAddress, s.dateFile+".jpg")

    humph = recolorAndDateMain(s.mainFile + ".jpg", s.finalFile)#oldOneToo)
    if humph:
        print "Success!\n"
        return True
    else:
        print "Something went wrong with saving downloaded image.\n"
        return False

if __name__ == '__main__':
    doStuff()
