import pygame
import pygame_gui
import math
import time

def josephus_elimination_order(n, k):
    order = []
    index = 0  # Starting index for elimination
    for remaining in range(n, 1, -1):  # Loop until one remains
        index = (index + k - 1) % remaining
        order.append(index)
    return order

def main():
    pygame.init()
    pygame.display.set_caption('Josephus Problem Visualization')
    
    screen = pygame.display.set_mode((800, 800))
    manager = pygame_gui.UIManager((800, 800))
    
    # GUI Elements
    start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 10), (90, 50)), text='Start', manager=manager)
    n_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((20, 20), (150, 20)), start_value=50, value_range=(2, 100), manager=manager)
    k_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((20, 50), (150, 20)), start_value=10, value_range=(1, 50), manager=manager)
    n_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((180, 20), (100, 20)), text='n: 50', manager=manager)
    k_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((180, 50), (100, 20)), text='k: 10', manager=manager)
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 20)
    
    running = True
    simulation_started = False
    n = int(n_slider.get_current_value())
    k = int(k_slider.get_current_value())
    positions, label_positions, colors = prepare_positions_labels_colors(n)

    while running:
        time_delta = clock.tick(60)/1000.0
        n_value = int(n_slider.get_current_value())
        k_value = int(k_slider.get_current_value())
        n_label.set_text(f'n: {n_value}')
        k_label.set_text(f'k: {k_value}')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    simulation_started = True
                    n = n_value
                    k = k_value
                    elimination_order = josephus_elimination_order(n, k)
                    eliminated = []
                    positions, label_positions, colors = prepare_positions_labels_colors(n)
            
            manager.process_events(event)
        
        manager.update(time_delta)
        
        screen.fill((255, 255, 255))  # Clear screen

        # Draw circles and labels
        draw_circles_labels(screen, font, positions, label_positions, colors, [], n)
        
        if simulation_started:
            draw_circles_labels(screen, font, positions, label_positions, colors, eliminated, n)
            handle_elimination(eliminated, elimination_order, n)
        
        manager.draw_ui(screen)
        
        pygame.display.flip()
    
    pygame.quit()

def prepare_positions_labels_colors(n):
    radius = 250  # Radius for circle of people
    label_radius = radius + 30  # Slightly higher radius for labels
    positions = [(400 + math.cos(2 * math.pi / n * x) * radius, 400 + math.sin(2 * math.pi / n * x) * radius) for x in range(n)]
    label_positions = [(400 + math.cos(2 * math.pi / n * x) * label_radius, 400 + math.sin(2 * math.pi / n * x) * label_radius) for x in range(n)]
    colors = [(0, 0, 0) for _ in range(n)]  # Start with all black
    return positions, label_positions, colors

def draw_circles_labels(screen, font, positions, label_positions, colors, eliminated, n):
    for i, (pos, label_pos) in enumerate(zip(positions, label_positions)):
        # Determine the color of the dot
        if i in eliminated:
            color = (255, 0, 0)  # Red for eliminated
        elif len(eliminated) == n - 1 and i not in eliminated:
            color = (0, 255, 0)  # Green for the last remaining dot
        else:
            color = (0, 0, 0)  # Black for others

        pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), 10)
        text_surface = font.render(str(i + 1), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(int(label_pos[0]), int(label_pos[1])))
        screen.blit(text_surface, text_rect)


def handle_elimination(eliminated, elimination_order, n):
    if len(eliminated) < n - 1 and elimination_order:  # Continue until one is left
        eliminated_index = elimination_order.pop(0)
        # Adjust for already eliminated positions
        for e in sorted(eliminated):
            if eliminated_index >= e:
                eliminated_index += 1
        eliminated.append(eliminated_index)
        time.sleep(0.1)  # Delay 

if __name__ == '__main__':
    main()
