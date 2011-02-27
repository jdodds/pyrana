#!/usr/bin/env python
"""
Pyrana -- a minimalist music player.

This program was written out of frustration with larger music players. Pretty
much all I've ever wanted out of a music player was one that played random
albums by picking a random artist, then picking a random album, then playing
that album, then picking another random artist.

For some reason,I've never run into a music player that played random albums
that way, which led to me often ending up having to skip past multiple albums by
a particular artist, especially when the artist has a large discography.

While I call this player minimalist, that's not set in stone -- I'll probably
add last.fm scrobbling capability and other various features. These features
will, however, be ones that I find useful. I highly doubt this app will ever be
incredibly bloated.
"""


import os
import random
import ConfigParser

import pynotify
pynotify.init("Basics")



class Pyrana(object):
    """Our player, sending sweet, sweet sounds to our speakers.
    """

    audio_types = [
        '.mp3',
        '.m4a',
        '.ogg'
    ]

    def __init__(self):
        """Initialize our player with a root directory to search through for
        music, and start the gtk main thread.
        """
        from pkg_resources import resource_filename

        self.__check_and_set_home_config()

        self.config = ConfigParser.ConfigParser()
        self.config.read(self.conf_file)

        self.pidgin_status = self.config.get('main',
                                             'update_pidgin_status')
        self.use_notify = self.config.get('main', 'use_notify')
        self.seen_file = self.config.get('main', 'seen_file')
        self.__init_seen()


        root = os.path.expanduser(
            self.config.get('main', 'music_dir'))
        self.artists = [[os.path.join(artist, album)
                             for album in os.listdir(artist)
                             if os.path.isdir(os.path.join(artist, album))]
                        for artist in
                        [os.path.join(root, artistname)
                         for artistname in os.listdir(root)
                         if os.path.isdir(os.path.join(root, artistname))]]

        #just in case we get some empty directories
        self.artists = [a for a in self.artists if a]



        self.cur_song = None
        self.cur_album = None
        self.cur_artist = None
        self.cur_hash = None

        gtk.main()

    def on_eos(self, bus, msg):
        self.player.set_state(gst.STATE_NULL)
        self.cur_song = None
        self.playing = False
        self.on_left_click(None)

    def on_left_click(self, widget, data=None):
        """Click handler for our status icon. Play or stop playing,
        respectively.
        """
        from pkg_resources import resource_filename
        if not self.playing:
            self.playing = True
            self.status_icon.set_from_file(
                resource_filename('pyrana', 'resources/playing.png')
            )
            if not self.cur_song:
                self.cur_song = self.get_next_song()
                self.__update_hash()

                while self.seen.get(self.cur_hash):
                    self.cur_song = self.get_next_song()
                    self.__update_hash()

                self.__update_seen()

            self.status_icon.set_tooltip(self.cur_song)
            if self.use_notify:
                self.notify(self.cur_song)
            if self.pidgin_status:
                self.update_pidgin_status(self.cur_song)


        else:
            self.status_icon.set_from_file(
                resource_filename('pyrana', 'resources/stopped.png')
            )

            self.status_icon.set_tooltip("[PAUSED] %s" % self.cur_song)
            if self.pidgin_status:
                self.update_pidgin_status()

    def get_next_song(self):
        import os.path
        if not self.cur_album:
            artist = self.cur_artist

            while artist == self.cur_artist:
                artist = random.choice(self.artists)

            albumpath = artist.pop(random.randrange(len(artist)))
            self.cur_album = sorted(
                [os.path.join(albumpath, song)
                 for song in os.listdir(albumpath)
                 if os.path.splitext(song)[-1] in self.audio_types])

        song = self.cur_album[0]
        self.cur_album = self.cur_album[1:]
        return song

    def skip_album(self, data=None):
        self.cur_album = None


    def notify(self, songpath):
        """Use libnotify to show growl-like alerts about what's playing.
        """
        to_display = "Playing: %s" % songpath
        notification = pynotify.Notification("Pyrana", to_display)
        notification.show()

    def update_pidgin_status(self, songpath=None):
        import dbus
        bus = dbus.SessionBus()

        if songpath:
            parts = songpath.split('/')
            artist = parts[-3]
            album = parts[-2]
            song = parts[-1]
            message = "%s (%s): %s" % (artist, album, song)
        else:
            message = "Paused"

        if "im.pidgin.purple.PurpleService" in bus.list_names():
            purple = bus.get_object("im.pidgin.purple.PurpleService",
                                    "/im/pidgin/purple/PurpleObject",
                                    "im.pidgin.purple.PurpleInterface")
            current = purple.PurpleSavedstatusGetType(
                purple.PurpleSavedstatusGetCurrent())
            status = purple.PurpleSavedstatusNew("", current)
            purple.PurpleSavedstatusSetMessage(status, message)

            purple.PurpleSavedstatusActivate(status)

    def __check_and_set_home_config(self):
        import os
        from pkg_resources import resource_filename

        home = os.path.expanduser('~')
        conf_dir = os.path.join(home, '.pyrana')

        if not os.path.isdir(conf_dir):
            os.mkdir(conf_dir)

        conf_file = os.path.join(conf_dir, 'pyrana.cfg')
        if not os.path.isfile(conf_file):
            base_conf = resource_filename('pyrana', 'resources/pyrana.cfg')

            import shutil
            shutil.copy(base_conf, conf_file)

        self.conf_file = conf_file
    def __init_seen(self):
        import pickle
        self.seen_file = os.path.expanduser(self.seen_file)
        if os.path.exists(self.seen_file):
            self.seen = pickle.load(open(self.seen_file, 'r'))
        else:
            self.seen = {}
            
    def __update_hash(self):
        from md5 import md5
        self.cur_hash = md5(self.cur_song).hexdigest()

    def __update_seen(self):
        import pickle
        self.seen[self.cur_hash] = True
        pickle.dump(self.seen, open(self.seen_file, 'w'))
        
    
            

def main():
    """Entry point for Pyrana.py.
    Start rockin'
    """

    from feather import Application
    from pyrana.uis import GTK2
    from pyrana.players import PyGST
    from pyrana.playlists import SaneRandomAlbums
    from pyrana.plugins import Notify, PidginStatus

    pyrana = Application(['play', 'pause'])
#    pyrana = Application([])
    p = GTK2()
    pyrana.register(p)
    pyrana.register(PyGST())
    pyrana.register(SaneRandomAlbums('~/music'))
    pyrana.register(Notify())
    pyrana.register(PidginStatus())
    pyrana.start()
#    Pyrana()

if __name__ == '__main__':
    main()
