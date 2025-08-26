import pygame
import random

# pygame setup
pygame.init()

width, height = 800, 600
grid_size = 20
cell_size = width // grid_size
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Candy Crush Lite")
clock = pygame.time.Clock()
running = True

COLORS = {
    1: (255, 0, 0),     #red
    2: (0, 255, 0),     #green
    3: (0, 0, 255),     #blue
    4: (255, 255, 0)    #yellow
}

def create_candy():
    return random.randint(1, 4) #4 types of candies


grid = [[create_candy() for _ in range(grid_size)] for _ in range(grid_size)]
selected_candy = None


def read_candy(row, col):
    return grid[row][col] 

def update_candy(row, col, candy_type):
    grid[row][col] = candy_type

def delete_candy(row,col):
    grid[row][col] = 0 

def handle_click(row, col):
    global selected_candy
    if selected_candy is None:
        selected_candy = (row, col)
    else:
        r1, c1 = selected_candy
        grid[row][col], grid[r1][c1] = grid[r1][c1], grid[row][col]
        selected_candy = None
   
def detect_matches():
    matches = set()
    
    #check horizontal matches
    for row in range(grid_size):
        for col in range(grid_size - 2):
            if grid[row][col] ==grid[row][col + 1 ] == grid[row][col + 2] != 0:
                matches.update({(row, col), (row, col + 1), (row, col + 2)})
       #check vertical matches      
    for col in range(grid_size):
        for row in range(grid_size - 2):
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col] != 0:
                matches.update({(row, col), (row + 1, col), (row + 2, col)})   
    return matches 

# main game loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = x // cell_size
            row = y // cell_size
            handle_click(row, col)  

    screen.fill(("purple"))  # fill the screen with purple

    #check foor matches
    matches = detect_matches()
    if matches:
        for row, col in matches:
            delete_candy(row, col)


    #draw the candies
    for row in range(grid_size):
        for col in range(grid_size):
            candy_type = read_candy(row, col)
            if candy_type !=0:
                candy_color = COLORS[candy_type]
                pygame.draw.rect(screen, candy_color,
                                (col * cell_size, row * cell_size, cell_size - 2, cell_size - 2))


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()