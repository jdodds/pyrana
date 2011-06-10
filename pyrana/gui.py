from pkg_resources import resource_filename

import pygtk
import gtk
import pynotify

pygtk.require("2.0")
pynotify.init("Basics")


class PyranaGUI(object):

    def __init__(self, helper, use_notify):
        self.use_notify = use_notify

        self.status_icon = gtk.StatusIcon()
        self.status_icon.set_visible(True)
        self.status_icon.set_tooltip("Pyrana!")
        self.status_icon.set_from_file(resource_filename("pyrana", "resources/stopped.png"))

        self.menu = gtk.Menu()

        skip_song = gtk.MenuItem("Skip Song")
        skip_album = gtk.MenuItem("Skip Album")
        quit_app = gtk.MenuItem("Quit")

        self.menu.append(skip_song)
        self.menu.append(skip_album)
        self.menu.append(quit_app)

        self.status_icon.connect("activate", helper.on_left_click)
        self.status_icon.connect("popup-menu", self._on_right_click)
        skip_song.connect_object("activate", helper.skip_song, "Skip Song")
        skip_album.connect_object("activate", helper.skip_album, "Skip Album")
        quit_app.connect_object("activate", self._quit, "Quit")

        skip_song.show()
        skip_album.show()
        quit_app.show()

    def start(self):
        gtk.main()

    def pause(self, song):
        self.status_icon.set_from_file(
            resource_filename('pyrana', 'resources/stopped.png')
        )
        self.status_icon.set_tooltip("[PAUSED] %s" % song)

    def play(self, song):
        self._notify(song)

        self.status_icon.set_from_file(
            resource_filename('pyrana', 'resources/playing.png')
        )
        self.status_icon.set_tooltip(song)

    def _notify(self, songpath):
        """Use libnotify to show growl-like alerts about what's playing.
        """
        if not self.use_notify:
            return False

        to_display = "Playing: %s" % songpath
        notification = pynotify.Notification("Pyrana", to_display)
        notification.show()

    def _on_right_click(self, data, event_button, event_time):
        self.menu.popup(None, None, None, event_button, event_time)

    def _quit(widget, data=None):
        gtk.main_quit()

