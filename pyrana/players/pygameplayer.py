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
    name = 'PyGamePlayer'

    def pre_run(self):
        pygame.display.init()
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(ENDEVENT)
        t = threading.Thread(target=self._songend_bubble, args=(self,))
        t.daemon = True
        t.start()

    def _songend_bubble(s,self):
        while self.runnable:
            event = pygame.event.get(ENDEVENT)
            if event:
                self.send('songend')
            else:
                time.sleep(0.1)
                
    def songloaded(self, payload):
        try:
            pygame.mixer.music.load(payload)
        except :
            pass
        pygame.mixer.music.play()
        self.playing = True
        self.send('songstart', payload)

    def pause(self, payload=None):
        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False
            self.send('songpause')
        else:
            pygame.mixer.music.unpause()
            self.playing = True
            self.send('songresume')

    def skipsong(self, payload=None):
        pygame.mixer.music.stop()

    def skipalbum(self, payload=None):
        pygame.mixer.music.stop()
            
    
        

