import pygame.event
import pygame.mixer
import pygame.display
import threading
import time

from feather import Plugin

ENDEVENT=42

class PyGamePlayer(Plugin):
    listeners = set(['songloaded', 'pause', 'skipsong', 'skipalbum'])
    messengers = set(['songstart', 'songpause', 'songend', 'songresume'])

    def run(self):
        pygame.display.init()
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(ENDEVENT)
        t = threading.Thread(target=self._songend_bubble, args=(self,))
        t.daemon = True
        t.start()

        message_funcs = {
            'songloaded': self.handle_songloaded,
            'pause' : self.handle_pause,
            'skipsong' : self.handle_skipsong,
            'skipalbum' : self.handle_skipalbum,
            'SHUTDOWN' : self.shutdown}
        
        while self.alive:
            message, payload = self.listener.get()
            message_funcs[message](payload)

    def _songend_bubble(s,self):
        while self.alive:
            event = pygame.event.get(ENDEVENT)
            if event:
                print event
                self.send('songend')
            else:
                time.sleep(0.1)
                
        print 'done'
                
    def handle_songloaded(self, payload):
        try:
            pygame.mixer.music.load(payload)
        except :
            pass
        pygame.mixer.music.play()
        self.playing = True
        self.send('songstart', payload)

    def handle_pause(self, payload=None):
        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False
            self.send('songpause')
        else:
            pygame.mixer.music.unpause()
            self.playing = True
            self.send('songresume')

    def handle_skipsong(self, payload=None):
        pygame.mixer.music.stop()

    def handle_skipalbum(self, payload=None):
        pygame.mixer.music.stop()
            
    
        

