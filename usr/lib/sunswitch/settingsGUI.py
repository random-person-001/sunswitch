#!/usr/bin/env python
from gi.repository import Gtk
#import sys
import os
#sys.path.append(os.path.abspath("/usr/lib/sunswitch"))
import getSun
import settingsIO
#import gtk as Gtk

#defaultSettings= {"update":True,"date":True,"resIndex":0,"typeIndex":0,"green":True}
settingsOrder =   ["update",     "date",     "resIndex",  "typeIndex",  "green"]

class ListBoxWindow(Gtk.Window):
    settings = {"update":True,"date":True,"resIndex":0,"typeIndex":0,"green":True}

    def __init__(self):
        self.settings = settingsIO.readSettings()
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
        
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label("Insert Date At Bottom", xalign=0)
        self.dateCheck = Gtk.CheckButton()
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
        self.check = Gtk.CheckButton()
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
        self.resCombo = Gtk.ComboBoxText()
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
        self.picCombo = Gtk.ComboBoxText()
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
        self.settings["green"] = self.check.get_active()
        self.settings["date"] = self.dateCheck.get_active()
        self.settings["resIndex"] = self.resCombo.get_active()
        self.settings["typeIndex"] = self.picCombo.get_active()
#["update",     "date",     "resIndex",  "typeIndex",  "green"]
        return self.settings

    def debugDate(self, widget):
        print "date was changed"
    def debugGreen(self, widget):
        print "green was changed"

    def preview(self, widget):
        eh = False
        try:
            eh = getSun.doStuff(self.update())
        except IOError as er:
            print "No internet connection?"
        #finally:
        #    pass
        if not eh:
            self.button.label = "failed"
        print ""
        
    def save(self, widget):
        print "Saving:"
        settings = self.update()
        print settings
        settingsIO.saveSettings(settings)
        #for sett in settings:
        #    print sett
        #    print settings[sett]
        print ""

    def killy(self, widget):
        self.save(widget) #save on kill
        print "Bye!"
        Gtk.main_quit()
        

win = ListBoxWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
