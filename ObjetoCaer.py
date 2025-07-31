import pygame
from pygame.sprite import Sprite
from util import cargar_imagen

import random

class Banana(Sprite):
    """
    Sprite de Banana que cae desde arriba a velocidad variable.
    """
    def __init__(self, velocidad):
        super().__init__()
        self.image, self.rect = cargar_imagen('banana.png', -1)
        self.rect.x = random.randint(20, 600)
        self.rect.y = -30  # Empieza fuera de pantalla
        self.velocidad = velocidad

    def update(self):
        self.rect.y += self.velocidad
        # Borra si sale de la pantalla (opcional)
        if self.rect.top > 480:
            self.kill()

class Bomba(Sprite):
    """
    Sprite de Bomba que cae desde arriba a velocidad variable.
    """
    def __init__(self, velocidad):
        super().__init__()
        self.image, self.rect = cargar_imagen('bomba1.png', -1)
        self.rect.x = random.randint(20, 600)
        self.rect.y = -30
        self.velocidad = velocidad

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > 480:
            self.kill()
