from feather import Plugin

class Notify(Plugin):
    listeners = set(['songloaded'])
    messengers = set()

    def songloaded(self, payload):
        msg = "Playing: %s" % payload
        print(msg)

