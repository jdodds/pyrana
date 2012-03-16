Pyrana -- A minimalist music player.
====================================

ABOUT
-----

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

REQUIREMENTS
------------

Pyrana, by default, requires PyGTK (http://www.pygtk.org/downloads.html), and
gst-python >= 0.10.0, which is likely available from your package manager --
it's the python2 bindings to gstreamer. gst-python isn't available via your
system's tools, get it from http://gstreamer.freedesktop.org/src/gst-python/ .

Pyrana is written using a framework called feather
(https://github.com/jdodds/feather). The above dependencies can be removed
pretty easily if you don't want to use GTK or gstreamer, provided you write
something for displaying the UI and something for playing audio files. Take a
look at the source if you're interested.

Pyrana assumes that your music directory is arranged in a artist/album
heirarchy.Something like:

    music/
      Underpowered Umpires/
        Third Strike/
      Robby and the Revoltors/
        William S. Burroughs Was My Father/

CONFIGURING
-----------

Pyrana stores its configuration in ~/.config/pyrana/options.ini. The file looks
like this by default:

    [main]
    use_notify: true
    update_pidgin_status: true
    
    [playlist]
    music_directory: ~/music
    seen_file: ~/.config/pyrana/seen

The options under `[main]` aren't actually used at the moment, sorry. I'm still
catching up a bit from a major rewrite. `music_directory` should be
self-explanatory. `seen_file` is used by pyrana to ensure that albums that have
been played already aren't played again, you should be able to just ignore it.

CREDIT
------

Credit is due to Shel from http://kipdreaming.com for the sweet tray
icons. Thanks, Shel!


CONTACT
-------

Questions? Comments? Suggestions? Hate-mail? Hit me up at
jeremiah.dodds@gmail.com