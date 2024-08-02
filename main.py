import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Set up the drawing window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Drawing App")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Brush settings
brush_radius = 10

# Create a drawings folder if it doesn't exist
drawings_folder = "drawings"
if not os.path.exists(drawings_folder):
    os.makedirs(drawings_folder)

# Clear the drawings folder
for filename in os.listdir(drawings_folder):
    file_path = os.path.join(drawings_folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            os.rmdir(file_path)
    except Exception as e:
        print(f"Failed to delete {file_path}. Reason: {e}")

# Fill the screen with white
screen.fill(WHITE)
pygame.display.update()

# Function to draw a circle
def draw_circle(screen, color, position, radius):
    pygame.draw.circle(screen, color, position, radius)
    pygame.display.update()

# Function to interpolate points
def interpolate_points(p1, p2, num_points):
    return [(p1[0] + (p2[0] - p1[0]) * i / num_points, p1[1] + (p2[1] - p1[1]) * i / num_points) for i in range(num_points + 1)]

# Function to save the current drawing
def save_drawing(screen, counter):
    filename = f"{drawings_folder}/drawing_{counter}.png"
    pygame.image.save(screen, filename)

# Run until the user asks to quit
running = True
drawing = False
last_pos = None
stroke_counter = 0

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                drawing = True
                last_pos = event.pos
                draw_circle(screen, BLACK, last_pos, brush_radius)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                drawing = False
                # Save the current drawing
                save_drawing(screen, stroke_counter)
                stroke_counter += 1
                # Clear the screen
                screen.fill(WHITE)
                pygame.display.update()
                last_pos = None
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                current_pos = event.pos
                if last_pos:
                    distance = max(abs(current_pos[0] - last_pos[0]), abs(current_pos[1] - last_pos[1]))
                    if distance == 0:
                        num_points = 1
                    else:
                        num_points = max(1, int(distance / (brush_radius / 2)))
                    
                    # Interpolate points between the last and current position
                    points = interpolate_points(last_pos, current_pos, num_points)
                    for point in points:
                        draw_circle(screen, BLACK, (int(point[0]), int(point[1])), brush_radius)
                last_pos = current_pos

# Quit Pygame
pygame.quit()
sys.exit()
