import pygame
from pygame.sprite import Sprite
from util import cargar_imagen

class Boom(Sprite):
    """
    Sprite de explosión.
    Se activa al explotar una bomba, mostrando la imagen boom.
    """
    def __init__(self, x, y):
        super().__init__()
        self.image, self.rect = cargar_imagen('boom2.png', -1)
        self.rect.center = (x, y)
        self.timer = 25  # Duración de la explosión en frames

    def update(self):
        # Reduce el timer, elimina el sprite cuando se acaba el tiempo
        self.timer -= 1
        if self.timer <= 0:
            self.kill()  # Elimina este sprite del grupo
