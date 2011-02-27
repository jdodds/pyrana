from pkg_resources import resource_filename

from feather import Plugin

import pygtk
pygtk.require('2.0')
import gtk, gobject

class GTK2(Plugin):
    """A simplistic interface of nothing but a tray icon"""

    listeners = set(['APP_START'])
    messengers = set(['APP_STOP', 'play', 'pause', 'skipsong', 'skipalbum'])
    name = 'GTK2'

    playing_icon = resource_filename('pyrana', 'resources/playing.png')
    stopped_icon = resource_filename('pyrana', 'resources/stopped.png')

    def __init__(self):
        super(GTK2, self).__init__()
        self.playing = False
        self.first_played = False

    def run(self):
        gtk.gdk.threads_init()

        message_funcs = {
            'APP_START' : self.handle_APP_START,
            'SHUTDOWN' : self.shutdown
        }

        first = True
        while self.runnable:
            gtk.threads_enter()
            message, payload = self.listener.get()
            message_funcs[message](payload)
            if first:
                first = False
                gtk.main()
            gtk.threads_leave()

        super(GTK2, self).send('APP_STOP')


    def send(self, message, payload=None):
        def run_send():
            super(GTK2, self).send(message, payload)
            return False
        gobject.idle_add(run_send)

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

    def skip_song(self, *args):
        self.send('skipsong')

    def skip_album(self, *args):
        self.send('skipalbum')
        
    def on_right_click(self, data, event_button, event_time):
        self.menu.popup(None, None, None, event_button, event_time)

    def quit(self, widget, data=None):
        self.runnable = False
        gtk.main_quit()

    def on_left_click(self, widget=None, data=None):
        if self.playing:
            self.playing = False
            self.status_icon.set_from_file(self.stopped_icon)
            self.send('pause')
        else:
            self.playing = True
            self.status_icon.set_from_file(self.playing_icon)
            if self.first_played:
                self.send('pause')
            else:
                self.first_played = True
                self.send('play')



    
    
