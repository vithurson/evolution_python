import pygame
import random

# ----- Configuration -----
GRID_SIZE = 50           # 50x50 grid
CELL_SIZE = 10           # Each cell is 10x10 pixels (window: 500x500)
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
NUM_FOODS = 10
NUM_CREATURES = 10
FPS = 30                 # Frames per second
DAY_LENGTH_FRAMES = 300  # A day lasts 300 frames

# Colors (R, G, B)
WHITE = (255, 255, 255)
GRAY  = (200, 200, 200)
GREEN = (0, 255, 0)      # Food color
RED   = (255, 0, 0)      # Creature color

# ----- Pygame Initialization -----
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Pure Random Strategy Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# ----- Global Variables -----
foods = []        # List of food positions as (x, y) tuples.
creatures = []    # List of creature dictionaries.
# Each creature is represented as:
#   {
#       'x': int, 'y': int,         # current grid position
#       'state': 'roaming' or 'waiting',
#       'ate': bool                 # whether it has eaten during this day
#   }
frame_counter = 0
day_count = 1

# ----- Utility Functions -----
def random_edge_position():
    """Return a random position along one of the four grid edges."""
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    if edge == 'top':
        return (random.randint(0, GRID_SIZE - 1), 0)
    elif edge == 'bottom':
        return (random.randint(0, GRID_SIZE - 1), GRID_SIZE - 1)
    elif edge == 'left':
        return (0, random.randint(0, GRID_SIZE - 1))
    else:  # 'right'
        return (GRID_SIZE - 1, random.randint(0, GRID_SIZE - 1))

def init_foods():
    """Place NUM_FOODS food items at random positions on the grid."""
    global foods
    foods = []
    while len(foods) < NUM_FOODS:
        pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if pos not in foods:
            foods.append(pos)

def init_creatures():
    """Initialize NUM_CREATURES creatures with random positions and set their state to 'roaming'."""
    global creatures
    creatures = []
    for _ in range(NUM_CREATURES):
        pos = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        creature = {'x': pos[0], 'y': pos[1], 'state': 'roaming', 'ate': False}
        creatures.append(creature)

# ----- Drawing Functions -----
def draw_grid():
    """Draw grid lines for visualization."""
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_SIZE))
    for y in range(0, WINDOW_SIZE, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOW_SIZE, y))

def draw_foods():
    """Draw each food item as a green square."""
    for food in foods:
        rect = pygame.Rect(food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, rect)

def draw_creatures():
    """Draw each creature as a red square."""
    for creature in creatures:
        rect = pygame.Rect(creature['x'] * CELL_SIZE, creature['y'] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, rect)

def draw_day_info():
    """Display current day, frame, and population info."""
    info = f"Day: {day_count}  Frame: {frame_counter}  Population: {len(creatures)}"
    text = font.render(info, True, (0, 0, 0))
    screen.blit(text, (10, 10))

# ----- Simulation Update Functions -----
def update_creatures():
    """
    For each roaming creature, move one random step.
    If a creature lands on a cell containing food, it eats the food,
    is repositioned to a random edge, and stops moving for the day.
    """
    global foods
    for creature in creatures:
        if creature['state'] != 'roaming':
            continue  # Skip creature if it already ate this day.

        # Choose a random movement: up, down, left, right, or no movement.
        dx, dy = random.choice([(1,0), (-1,0), (0,1), (0,-1), (0,0)])
        new_x = creature['x'] + dx
        new_y = creature['y'] + dy

        # Ensure new position is within grid bounds.
        if 0 <= new_x < GRID_SIZE:
            creature['x'] = new_x
        if 0 <= new_y < GRID_SIZE:
            creature['y'] = new_y

        # Check if there's food at the creature's new position.
        pos = (creature['x'], creature['y'])
        if pos in foods:
            foods.remove(pos)
            creature['ate'] = True
            creature['state'] = 'waiting'
            # Reposition creature to a random edge.
            creature['x'], creature['y'] = random_edge_position()

def end_of_day():
    """
    At the end of the day (after 300 frames):
      - Remove creatures that did not eat (still 'roaming').
      - Reset survivors (those that ate) to 'roaming' for the next day.
      - Generate new food.
    """
    global creatures, frame_counter, day_count
    # Keep only creatures that ate.
    survivors = [creature for creature in creatures if creature['ate']]
    # Reset survivors for the new day.
    for creature in survivors:
        creature['state'] = 'roaming'
        creature['ate'] = False
        creature['x'], creature['y'] = random_edge_position()  # reposition at the edge
    creatures = survivors

    init_foods()      # Generate new food.
    frame_counter = 0 # Reset the day counter.
    day_count += 1

# ----- Main Simulation Loop -----
def main():
    global frame_counter
    init_foods()
    init_creatures()
    running = True

    while running:
        clock.tick(FPS)
        frame_counter += 1

        # Event handling.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update creature positions.
        update_creatures()

        # End the day if the frame limit is reached.
        if frame_counter >= DAY_LENGTH_FRAMES:
            end_of_day()

        # Drawing.
        screen.fill(WHITE)
        draw_grid()
        draw_foods()
        draw_creatures()
        draw_day_info()
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()

