import pygame

def adjustBrightness(color, value):
    r = max(0, min(255, color[0] + value))
    g = max(0, min(255, color[1] + value))
    b = max(0, min(255, color[2] + value))

    return (r, g, b)

def create_brick(width, height, color) -> pygame.Surface:
    surface = pygame.Surface((width, height))
    surface.fill(color)
    highlight = adjustBrightness(color, 150)
    pygame.draw.line(surface, highlight, (0,0), (0, height), 5)
    pygame.draw.line(surface, highlight, (0,0), (width, 0), 5)
    shadow = adjustBrightness(color, -150)
    pygame.draw.line(surface, shadow, (0, height), (width, height), 5)
    pygame.draw.line(surface, shadow, (width, 0), (width, height), 5)
    return surface