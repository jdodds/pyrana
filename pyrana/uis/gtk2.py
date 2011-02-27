from pkg_resources import resource_filename
from multiprocessing import Process

from feather import Plugin

import pygtk
pygtk.require('2.0')
import gtk, gobject

import thread, sys, threading


class GTK2(Plugin):
    """A simplistic interface of nothing but a tray icon"""

    listeners = set(['APP_START', 'songstart', 'songpause', 'songresume'])
    messengers = set(['APP_END', 'play', 'pause', 'skipsong', 'skipalbum'])

    playing_icon = resource_filename('pyrana', 'resources/playing.png')
    stopped_icon = resource_filename('pyrana', 'resources/stopped.png')

    def __init__(self):
        super(GTK2, self).__init__()
        self.first_song_started = False

    def run(self):
        gtk.gdk.threads_init()
#        gobject.threads_init()
        message_funcs = {
            'APP_START' : self.handle_APP_START,
            'songstart' : self.handle_songplaying,
            'songresume' : self.handle_songplaying,
            'songpause' : self.handle_songstopped,
        }

        first = True
        while True:
#                gtk.main()
            message, payload = self.listener.get()
            message_funcs[message](payload)
            if first:
                first = False
                thread.start_new_thread(gtk.main, ())


#                threading.Thread(target=gtk.main).start()

    def send(self, message, payload=None):
        gobject.idle_add(super(GTK2, self).send, message, payload)

    def handle_APP_START(self, payload):
        self.status_icon = gtk.StatusIcon()
        self.status_icon.connect('activate', self.on_left_click)
        self.status_icon.connect('popup-menu', self.on_right_click)
        self.status_icon.set_visible(True)
        self.status_icon.set_tooltip("Pyrana!")
        self.status_icon.set_from_file(self.stopped_icon)

        self.menu = gtk.Menu()
        skip_song = gtk.MenuItem("Skip Song")
        play = gtk.MenuItem("Play/Pause")
        skip_album = gtk.MenuItem("Skip Album")
        quit_app = gtk.MenuItem("Quit")

        self.menu.append(play)
        self.menu.append(skip_song)
        self.menu.append(skip_album)
        self.menu.append(quit_app)

        play.connect_object('activate', self.on_left_click, 'Play/Pause')
        skip_song.connect_object("activate", self.skip_song, "Skip Song")
        skip_album.connect_object("activate", self.skip_album, "Skip Album")
        quit_app.connect_object("activate", self.quit, "Quit")

        play.show()
        skip_song.show()
        skip_album.show()
        quit_app.show()
#hmm        pass

    def skip_song(self, *args):
        self.send('skipsong')

    def skip_album(self, *args):
        self.send('skipalbum')
        
    def on_right_click(self, data, event_button, event_time):
        self.menu.popup(None, None, None, event_button, event_time)

    def quit(self, widget, data=None):
#        gobject.idle_add(gtk.main_quit)
#        thread.start_new_thread(gtk.main_quit, ())
#        gtk.main_quit()
#        gtk.gdk.threads_leave()
#        thread.exit()
        self.send('APP_STOP')

    def handle_songplaying(self, payload):
        self.status_icon.set_from_file(resource_filename('pyrana', 'resources/playing.png'))

    def handle_songstopped(self, payload):
        self.status_icon.set_from_file(resource_filename('pyrana', 'resources/stopped.png'))

    def on_left_click(self, widget=None, data=None):
        if self.first_song_started:
            self.send('pause')
        else:
            self.first_song_started = True
            self.send('play')



    
    
