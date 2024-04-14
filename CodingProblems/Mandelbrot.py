import pygame
from pygame.locals import *
import numpy as np
import numba as nb

@nb.njit(parallel=True)
def mandelbrot(c, max_iter):
    output = np.empty(c.shape, dtype=np.int32)
    for i in nb.prange(c.shape[0]):
        for j in nb.prange(c.shape[1]):
            z = c[i, j]
            for n in range(max_iter):
                if abs(z) > 2:
                    output[i, j] = n
                    break
                z = z * z + c[i, j]
            else:
                output[i, j] = max_iter
    return output


'''
The below are functions that use fastmath to improve runtime, but they come at a tradeoff of accuracy
The check discrepancy function compares the fastmath discrepancies to the regular calculation to give the percentage of mistakes
and the magnitude of those mistakes due to fastmath
-
The summary is that at low zoom levels there are fewer discrepant calculations at higher magnitudes (average ~33 difference)
At higher zoom levels there are many more discrepancies (about 20% at max pixels are discrepant) but those discrepancies are 
smaller on average (~3)

I've decided to just reduce the iteration count and not use fastmath for the default
Uncomment the functions and the useage in the update image function to have it print the discrepancies
'''

'''
@nb.njit(parallel=True, fastmath=True)
def mandelbrot_fastmath(c, max_iter):
    output = np.empty(c.shape, dtype=np.int32)
    for i in nb.prange(c.shape[0]):
        for j in nb.prange(c.shape[1]):
            z = c[i, j]
            for n in range(max_iter):
                if abs(z) > 2:
                    output[i, j] = n
                    break
                z = z * z + c[i, j]
            else:
                output[i, j] = max_iter
    return output

def check_discrepancy(c, max_iter):
    output = mandelbrot(c, max_iter)
    output_fastmath = mandelbrot_fastmath(c, max_iter)
    discrepancy = np.sum(output != output_fastmath)
    total_calculations = output.size
    percentage_discrepancy = (discrepancy / total_calculations) * 100
    avg_magnitude_discrepancy = np.mean(np.abs(output[output != output_fastmath] - output_fastmath[output != output_fastmath]))
    return discrepancy, percentage_discrepancy, avg_magnitude_discrepancy
'''

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))

pixel_size = 1
x_min, x_max, y_min, y_max = -2.5, 1.5, -2, 2
iter = 900

def generate_color_palette(max_iter):
    import numpy as np
    palette = np.zeros((max_iter + 1, 3), dtype=np.uint8)

    # Handle the first 16 iterations with shades of blue
    for i in range(16):
        # Gradually increase the intensity of the blue
        blue = int(20 + i * (240 / 10))  # Start from very dark and increase
        palette[i] = (i*10, i*10, blue)

    # For the rest of the palette, transition through vibrant colors
    for i in range(16, max_iter):
        red = int((np.sin(i * 0.1) * 127.5) + 127.5)
        green = int((np.sin(i * 0.15 + 2) * 127.5) + 127.5)
        blue = int((np.sin(i * 0.2 + 4) * 127.5) + 127.5)
        palette[i] = (red, green, blue)

    return palette



palette = generate_color_palette(iter)  # Generate the palette once

def generate_image(c, max_iter):
    iterations = mandelbrot(c, max_iter)
    image = palette[iterations]  # Map the iterations directly to colors
    return image

def update_mandelbrot_image():
    global img
    xx = np.linspace(x_min, x_max, width // pixel_size)
    yy = np.linspace(y_min, y_max, height // pixel_size) * 1j
    c = xx[:, None] + yy
    img = generate_image(c, iter)
    img = np.repeat(np.repeat(img, pixel_size, axis=0), pixel_size, axis=1)
    '''
    discrepancy, percentage_discrepancy, avg_magnitude_discrepancy = check_discrepancy(c, iter)
    print("Discrepancy:", discrepancy)
    print("Percentage Discrepancy:", percentage_discrepancy)
    print("Average Magnitude of Discrepancies:", avg_magnitude_discrepancy)
    '''

update_mandelbrot_image()

font = pygame.font.Font(None, 20)
running = True
is_dragging = False 
last_x, last_y = None, None

def draw_mandelbrot_path(screen, c, iter, x_min, x_max, y_min, y_max, width, height):
    z = np.zeros(c.shape, dtype=np.complex128)
    prev_x, prev_y = None, None

    def on_screen(x, y):
        return 0 <= x < width and 0 <= y < height

    for i in range(iter):
        z = z * z + c
        if not np.isfinite(z).all():
            break

        real_part = (z.real - x_min) / (x_max - x_min) * width
        imag_part = (z.imag - y_min) / (y_max - y_min) * height

        if not np.isfinite(real_part) or not np.isfinite(imag_part):
            continue  # Skip iteration if the coordinates are not finite

        x, y = int(real_part), int(imag_part)

        if prev_x is not None and prev_y is not None:
            if on_screen(x, y) and on_screen(prev_x, prev_y):
                pygame.draw.line(screen, (255, 255, 255), (prev_x, prev_y), (x, y), 1)
            else:
                if not (on_screen(x, y) or on_screen(prev_x, prev_y)):
                    continue
                else:
                    clamped_prev_x = min(max(prev_x, 0), width - 1)
                    clamped_prev_y = min(max(prev_y, 0), height - 1)
                    clamped_x = min(max(x, 0), width - 1)
                    clamped_y = min(max(y, 0), height - 1)
                    pygame.draw.line(screen, (255, 255, 255), (clamped_prev_x, clamped_prev_y), (clamped_x, clamped_y), 1)

        prev_x, prev_y = x, y

        if np.abs(z) > 2:
            break
        
def zoom_to_julia_island():
    global x_min, x_max, y_min, y_max
    julia_island_x = -1.76877883727888
    julia_island_y = -0.00173898653183
    target_zoom = 862162921902
    
    x_min = -1.76877883670268
    x_max = -1.76877883656601
    y_min = -0.00173898590092
    y_max = -0.00173898598867
    
    update_mandelbrot_image()
    pygame.display.flip()






is_drawing_path = False
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
            dx = (event.pos[0] - last_x) * (x_max - x_min) / width
            dy = (event.pos[1] - last_y) * (y_max - y_min) / height
            x_min -= dx
            x_max -= dx
            y_min -= dy
            y_max -= dy
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
        elif event.type == MOUSEBUTTONDOWN and event.button == 3:
            is_drawing_path = True
        elif event.type == MOUSEBUTTONUP and event.button == 3:
            is_drawing_path = False
        elif event.type == KEYDOWN:
            if event.key == K_j:
                zoom_to_julia_island()

    screen.fill((0, 0, 0))
    surf = pygame.surfarray.make_surface(img)
    screen.blit(surf, (0, 0))
    
    zoom_level = round(width / (abs(x_max - x_min)), 2)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pixel_width = (x_max - x_min) / width
    pixel_height = (y_max - y_min) / height
    coord_real_part = x_min + mouse_x * pixel_width
    coord_imag_part = y_min + mouse_y * pixel_height

    iterations = mandelbrot(np.array([[coord_real_part + coord_imag_part * 1j]]), iter)[0][0]
    if iterations == iter:
        escape_time = "Never"
    else:
        escape_time = str(iterations)
    
    if zoom_level > 1000000:
        text_zoom = font.render(f'Zoom Level: {zoom_level}X', True, (0, 0, 0))
        text_coords = font.render(f'Coord ({coord_real_part:.14f}, {coord_imag_part:.14f})', True, (0, 0, 0))
        text_escape = font.render(f'Escape Time: {escape_time}', True, (0, 0, 0))
        screen.blit(text_zoom, (570, 10))
        screen.blit(text_coords, (500, 30))
        screen.blit(text_escape, (570, 50))
    
    else:

        text_zoom = font.render(f'Zoom Level: {zoom_level}X', True, (255, 255, 255))
        text_coords = font.render(f'Coord ({coord_real_part:.4f}, {coord_imag_part:.4f})', True, (255, 255, 255))
        text_escape = font.render(f'Escape Time: {escape_time}', True, (255, 255, 255))

        screen.blit(text_zoom, (610, 10))
        screen.blit(text_coords, (610, 30))
        screen.blit(text_escape, (610, 50))
        
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pixel_width = (x_max - x_min) / width
    pixel_height = (y_max - y_min) / height
    coord_real_part = x_min + mouse_x * pixel_width
    coord_imag_part = y_min + mouse_y * pixel_height

    c = np.array([[coord_real_part + coord_imag_part * 1j]])
    if(is_drawing_path):
        draw_mandelbrot_path(screen, c, iter, x_min, x_max, y_min, y_max, width, height)
    
    
    pygame.display.flip()

pygame.quit()
