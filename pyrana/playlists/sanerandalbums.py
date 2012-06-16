import os, random, pickle
from md5 import md5

from feather import Plugin

class SaneRandomAlbums(Plugin):
    listeners = set(['play', 'skipsong', 'skipalbum', 'albumstart', 'albumend', 'songend'])
    messengers = set(['songloaded', 'albumstart', 'albumend'])
    name = 'SaneRandomAlbums'

    audio_types = set(['.mp3', '.m4a', '.ogg'])

    def __init__(self, musicdir, seen_file):
        super(SaneRandomAlbums, self).__init__()
        # give us a list of sets of albums by artists, assuming the directory
        # structure:
        #   Artists
        #    Albums
        #     Songs
        #This is a little ugly, but whatever.
        root = os.path.expanduser(musicdir)
        artistdata = [[os.path.join(artist, album)
                       for album in os.listdir(artist)
                       if os.path.isdir(os.path.join(artist, album))]
                      for artist in
                      [os.path.join(root, artistname)
                       for artistname in os.listdir(root)
                       if os.path.isdir(os.path.join(root, artistname))]]
        self.artistdata = filter(None, artistdata)
        self.last_artist = self.current_artist = None
        self.seen_file = seen_file
        self.__init_seen()

    def __init_seen(self):
        self.seen_file = os.path.expanduser(self.seen_file)
        if os.path.exists(self.seen_file):
            self.seen = pickle.load(open(self.seen_file, 'r'))
        else:
            self.seen = {}
        self.current_album_hash = None

    def next_album_path(self):
        while self.current_artist == self.last_artist:
            self.current_artist = random.choice(self.artistdata)
        self.last_artist = self.current_artist

        if len(self.current_artist) == 0:
            return self.next_album_path()
        return self.current_artist.pop(
            random.randrange(len(self.current_artist)))

    def next_album(self, payload):

        album_path = self.next_album_path()


        album_hash = md5(album_path).hexdigest()

        while album_hash in self.seen and len(self.current_artist) > 0:
            album_path = self.current_artist.pop(
                random.randrange(len(self.current_artist)))
            album_hash = md5(album_path).hexdigest()
        if len(self.current_artist) == 0:
            self.next_album(payload)
        else:
            self.seen[self.current_album_hash] = True

            self.current_album_hash = album_hash

            self.current_album = sorted(
                [os.path.join(album_path, song)
                 for song in os.listdir(album_path)
                 if os.path.splitext(song)[-1] in self.audio_types])

            self.send('albumstart', album_path)
    play = next_album
    skipalbum = next_album
    albumend = next_album


    def next_song(self, payload):
        if len(self.current_album) == 0:
            self.write_seen_file()
            self.send('albumend')
        else:
            song = self.current_album[0]
            self.current_album = self.current_album[1:]
            self.send('songloaded', song)

    def write_seen_file(self):
        seen_file = open(self.seen_file, 'w')
        pickle.dump(self.seen, seen_file)
        seen_file.close()


    skipsong = next_song
    albumstart = next_song
    songend = next_song
