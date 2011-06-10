#!/usr/bin/env python
""" Pyrana -- a minimalist music player.

This program was written out of frustration with larger music players. Pretty
much all I've ever wanted out of a music player was one that played random
albums by picking a random artist, then picking a random album, then playing
that album, then picking another random artist.

For some reason, I've never run into a music player that played random albums
that way, which led to me often ending up having to skip past multiple albums
by a particular artist, especially when the artist has a large discography.

While I call this player minimalist, that's not set in stone -- I'll probably
add last.fm scrobbling capability and other various features. These features
will, however, be ones that I find useful. I highly doubt this app will ever be
incredibly bloated.

"""

from pkg_resources import resource_filename
from hashlib import md5

import ConfigParser
import os
import random
import pickle
import shutil

import dbus

from pyrana.gui import PyranaGUI
from pyrana.player import PyranaPlayer


def build_index(path):
    """ Generate a list of sets of albums by artists.

    Assume the directory structure...

    Artists
    |-> Albums
      |-> Songs

    This is a little ugly, but whatever.

    """
    root = os.path.expanduser(path)
    artists = [[os.path.join(artist, album)
                         for album in os.listdir(artist)
                         if os.path.isdir(os.path.join(artist, album))]
                    for artist in
                    [os.path.join(root, artistname)
                     for artistname in os.listdir(root)
                     if os.path.isdir(os.path.join(root, artistname))]]

    # just in case we get some empty directories
    return [a for a in artists if a]


class Pyrana(object):

    """ Our player, sending sweet, sweet sounds to our speakers.  """

    audio_types = [
        '.mp3',
        '.m4a',
        '.ogg'
    ]

    def __init__(self, pidgin_status, use_notify, seen_file, music_dir):
        """ Wire up dependencies and defaults. """

        self.seen_file = seen_file
        self.pidgin_status = pidgin_status

        self.artists = build_index(music_dir)

        self.playing = False
        self.cur_song = None
        self.cur_album = None
        self.cur_artist = None
        self.cur_hash = None

        self.__init_seen()

        self.player = PyranaPlayer(self)
        self.gui = PyranaGUI(self, use_notify)

    def start(self):
        """ Start the main GTK and gstreamer threads. """

        self.player.start()
        self.gui.start()

    def end_of_song(self):
        self.player.stop()
        self.cur_song = None
        self.playing = False
        self.on_left_click(None)

    def on_left_click(self, widget, data=None):
        """ Toggle play status. """

        if not self.playing:
            if not self.cur_song:
                # don't change songs if we're paused
                self.get_next_unseen_song()
            self.start_playing()
        else:
            self.stop_playing()

    def start_playing(self):
        self.player.play()
        self.playing = True
        self.gui.play(self.cur_song)
        self.update_pidgin_status(self.cur_song)

    def stop_playing(self):
        self.player.pause()
        self.playing = False
        self.gui.pause(self.cur_song)
        self.update_pidgin_status()

    def get_next_unseen_song(self):
        self.cur_song = self.get_next_song()
        self.__update_hash()

        while self.seen.get(self.cur_hash):
            self.cur_song = self.get_next_song()
            self.__update_hash()

        self.player.song = self.cur_song
        self.__update_seen()

    def get_next_song(self):
        if not self.cur_album:
            artist = self.cur_artist

            while artist == self.cur_artist:
                print self.artists
                artist = random.choice(self.artists)

            print artist
            albumpath = artist.pop(random.randrange(len(artist)))
            self.cur_album = sorted(
                [os.path.join(albumpath, song)
                 for song in os.listdir(albumpath)
                 if os.path.splitext(song)[-1] in self.audio_types])

        song = self.cur_album[0]
        self.cur_album = self.cur_album[1:]
        return song

    def skip_song(self, data=None):
        self.end_of_song()

    def skip_album(self, data=None):
        self.cur_album = None
        self.end_of_song()

    def update_pidgin_status(self, songpath=None):
        if not self.pidgin_status:
            return False

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

    def __init_seen(self):
        self.seen_file = os.path.expanduser(self.seen_file)
        if os.path.exists(self.seen_file):
            self.seen = pickle.load(open(self.seen_file, 'r'))
        else:
            self.seen = {}

    def __update_hash(self):
        self.cur_hash = md5(self.cur_song).hexdigest()

    def __update_seen(self):
        self.seen[self.cur_hash] = True
        pickle.dump(self.seen, open(self.seen_file, 'w'))


def _check_and_set_home_config():
    """ Create from skel if necessary """

    home = os.path.expanduser('~')
    conf_dir = os.path.join(home, '.pyrana')

    if not os.path.isdir(conf_dir):
        os.mkdir(conf_dir)

    conf_file = os.path.join(conf_dir, 'pyrana.cfg')
    if not os.path.isfile(conf_file):
        base_conf = resource_filename('pyrana', 'resources/pyrana.cfg')

        shutil.copy(base_conf, conf_file)

    return conf_file


def main():
    """ Entry point for Pyrana.py.

    Start rockin'

    """
    conf_file = _check_and_set_home_config()

    config = ConfigParser.ConfigParser()
    config.read(conf_file)

    pidgin_status = config.get('main', 'update_pidgin_status')
    use_notify = config.get('main', 'use_notify')
    seen_file = config.get('main', 'seen_file')
    music_dir = config.get('main', 'music_dir')

    pyrana = Pyrana(pidgin_status, use_notify, seen_file, music_dir)

    pyrana.start()


if __name__ == '__main__':
    main()
