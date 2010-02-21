#!/usr/bin/env python
"""
Pyrana -- a minimalist music player.

This little script was written out of frustration with larger music
players. Pretty much all I've ever wanted out of a music player was one that
played random albums by picking a random artist, then picking a random album,
then playing that album, then picking _another random artist_.

For some reason,I've never run into a music player that played random albums
that way, which led to me often ending up having to skip past multiple Frank
Zappa albums when playing random albums. I like Zappa, but not that goddamned
much. Same deal with Slayer and Aphex Twin and Bad Religion, and all these other
artists and bands that I have discographies of.

Another problem I've had is that a lot of 'modern' music players base their
artist and album information off of metadata. I have a couple of issues with this:

1: My music collection is large. Doing a scan of metadata, even if it only needs
to be done once takes a long time. I hate it.

2: My music collection has unreliable metadata. This is because I'm a lazy
asshole, and haven't kept up with fixing metadata on music that I
download. That's right, I download music -- so do you, shut up. Since my music
collection is so large that the probability of me fixing the metadata ever is
basically nil. I can, however, rely on the directory structure of my music
collection.

This little ~50 line does one thing, and does it acceptably -- play random
albums from a music collection. Maybe it'll expand in the future. I doubt it.
"""
import os
import random
import time
import ConfigParser
import pygame.mixer as mixer

import pygtk
pygtk.require('2.0')
import gtk

import pynotify
pynotify.init("Basics")



class Pyrana(object):
    def __init__(self, root, frequency=44100):
        self.frequency = frequency
        self.statusIcon = gtk.StatusIcon()
        self.statusIcon.connect('activate', self.activate)
        self.root = root
        self.statusIcon.set_visible(True)
        self.statusIcon.set_tooltip("Pyrana!")
        self.statusIcon.set_from_file('stopped.png')

        self.config = ConfigParser.ConfigParser()
        self.config.read('pyrana.cfg')

        #give us a list of sets of albums by artists, assuming the directory structure
        #Artists
        # Albums
        #  Songs
        #This is a little ugly, but whatever. 
        self.artists = [set([os.path.join(artist, album)
                             for album in os.listdir(artist)
                             if os.path.isdir(os.path.join(artist, album))])
                        for artist in [os.path.join(root, artistname)
                                       for artistname in os.listdir(root)
                                       if os.path.isdir(os.path.join(root, artistname))]]

        #just in case we get some empty directories
        self.artists = filter(None, self.artists)

        gtk.main()
        
    def activate(self, widget, data=None):
        if not mixer.get_init():
            mixer.init(self.frequency)
            self.statusIcon.set_from_file('playing.png')
            self._play()
        else:
            mixer.quit()
            self.statusIcon.set_from_file('stopped.png')
            self.statusIcon.set_tooltip("Not Playing")

    def _play(self):
        while self.artists:
            if not mixer.get_init():
                break
            artist = random.choice(self.artists)

            #this ensures that we never play the same album twice
            albumpath = artist.pop()

            #hopefully, the tracks will be named in such a way that we can rely
            #on their names for ordering 
            album = sorted([os.path.join(albumpath, song)
                            for song in os.listdir(albumpath)
                            if song.endswith('mp3')])
            while album:
                if not mixer.get_init():
                    break
                if not mixer.music.get_busy():
                    songpath = album[0]
                    album = album[1:]
                    self._notify(songpath)
                    self.statusIcon.set_tooltip("Playing: %s" % songpath)
                    mixer.music.load(songpath)
                    mixer.music.play()
                else:
                    #avoid eating cpu
                    time.sleep(1)
                    #allow this shit to flush...
                    while gtk.events_pending():
                        gtk.main_iteration(False)


            self.artists = filter(None, self.artists)

    def _notify(self, songpath):
        to_display = "Playing: %s" % songpath
        if self.config.get('main', 'notification_type') == 'pynotify':
            n = pynotify.Notification("Pyrana", to_display)
            n.show()
        else:
            pass
    
if __name__ == '__main__':
    import sys
    player = Pyrana(sys.argv[1])

