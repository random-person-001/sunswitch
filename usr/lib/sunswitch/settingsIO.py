#!/usr/bin/env python
import os
user = os.getlogin()
#path = "/home/"+user+"/.sunswitch/settings.txt"
path = "/home/"+user+"/.config/sunswitch/settings.txt"
settingsDefault = {"update":True,"date":True,"resIndex":0,"typeIndex":0,"green":True,"updateInterval":13,"flickr":False}
settings = settingsDefault
settingsOrder = ["update","date","resIndex","typeIndex","green","updateInterval","flickr"]



def writeDefaultSettings():
    print "\n\n****** SETTINGS FILE CORRUPT--REWRITING ******"
    try:
        with open(path, 'w+') as f:
            #print 'hi'
            f.truncate() #Clear file contents
            for i in settingsOrder:
                print i + "   \t:\t" + str(settingsDefault[i])
                f.write(str(settingsDefault[i]) + "\n")
            #f.write('True\nTrue\n0\n0\nTrue')
            print "File was recreated successfully"
    except IOError:
        print "Problems writing file :(  \n Try again?"
        #print "File created!"
        #return readSettings()

def readSettings():
    rewrite = True
    resets = 0
    #try:
    while rewrite:
        try:        
            with open(path, 'r') as f:
                rewrite = False
                i=0
                print "\nReading:"
                for line in f:
                    that = ""
                    #print i
                    if i >= len(settings) or line == "\n":
                        print "Number of lines in settings, or unexpected empty lines, in file!"
                        rewrite = True
                        break
                    try:
                        that = line.strip()
                    except IndexError as er: #File isn't long enough, or too long
                        print er
                        rewrite = True
                        break
                    if that == "True":
                        that = True 
                    elif that == "False":
                        that = False
                    else:
                        try:
                            that = int(that)
                        except ValueError as er:
                            try:
                                that = float(that)
                            except ValueError as er:                            
                                print "Non-numbery lines in settings file.  Resetting."
                                print er
                                rewrite = True
                    #print that
                    settings[settingsOrder[i]] = that
                    i+=1
                print "Settings read."
                if i < len(settingsOrder):
                    print "Not enough settings in config.  Resetting."
                    rewrite = True
            if not rewrite:
                if (type(settings[settingsOrder[0]]) != type(True)) or (type(settings[settingsOrder[1]]) != type(True)) or (type(settings[settingsOrder[4]]) != type(True)) or (type(settings[settingsOrder[-1]]) != type(True)):
                    print "First two items (or last one) weren't bools!  Corrupt file!"
                    rewrite = True
                if (settings[settingsOrder[2]] > 2) or (settings[settingsOrder[3]] > 9):
                    print "Second two items weren't little ints!  Corrupt file!"
                    rewrite = True
        except IOError as er:
            print "Error reading file."
            rewrite = True    
        if rewrite:
            resets += 1
            if resets < 40:
                writeDefaultSettings()
            
            else:  #Assume something went terribly wrong
                print "\n\n\n\n********************************************************\n****** SETTINGS RESET CODE BROKEN!!!!  FIX MEEEEE!!! ******\n"
                return settingsDefault
        

    return settings
    #finally:
    #    return False


def saveSettings(dic):
    with open(path, "r+") as f:
        print "\nSaving:"
        f.truncate() #Clear file contents
        #for i in range(len(tupley)):
        #    print tupley[i]
        #    print >> f, tupley[i]
        for index in settingsOrder:
            print index + "    \t:\t" + str(dic[index])
            print >> f, dic[index]
        print "Done"
    #return True


