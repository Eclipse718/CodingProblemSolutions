import pygame
from pygame.locals import *
import numpy as np

def mandelbrot(c, max_iter):
    z = np.zeros(c.shape, dtype=complex)
    output = np.full(c.shape, max_iter, dtype=int)
    for n in range(max_iter):
        mask = np.abs(z) <= 2
        if not np.any(mask):
            break
        output[mask] = n
        z[mask] = z[mask] * z[mask] + c[mask]
    return output

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))

pixel_size = 2
x_min, x_max, y_min, y_max = -2.5, 1.5, -2, 2
iter = 130

def update_mandelbrot_image():
    global img
    xx = np.linspace(x_min, x_max, width // pixel_size)
    yy = np.linspace(y_min, y_max, height // pixel_size) * 1j
    c = np.ravel(xx + yy[:, None]).reshape((height // pixel_size, width // pixel_size))
    iterations = mandelbrot(c, iter)
    img = np.repeat(np.repeat(iterations, pixel_size, axis=0), pixel_size, axis=1)
    img = (img * 255 / np.max(img)).astype(np.uint8)

update_mandelbrot_image()

font = pygame.font.Font(None, 20)
running = True
is_dragging = False 
last_x, last_y = None, None

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            is_dragging = True
            last_x, last_y = event.pos
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            is_dragging = False
            last_x, last_y = None, None
        elif event.type == MOUSEMOTION and is_dragging:
            dy = (event.pos[0] - last_x) * (x_max - x_min) / width
            dx = (event.pos[1] - last_y) * (y_max - y_min) / height
            y_min -= dx
            y_max -= dx
            x_min -= dy
            x_max -= dy
            last_x, last_y = event.pos
            update_mandelbrot_image()
        elif event.type == MOUSEWHEEL:
            zoom_factor = 1.1 if event.y > 0 else 0.9
            mx, my = pygame.mouse.get_pos()
            focus_x = x_min + mx * (x_max - x_min) / width
            focus_y = y_min + my * (y_max - y_min) / height
            x_min = focus_x - (focus_x - x_min) * zoom_factor
            x_max = focus_x + (x_max - focus_x) * zoom_factor
            y_min = focus_y - (focus_y - y_min) * zoom_factor
            y_max = focus_y + (y_max - focus_y) * zoom_factor
            update_mandelbrot_image()

    screen.fill((0, 0, 0))
    
    # Render additional text
    zoom_level = round(width / (abs(x_max - x_min)), 2)
    mouse_x, mouse_y = pygame.mouse.get_pos()  # Get mouse position
    pixel_width = (x_max - x_min) / width
    pixel_height = (y_max - y_min) / height
    coord_real_part = x_min + mouse_x * pixel_width
    coord_imag_part = y_min + mouse_y * pixel_height
    
    text_zoom = font.render(f'Zoom Level: {zoom_level}X', True, (0, 0, 0))
    text_coords = font.render(f'Coord ({coord_real_part:.4f}, {coord_imag_part:.4f})', True, (0, 0, 0))
    

    
    surf = pygame.surfarray.make_surface(img.T)
    screen.blit(surf, (0, 0))
    screen.blit(text_zoom, (610, 10))
    screen.blit(text_coords, (610, 30))

    pygame.display.flip()

pygame.quit()
