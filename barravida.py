import pygame

class BarraVida():
    """
    Clase para mostrar una barra de vida horizontal.
    x, y: posición de inicio
    colorvida: color del relleno de vida (tupla RGB)
    colorlinea: color del borde de la barra (tupla RGB)
    alto: altura de la barra (int)
    ancho: ancho máximo de la barra (int)
    """
    def __init__(self, x, y, colorvida, colorlinea, alto, ancho):
        self.x = x
        self.y = y
        self.colorvida = colorvida
        self.colorlinea = colorlinea
        self.ancho = ancho
        self.alto = alto
        
    def update(self):
        pass  # Para compatibilidad, no se usa

    def imprimir(self, screen, vida):
        """
        Dibuja la barra de vida sobre la superficie 'screen'
        vida: ancho de la vida actual (de 0 a self.ancho)
        """
        # Borde de la barra
        pygame.draw.rect(screen, self.colorlinea, (self.x-2, self.y-16, self.ancho+4, self.alto+3), 2)
        # Relleno (barra de vida actual)
        pygame.draw.line(screen, self.colorvida, (self.x, self.y), (self.x + vida, self.y), self.alto)

# Ejemplo de uso (comentar en integración final):
# if __name__ == '__main__':
#     pygame.init()
#     screen = pygame.display.set_mode((300, 60))
#     vida = BarraVida(10, 20, (255, 0, 0), (255, 255, 255), 30, 200)
#     vida_actual = 200
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#         screen.fill((0,0,0))
#         vida.imprimir(screen, vida_actual)
#         pygame.display.flip()
#     pygame.quit()
