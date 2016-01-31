#!/usr/bin/env python
import random
import urllib
import urllib2

VERBOSE = False

def downloadRandomFlickrImage ():
    """
    Example URLs around Flickr:
    small icon    https://farm2.staticflickr.com/1573/24023749909_039594a2df_m.jpg
    Photo special https://www.flickr.com/photos/flickr/24023749909/
    DOWNLOAD      https://www.flickr.com/photos/flickr/24023749909/sizes/h/

    a href="https://c2.staticflickr.com/2/1573/24023749909_a99c178e5b_h_d.jpg">
					    Download the Large

    FINAL FILE    https://c2.staticflickr.com/2/1573/24023749909_a99c178e5b_h_d.jpg


    Steps to get (around) the stuff (they seem to have put in place to keep people like me out?):
    1) save author, ID
    2) https://www.flickr.com/photos/"+author+"/"+ID+"/sizes/h/
    3) find 
    a href="https://c2.staticflickr.com/2/1573/24023749909_a99c178e5b_h_d.jpg">
					    Download the Large
    4) retrieve the link.
    5)  Presto!  It's done!

    """
    url = "http://flickr.com/explore"
    response = urllib2.urlopen(url).read()

    startText = '{"_flickrModelRegistry":"photo-lite-models","pathAlias":"'
    pictureStartIndexs = []
    index = 0
    while index < len(response)-1: #not the last one though
        index = response.find(startText, index)
        if index == -1:
            break
        pictureStartIndexs.append(index + len(startText))
        index += 1
    if VERBOSE:
        print pictureStartIndexs

    goodies = response[ random.choice(pictureStartIndexs) :-1].partition(startText)[0]
    
    if VERBOSE:
        print goodies
        print ""

    author = goodies.partition('"')[0]
    print "Author of this picture is " + author

    temp = goodies.partition('"id":"')[2]
    ID = temp.partition('"}')[0]
    print "Picture ID is " + ID
    #STEP 1 COMPLETE!

    url = "https://www.flickr.com/photos/"+author+"/"+ID+"/sizes/h/"
    response = urllib2.urlopen(url)
    goodies = response.read().partition('Download the')[0].partition('<dt>Download</dt>')[2]

    """Goodies:
    <dd>
			    <a href="https://c2.staticflickr.com/2/1573/24023749909_a99c178e5b_h_d.jpg">
    """

    url = goodies.partition('href="')[2].partition('">')[0]
    if url.find("http") == -1: #Non-downloadable images will never have full URLs
        return False
    print "Downloading " + url
    #urllib.urlretrieve(url, "Your Special Web-Scraped Image")
    #print "Done!!!"


    #Set the background, if running linux.
    #import platform
    #if platform.system() == 'Linux':
    from gi.repository import Gio
    import os
    #print "Oooh, you run linux.  As a bonus, I'll set your wallpaper for you!"
    SCHEMA = 'org.gnome.desktop.background'
    KEY = 'picture-uri'

    user = os.getlogin()
    filey = "/home/" + user + "/Pictures/Wallpapers/latest-sunswitch-new.jpg"
    if VERBOSE:
        print filey

    urllib.urlretrieve(url, filey) #Redownloading the image is faster for me to write than copying it.

    gsettings = Gio.Settings.new(SCHEMA)
    gsettings.set_string(KEY, "file://" + filey)
    return True

def main():
    for i in range(30):
        if downloadRandomFlickrImage():
            return True
        else:
            print "Whoops!  The owner of that image disabled downloading it."
            print "Tossing the die again."
    return False

if __name__ == '__main__':
	main()
