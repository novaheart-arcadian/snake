import pygame
import economia

pygame.init()

FONT = pygame.font.SysFont("Arial", 28)
SMALL = pygame.font.SysFont("Arial", 22)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)
DARK = (25, 25, 25)
GREEN = (0, 255, 0)
RED = (255, 80, 80)
GOLD = (255, 215, 0)


class Button:
    def __init__(self, x, y, w, h, text, color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
        t = SMALL.render(self.text, True, self.text_color)
        screen.blit(t, (self.rect.x + 10, self.rect.y + 8))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


def pantalla_tienda(screen, data):
    clock = pygame.time.Clock()

    scroll = 0
    running = True

    while running:
        screen.fill(DARK)

        # COINS DISPLAY
        coins_text = FONT.render(f"Monedas: {data['coins']}", True, GOLD)
        screen.blit(coins_text, (20, 20))

        y = 100 + scroll
        buttons = []

        # LISTA DE SKINS
        for skin_name, info in economia.SKINS.items():

            # Fondo del bloque
            pygame.draw.rect(screen, GRAY, (50, y, 500, 100), border_radius=15)

            # Nombre de skin
            name_text = SMALL.render(skin_name.upper(), True, WHITE)
            screen.blit(name_text, (70, y + 10))

            # Cuadrado color
            pygame.draw.rect(screen, info["color"], (70, y + 50, 40, 40))

            # Owned?
            if skin_name in data["owned_skins"]:
                btn = Button(400, y + 30, 120, 40, "EQUIPAR", GREEN)

            else:
                price = info["price"]
                btn = Button(400, y + 30, 120, 40, f"{price} $", RED)

            btn.draw(screen)
            buttons.append((btn, skin_name))

            y += 130

        # Botón de salida
        exit_btn = Button(600, 20, 140, 40, "SALIR", RED)
        exit_btn.draw(screen)

        # EVENTOS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # scroll hacia arriba
                    scroll += 40
                if event.button == 5:  # scroll hacia abajo
                    scroll -= 40

                if exit_btn.clicked(event.pos):
                    return

                # CLICK EN BOTONES DE SKINS
                for btn, skin_name in buttons:
                    if btn.clicked(event.pos):

                        # Comprar o equipar
                        if skin_name in data["owned_skins"]:
                            resultado = economia.equip_skin(data, skin_name)
                        else:
                            resultado = economia.buy_skin(data, skin_name)

                        # Mensaje emergente simple
                        popup(screen, resultado)

        pygame.display.flip()
        clock.tick(60)


def popup(screen, message):
    """Pequeño cuadro de aviso."""
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    box = pygame.Rect(150, 200, 500, 200)
    pygame.draw.rect(screen, GRAY, box, border_radius=20)

    text = FONT.render(message, True, WHITE)
    screen.blit(text, (box.x + 40, box.y + 80))

    pygame.display.flip()
    pygame.time.wait(1400)
