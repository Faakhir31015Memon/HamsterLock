def rounded_label(surface, pygame, font, text, position, color, background, padding=(14, 8)):
    rendered = font.render(text, True, color)
    box = rendered.get_rect(center=position).inflate(padding[0] * 2, padding[1] * 2)
    pygame.draw.rect(surface, background, box, border_radius=box.height // 2)
    surface.blit(rendered, rendered.get_rect(center=box.center))


def lock_icon(surface, pygame, center, locked, color):
    x, y = center
    body = pygame.Rect(x - 18, y - 3, 36, 29)
    pygame.draw.rect(surface, color, body, border_radius=7)
    arc = pygame.Rect(x - 13, y - 23, 26, 31)
    pygame.draw.arc(surface, color, arc, 3.2, 6.2, 6)
    pygame.draw.circle(surface, (10, 15, 32), (x, y + 10), 4)
    pygame.draw.line(surface, (10, 15, 32), (x, y + 10), (x, y + 18), 3)
