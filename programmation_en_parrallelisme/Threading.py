# -*- coding: utf8 -*-
import random
import sys
import time
from threading import Thread, RLock

verrouillage = RLock()

class Fonctionalites(Thread):
    """Thread chargé de recup et afficher un elm des liste dans laconsole."""

    def __init__(self, timedivisor):
        Thread.__init__(self)
        self.value = timedivisor

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        i = 0
        while i < 20:
            with verrouillage: # bloque l'acces au ressource pour eviter les conflits
                attente = 0.2
                attente += random.randint(1, 60) / self.value
                time.sleep(attente)
                print 'Test '+str(i)
                i += 1
            #debloqué

if __name__ == '__main__':
    # Création des threads
    thread_1 = Fonctionalites(10)
    thread_2 = Fonctionalites(100)

    # Lancement des threads et poursuite du script
    thread_1.start()
    thread_2.start()

    # Attend que les threads se terminent(bloquent le script)
    thread_1.join()
    thread_2.join()
