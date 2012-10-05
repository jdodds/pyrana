from feather import Plugin

class MetadataReader(Plugin):
    listeners = set(['songstart'])
    messengers = set(['metadataread'])

    def songstart(self, payload):
        import mutagen
        info = mutagen.File(payload, easy=True)
        self.send('metadataread', dict(info))
