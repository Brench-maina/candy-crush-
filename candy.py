import pygame
import random


# pygame setup
pygame.init()

width, height = 800, 800
grid_size = 10
cell_size = width // grid_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Candy Crush Lite")
clock = pygame.time.Clock()
running = True

def load_image(filename):
    image = pygame.image.load(f"images/{filename}").convert_alpha()
    return pygame.transform.scale(image, (cell_size - 2, cell_size - 2))

IMAGES = {
    1: load_image("blueCandy.png"),
    2: load_image("orangeCandy.png"),
    3: load_image("purpleCandy.png"),
    4: load_image("redCandy.png"),
}

def create_candy():
    return random.randint(1, 4) #4 types of candies




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
        if detect_matches():
            pass
        else:
            pygame.display.flip()
            pygame.time.delay(500)
            grid[row][col], grid[r1][c1] = grid[r1][c1], grid[row][col]
        selected_candy = None
   
def detect_matches():
    matches = set()
    
    
    # check horizontal matches
    for row in range(grid_size):
        for col in range(grid_size - 2):
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2] != 0:
                matches.update({(row, col), (row, col + 1), (row, col + 2)})

    # check vertical matches      
    for col in range(grid_size):
        for row in range(grid_size - 2):
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col] != 0:
                matches.update({(row, col), (row + 1, col), (row + 2, col)})   

    return matches
    

def collapse_grid():
    for col in range(grid_size):
        for row in range(grid_size - 1, -1, -1):
            if grid[row][col] == 0: # if empty
                for above in range(row -1, -1, -1):
                    if grid[above][col] != 0:
                        grid[row][col] = grid[above][col]
                        grid[above][col] = 0
                        break

                else: 
                    grid[row][col] = create_candy()   #adds a new candy  

grid = [[create_candy() for _ in range(grid_size)] for _ in range(grid_size)]
selected_candy = None
score = 0  # initial score  

while detect_matches():
        matches = detect_matches()
        for row, col in matches:
            delete_candy(row, col)
        collapse_grid()
                    

def has_moves_left():
    for row in range(grid_size):
        for col in range(grid_size):
            if col + 1 < grid_size:
                grid[row][col], grid[row][col +1] = grid[row][col + 1], grid[row][col]
                if detect_matches():
                    grid[row][col], grid[row][col +1] = grid[row][col + 1], grid[row][col]
                    return True
                grid[row][col], grid[row][col +1] = grid[row][col + 1], grid[row][col]
            if row + 1 < grid_size:
                grid[row][col], grid[row + 1][col] = grid[row + 1][col], grid[row][col]
                if detect_matches():
                    grid[row][col], grid[row + 1][col] = grid[row + 1][col], grid[row][col]
                    return True
                grid[row][col], grid[row + 1][col] = grid[row + 1][col], grid[row][col]

    return False

# menu
menu_height = 50
font = pygame.font.Font(None, 36)

# main game loop
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = x // cell_size
            row = (y - menu_height) // cell_size  #subtract menu height
            if row >= 0:  # ignore clicks on menu
                handle_click(row, col) 

    screen.fill("purple")  # fill the screen with purple

    # check for matches
    matches = detect_matches()
    if matches:
        score += 5 # increase score
        for row, col in matches:
            delete_candy(row, col)
        collapse_grid()

    # draw the candies
    for row in range(grid_size):
        for col in range(grid_size):
            candy_type = read_candy(row, col)
            if candy_type != 0:
                screen.blit(IMAGES[candy_type],
                            (col * cell_size, row * cell_size + menu_height))

    # draw menu background + score
    pygame.draw.rect(screen, (50,50,50), (0, 0, width, menu_height))   #menu background
    score_text = font.render(f"Score: {score}", True, (255, 255,255))
    screen.blit(score_text, (10, 10)) #draw score

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
