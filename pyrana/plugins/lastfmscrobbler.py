import pylast

from feather import Plugin

class LastFmScrobbler(Plugin):
    listeners = set(['songstart', 'songend', 'metadataread'])
    messengers = set()

    API_KEY = 'fd0c0272688b807631f12d91ce6d3afb'
    SECRET = 'fb1f796931a24717dd2ac8e1f4789912'
    CLIENT_ID = 'tst'
    CLIENT_VERSION = 1.0

    def __init__(self, username, password) :
        super(LastFmScrobbler, self).__init__()
        self.username = username
        self.password_hash = pylast.md5(password)
        self.network = pylast.LastFMNetwork(
            api_key = self.API_KEY,
            api_secret = self.SECRET,
            username = self.username,
            password_hash = self.password_hash
        )


    def songstart(self, payload=None):
        from time import time
        self.started_at = int(time())

    def metadataread(self, payload):
        self.metadata = payload

    def songend(self, payload=None):
        self.network.scrobble(
            self.metadata['artist'][0],
            self.metadata['title'][0],
            self.started_at,
            self.metadata['album'][0]
        )
