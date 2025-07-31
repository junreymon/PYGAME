import pygame
import os

def cargar_imagen(name: str, transparente: bool):
    """
    Carga una imagen desde ./datos/ y la convierte si es necesario.
    Si 'transparente' es True, mantiene canal alpha.
    Retorna: (surface, rect)
    """
    fullname = os.path.join('./datos/', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print(f"Imposible cargar imagen {fullname}: {message}")
        raise SystemExit(message)
    if transparente:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image, image.get_rect()

def cargar_sonido(name: str):
    """
    Carga un sonido desde ./datos/.
    Retorna un objeto Sound, o un mock si mixer no está inicializado.
    """
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('./datos/', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print(f"No se pudo cargar el sonido {fullname}: {message}")
        raise SystemExit(message)
    return sound

def texto(color, texto, fuente, posx, posy):
    """
    Renderiza un texto usando una fuente, color y posición.
    Retorna: (surface, rect)
    """
    text_surface = fuente.render(str(texto), True, color)
    text_rect = text_surface.get_rect()
    text_rect.left, text_rect.top = (posx, posy)
    return text_surface, text_rect
