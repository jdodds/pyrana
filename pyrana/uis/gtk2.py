from pkg_resources import resource_filename
from feather import Plugin


import pygtk
pygtk.require('2.0')
import gtk

class GTK2(Plugin):
    """A simplistic interface of nothing but a tray icon"""

    listeners = set(['APP_START'])
    messengers = set(['APP_END'])
    
    def recieve(self, message, payload):
        message_funcs = {
            'APP_START' : self.handle_APP_START
        }

        message_funcs[message](payload)

    def handle_APP_START(self, payload):
        self.status_icon = gtk.StatusIcon()
        # self.status_icon.connect('activate', self.on_left_click)
        self.status_icon.connect('popup-menu', self.on_right_click)
        self.status_icon.set_visible(True)
        self.status_icon.set_tooltip("Pyrana!")
        self.status_icon.set_from_file(resource_filename('pyrana', 'resources/stopped.png'))

        self.menu = gtk.Menu()
        skip_song = gtk.MenuItem("Skip Song")
        skip_album = gtk.MenuItem("Skip Album")
        quit_app = gtk.MenuItem("Quit")
        self.menu.append(skip_song)
        self.menu.append(skip_album)
        self.menu.append(quit_app)

        # skip_song.connect_object("activate", self.skip_song, "Skip Song")
        # skip_album.connect_object("activate", self.skip_album, "Skip Album")
        quit_app.connect_object("activate", self.quit, "Quit")

        skip_song.show()
        skip_album.show()
        quit_app.show()

        gtk.main()
        
    def on_right_click(self, data, event_button, event_time):
        self.menu.popup(None, None, None, event_button, event_time)

    def quit(self, widget, data=None):
        gtk.main_quit()
        self.send('APP_STOP')
    
