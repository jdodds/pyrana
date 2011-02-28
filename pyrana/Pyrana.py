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
    def __init__(self):
        from pkg_resources import resource_filename
        self.__check_and_set_home_config()

        self.config = ConfigParser.ConfigParser()
        self.config.read(self.conf_file)

        self.__init_seen()


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
    from pyrana.players import PyGSTPlayer, PyGamePlayer, PygletPlayer
    from pyrana.playlists import SaneRandomAlbums
    from pyrana.plugins import Notify, PidginStatus

    pyrana = Application(['play', 'pause', 'skipsong', 'skipalbum'])
    pyrana.register(GTK2())
    pyrana.register(PyGSTPlayer())
    pyrana.register(SaneRandomAlbums('~/music', '~/.pyrana/seen'))
    pyrana.register(Notify())
    pyrana.register(PidginStatus())
    pyrana.start()


if __name__ == '__main__':
    main()
