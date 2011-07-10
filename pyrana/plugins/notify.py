import pynotify
pynotify.init("Basics")

from feather import Plugin

class Notify(Plugin):
    listeners = set(['songloaded'])
    messengers = set()

    def songloaded(self, payload):
        msg = "Playing: %s" % payload
        notification = pynotify.Notification("Pyrana", msg)
        notification.show()

