import pygame
from pygame.sprite import Sprite
from util import cargar_imagen, cargar_sonido

class Mono(Sprite):
    """
    Sprite principal del mono jugador.
    Cambia de imagen según estado: normal, contento, pierde.
    Reacciona con sonidos y animaciones.
    Movimiento clásico: izquierda/derecha (puedes expandir a arriba/abajo).
    """
    def __init__(self):
        super().__init__()
        # Imágenes de estado
        self.normal, self.rect = cargar_imagen('mono.png', -1)
        self.contento, _ = cargar_imagen('mono_contento.png', -1)
        self.pierde, _ = cargar_imagen('mono_pierde.png', -1)
        self.image = self.normal

        # Sonidos
        self.sonido_risa = cargar_sonido('mono_risa.wav')
        self.sonido_grito = cargar_sonido('mono_grito.wav')

        # Timer para mostrar estado contento o pierde
        self.estado_contador = 0

        # Ajusta la posición inicial si quieres
        self.rect.centerx = 320
        self.rect.bottom = 420

        # Velocidad del mono
        self.velocidad = 7

    def risa(self):
        """Mono sonríe y suena, cambia a imagen contento."""
        self.image = self.contento
        if self.sonido_risa:
            self.sonido_risa.play()
        self.estado_contador = 20  # frames que dura contento

    def grito_perder(self):
        """Mono pierde y suena, cambia a imagen de perder."""
        self.image = self.pierde
        if self.sonido_grito:
            self.sonido_grito.play()
        self.estado_contador = 40  # frames que dura triste

    def update(self):
        """Gestiona el cambio de imagen al terminar el estado especial y el movimiento."""
        # Movimiento clásico con flechas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidad
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidad

        # Limitar dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 640:
            self.rect.right = 640
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 480:
            self.rect.bottom = 480

        # Volver a estado normal si terminó la animación especial
        if self.estado_contador > 0:
            self.estado_contador -= 1
            if self.estado_contador == 0:
                self.image = self.normal

