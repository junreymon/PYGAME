import pygame
from pygame.sprite import Sprite
from util import cargar_imagen, cargar_sonido

class Cazador(Sprite):
    """
    Sprite del cazador. Puede estar normal o celebrar (contento).
    Persigue al mono cada vez que se actualiza.
    """
    def __init__(self):
        super().__init__()
        # Cargar imágenes
        self.normal, self.rect = cargar_imagen('cazador.png', -1)
        self.contento, _ = cargar_imagen('cazador_contento.png', -1)
        self.image = self.normal
        # Cargar sonido
        self.sonido_risa = cargar_sonido('cazador_risa.wav')
        self.estado_contador = 0  # Frames restantes para estado contento

        # Posición inicial
        self.rect.x = 20
        self.rect.y = 400  # Ajusta según el fondo

        self.velocidad = 3  # Velocidad de persecución

    def risa(self):
        """Activa la animación y sonido de risa del cazador"""
        self.image = self.contento
        if self.sonido_risa:
            self.sonido_risa.play()
        self.estado_contador = 50

    def perseguir(self, mono):
        """
        Mueve al cazador un paso hacia el mono.
        Usa Manhattan (sin diagonales) o permite diagonal.
        """
        dx = mono.rect.x - self.rect.x
        dy = mono.rect.y - self.rect.y

        # Movimiento en x
        if abs(dx) > abs(dy):
            self.rect.x += self.velocidad if dx > 0 else -self.velocidad if dx < 0 else 0
        # Movimiento en y
        elif dy != 0:
            self.rect.y += self.velocidad if dy > 0 else -self.velocidad if dy < 0 else 0

        # Opcional: ajustar para no moverse más allá de la posición del mono
        if abs(dx) < self.velocidad:
            self.rect.x = mono.rect.x
        if abs(dy) < self.velocidad:
            self.rect.y = mono.rect.y

    def update(self, mono=None):
        """Gestiona el tiempo que el cazador está contento y lo mueve si hay mono."""
        if self.estado_contador > 0:
            self.estado_contador -= 1
            if self.estado_contador == 0:
                self.image = self.normal
        # Si se pasa el objeto mono, lo persigue
        if mono is not None:
            self.perseguir(mono)
