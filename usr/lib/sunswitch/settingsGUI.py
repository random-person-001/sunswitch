#!/usr/bin/env python
from gi.repository import Gtk
import os
import getSun
import getFlickr
import settingsIO
#import gtk as Gtk

#defaultSettings= {"update":True,"date":True,"resIndex":0,"typeIndex":0,"green":True,"updateInterval":13,"flickr":False}
settingsOrder =   ["update",     "date",     "resIndex",  "typeIndex",  "green",     "updateInterval",   "flickr"]

class ListBoxWindow(Gtk.Window):
    settings = {"update":True,"date":True,"resIndex":0,"typeIndex":0,"green":True,"flickr":False}

    def __init__(self):
        self.settings = settingsIO.readSettings()
        self.updateSeconds = 20
        self.check = 'placeholder'
        self.scale = 'placeholder'
        self.resCombo = 'placeholder'
        self.picCombo = Gtk.ComboBoxText()
        self.resCombo = Gtk.ComboBoxText()
        self.dateCheck = Gtk.CheckButton()
        self.check = Gtk.CheckButton()
        self.scale = Gtk.HScale()
        if self.settings == False:
            print "Uh-oh!  Your settings file appears to be corrupt.  We'll remake it."
            self.settings = settingsIO.writeDefaultSettings()

        Gtk.Window.__init__(self, title="Sunswitch Settings")
        self.set_icon_from_file("/usr/share/app-install/icons/sunswitch-settings.png")
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        hbox.pack_start(listbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox, True, True, 0)

        label1 = Gtk.Label("Background Automatic Update", xalign=0)
        label2 = Gtk.Label("Requires internet access", xalign=0)
        vbox.pack_start(label1, True, True, 0)
        vbox.pack_start(label2, True, True, 0)

        self.switch = Gtk.Switch()
        self.switch.props.valign = Gtk.Align.CENTER
        self.switch.set_active(self.settings["update"])
        #self.switch.connect("activate", self.update)
        hbox.pack_start(self.switch, False, True, 0)

        listbox.add(row)

#Flickr stuff
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label("Screw all this, use a random flickr photo instead", xalign=0)
        self.flickrCheck = Gtk.CheckButton()
        self.flickrCheck.connect("toggled", self.checkedFlickr)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(self.flickrCheck, False, True, 0)
        self.flickrCheck.set_active(self.settings["flickr"])

        listbox.add(row)


#Slider for update
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        label = Gtk.Label("Update Interval", xalign=0)
        row.add(hbox)
        self.scale.set_range(1, 35)
        self.scale.set_size_request(200, 29)
        self.scale.set_value(200)
        self.scale.set_value(self.settings["updateInterval"])
        self.scale.connect("format-value", self.changeScaleDisplay)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(self.scale, False, True, 0)
        #scale.connect("value-changed", self.updateInterval)

        listbox.add(row)

        
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label("Insert Date At Bottom", xalign=0)
        self.dateCheck.connect("toggled", self.debugDate)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(self.dateCheck, False, True, 0)
        print self.settings
        self.dateCheck.set_active(self.settings["date"])

        listbox.add(row)
        
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label("Decrease Green", xalign=0)
        self.check.connect("toggled", self.debugGreen)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(self.check, False, True, 0)
        #print self.settings
        self.check.set_active(self.settings["green"])

        listbox.add(row)
        
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label("Image Resolution", xalign=0)
        self.resCombo.insert(0, "0", "2048")
        self.resCombo.insert(1, "1", "1024")
        self.resCombo.insert(2, "2", "512")
        self.resCombo.set_active(self.settings["resIndex"])
        #self.resCombo.connect("changed", self.update)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(self.resCombo, False, True, 0)

        listbox.add(row)


        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label("Image Type", xalign=0)
        self.picCombo.insert(0, "1", "171")
        self.picCombo.insert(1, "1", "193")
        self.picCombo.insert(2, "2", "304")
        self.picCombo.insert(3, "2", "211")
        self.picCombo.insert(4, "0", "131")
        self.picCombo.insert(5, "2", "335")
        self.picCombo.insert(6, "2", "094")
        self.picCombo.insert(7, "2", "1600")
        self.picCombo.insert(8, "2", "1700")
        self.picCombo.insert(9, "2", "Magnetogram")
        self.picCombo.set_active(self.settings["typeIndex"])
        #self.picCombo.connect("changed", self.update)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(self.picCombo, False, True, 0)

        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label("Save Configuration", xalign=0)
        self.button = Gtk.Button(label="Save")
        self.button.connect("clicked", self.save)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(self.button, False, True, 0)

        listbox.add(row)

        
        #row = Gtk.ListBoxRow()
        #previewbox = Gtk.IconView.new()
        #previewbox.set_selection_mode(0)
        """
        previewbox.set_pixbuf_column(column)
        # Create a tuple with image file
        immagini = () 
#Zoom them to a third of the 512
        try:
            image = Gtk.Image()
                        
            path = "~/.sunswitch/preview.jpg"
            image.set_from_file(path)
            #pix_w = pixbuf.get_width()
            #pix_h = pixbuf.get_height()
            #new_h = (pix_h * DEFAULT_IMAGE_WIDTH) / pix_w   # Calculate the scaled height before resizing image
            #scaled_pix = pixbuf.scale_simple(DEFAULT_IMAGE_WIDTH, new_h, gtk.gdk.INTERP_TILES)
            #model.append((scaled_pix, im))
        except:
            pass
        """
        #listbox.add(previewbox)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label("Preview Changes on Desktop", xalign=0)
        self.button = Gtk.Button(label="Update Background")
        self.button.connect("clicked", self.preview)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(self.button, False, True, 0)

        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        row.add(hbox)
        #label = Gtk.Label("Exit and Save", xalign=0)
        self.exit = Gtk.Button(label="Save and Exit")
        self.exit.connect("clicked", self.killy)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(self.exit, False, True, 0)

        listbox.add(row)

        #self.scale.checkedFlickr(self) # Update greyed-out things
        #self.checkedFlickr(self.exit)
        #self.scale.flickrUpdate()

    def update(self):
        """
        self.settings[0] = self.switch.get_active()
        self.settings[1] = self.check.get_active()
        self.settings[4] = self.dateCheck.get_active()
        #self.settings[2] = self.resCombo.get_active_text()
        self.settings[2] = self.resCombo.get_active()
        #pic = self.picCombo.get_active_text()
        #self.settings[3] = self.picCombo.get_active()
        #if pic == "Magnetogram":
        #    self.settings[3] = "HMIB"
        #elif len(pic) < 4:
        #    self.settings[3] = "0"+pic
        return (self.settings[0], self.settings[1], self.settings[2], self.settings[3], self.settings[4])
        """
        self.settings["update"] = self.switch.get_active()
        self.settings["flickr"] = self.flickrCheck.get_active()
        self.settings["updateInterval"] = self.scale.get_value()
        self.settings["green"] = self.check.get_active()
        self.settings["date"] = self.dateCheck.get_active()
        self.settings["resIndex"] = self.resCombo.get_active()
        self.settings["typeIndex"] = self.picCombo.get_active()
        return self.settings

    def checkedFlickr(self, widget):
        if self.flickrCheck.get_active():
            self.check.set_sensitive(False)
            self.dateCheck.set_sensitive(False)
            self.resCombo.set_sensitive(False)
            self.picCombo.set_sensitive(False)
            self.scale.set_sensitive(True)
        else:
            self.check.set_sensitive(True)
            self.dateCheck.set_sensitive(True)
            self.resCombo.set_sensitive(True)
            self.picCombo.set_sensitive(True)
            self.scale.set_sensitive(False)
        self.update()


    def debugDate(self, widget):
        print "date was changed"
    def debugGreen(self, widget):
        print "green was changed"

    def changeScaleDisplay(self, widget, value):
        value = .01 * 2.71828 ** (.302*(value+24.4)) - 6
        self.updateSeconds = value
        if (value < 60):
            return str(round(value)) + " s"
        if (value < 3600):
            return str(round(value/60)) + " m"
        if (value < 3600*24):
            return str(round(value/3600)) + " hr"
        if (value < 3600*24*8):
            return str(round(value/24/3600)) + " days"

    def preview(self, widget):
        eh = False
        try:
            if not self.settings["flickr"]:
                eh = getSun.doStuff(self.update())
            else:
                eh = getFlickr.main()
        except IOError as er:
            print "No internet connection?"
        #finally:
        #    pass
        if not eh:
            self.button.label = "failed"
        print ""
        
    def save(self, widget):
        print "Saving configuration"
        settings = self.update()
        #print settings
        settingsIO.saveSettings(settings)
        self.restartBackground()
        #for sett in settings:
        #    print sett
        #    print settings[sett]
        print ""

    def killy(self, widget):
        self.save(widget) #save on kill
        print "Bye!"
        Gtk.main_quit()

    def restartBackground(self):
        try:
            print "Killing background sunswitch"
            import subprocess, signal, os
            p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
            out, err = p.communicate()

            for line in out.splitlines():
                #print line
                if 'sunswitch-bac' in line:
                    print "Killed process: " + line
                    pid = int(line.split(None, 1)[0])
                    os.kill(pid, signal.SIGKILL)
            print "Restarting background sunswitch"
            p = subprocess.Popen(['nohup', 'sunswitch-background', '2', str(int(self.updateSeconds))], stdout=open('/dev/null', 'w'),  stderr=open('/home/'+os.getlogin()+'/.config/sunswitch/background.log', 'a'), preexec_fn=os.setpgrp)
            print "Successfully killed any earlier processes, and started own."
        finally:
            pass
        
        #out, err = p.communicate()
        #print out
        #os.system( " "+ str(self.updateSeconds) +" &" )

        

win = ListBoxWindow()
win.connect("delete-event", Gtk.main_quit)
win.connect("destroy-event", Gtk.main_quit)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
