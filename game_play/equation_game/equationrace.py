import pygame
import time
import random
from sys import exit

pygame.init()
pygame.font.init()

# Constants
WIDTH, HEIGHT = 1200, 800
P_WIDTH, P_HEIGHT, P_VEL = 40, 60, 10
BLOCK_WIDTH, BLOCK_HEIGHT, BLOCK_VEL = 50, 50, 2
FONT = pygame.font.SysFont("comicsans", 30)
OPERATIONS_LIST = ["+", "-"]
# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Equation Race")
home_screen = pygame.transform.scale(pygame.image.load("landscape.jpg"), 
                                     (WIDTH, HEIGHT))



def draw_screen(player, elapsed_time, blocks, block_texts, heart_list, 
                equation, score):
    """Draws all game elements onto the screen."""
    screen.blit(home_screen, (0, 0))
    time_text = FONT.render(f"Time: {round(max(0, 60 - elapsed_time))}s", 1, "white")
    live_text = FONT.render("Lives:", 1, "white")
    bar = pygame.Rect(0,0, 1200, 60)
    
    pygame.draw.rect(screen, "black", bar)
    screen.blit(live_text, (900, 10))
    screen.blit(time_text, (10, 10))
    
    
    pygame.draw.rect(screen, "red", player)
    #draw blocks
    for i, block in enumerate(blocks):
        pygame.draw.rect(screen, "white", block)

        text_surface = FONT.render(block_texts[i], 1, "black")
        text_x = block.x + (BLOCK_WIDTH // 2 - text_surface.get_width() // 2)
        text_y = block.y + (BLOCK_HEIGHT // 2 - text_surface.get_height() // 2)
        screen.blit(text_surface, (text_x, text_y))
    #draw hearts
    for i, heart in enumerate(heart_list):
        screen.blit(heart, (i*60 + 960, 10))

    #draw equation 
    font_equation = FONT.render(equation, 1, "white")
    screen.blit(font_equation, (WIDTH//2 - font_equation.get_width()//2, 10))

    #draw score
    draw_score(score)
    pygame.display.update()
    
def draw_score(score):
    font_score = FONT.render(f"Score: {score}", 1, "white")
    screen.blit(font_score, (200, 10))

def handle_player_movement(keys, player):
    """Handles player movement based on key inputs."""
    if keys[pygame.K_LEFT] and player.x - P_VEL >= 0:
        player.x -= P_VEL
    if keys[pygame.K_RIGHT] and player.x + P_VEL + player.width <= WIDTH:
        player.x += P_VEL
    if keys[pygame.K_UP] and player.y - P_VEL >= 60:
        player.y -= P_VEL
    if keys[pygame.K_DOWN] and player.y + P_VEL + player.height <= HEIGHT:
        player.y += P_VEL

def spawn_blocks(blocks, blocks_text, block_add_increment, total, 
                 equation_start):
    """Spawns new falling blocks periodically."""
    correct_block_index = None
    if 5 < time.time() - equation_start < 7:
            correct_block_index = random.randint(0, 2)
    for i in range(3):
        while True: 
            block_x = random.randint(0, WIDTH - BLOCK_WIDTH)

            if all(abs
            (block_x - block.x) > BLOCK_WIDTH + 5 for block in blocks):
                break  
        block = pygame.Rect(block_x, -BLOCK_HEIGHT + 80, 
                            BLOCK_WIDTH, BLOCK_HEIGHT)
        if i == correct_block_index:
            block_text = str(total)
        else:
            block_text = str(random.randint(max(total - 10, 0), 
                                        total + 10))
        blocks_text.append(block_text)
        blocks.append(block)
    
    return max(300, block_add_increment - 25)


def update_blocks(blocks, blocks_text, player, total):
    """Updates block positions and checks for collisions."""
    hit = False
    correct = False
    block_remove = []
    for i in range(len(blocks)):
        blocks[i].y += BLOCK_VEL
        if blocks[i].y > HEIGHT:
            block_remove.append(i)
        elif blocks[i].colliderect(player):
            if int(blocks_text[i]) == total:
                correct = True
            block_remove.append(i)
            hit = True
            break
    for block_index in block_remove[::-1]:
        del blocks[block_index]
        del blocks_text[block_index]
    
    return (hit, correct)
    

def display_game_over(score, elapsed_time):
    """Displays the game over screen when all 3 lives are out"""
   
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 150))
    screen.blit(overlay, (0, 0))
    stat_text = FONT.render(f"You survived {elapsed_time // 1} seconds with a score of {score}", 1, "black")
    game_over_text = FONT.render("Press R to play again, E to exit", 1, "black")
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2,
                                  (HEIGHT // 2) + 100))
    screen.blit(stat_text, (WIDTH // 2 -stat_text.get_width() //2, 
                            (HEIGHT // 2) - 100))
    pygame.display.update()

def restart_quit():
    """Game action after displaying game over"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_e:
                    pygame.quit()
                    exit()
def new_equation():
    """Generates new equation."""
    rand_num1 = random.randint(0, 100)
    rand_num2 = random.randint(0, 100)
    rand_operation = random.randint(0,1)
    operation = OPERATIONS_LIST[rand_operation]
    if operation == "+":
        equation = f"{rand_num1} + {rand_num2}"
        total = rand_num1 + rand_num2
        return equation, total
    if operation == "-":
        if rand_num1 > rand_num2:
            equation = f"{rand_num1} - {rand_num2}"
            total = rand_num1 - rand_num2
            return equation, total
        elif rand_num1 < rand_num2:
            equation = f"{rand_num2} - {rand_num1}"
            total = rand_num2 - rand_num1
            return equation, total
        else:
            equation = f"{rand_num1} - {rand_num2}"
            total = rand_num1 - rand_num2
            return equation,total

def main():
    """Main game loop."""
    run = True
    player = pygame.Rect(200, HEIGHT - P_HEIGHT, P_WIDTH, P_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    block_add_increment = 2000
    block_count = 0
    blocks = []
    blocks_text = []
    
    heart = pygame.image.load("heart.png")
    heart_scaled = pygame.transform.scale(heart, (100, 50))
    heart_list = [heart_scaled for _ in range(3)]
    hit = False

    #music
    pygame.mixer.init()
    music = pygame.mixer.Sound("game song.wav")
    music_channel = pygame.mixer.Channel(0)  # Use channel 0 for background music
    music_channel.play(music, loops=-1)
    music_channel.set_volume(0.25)    

    equation, total = new_equation()
    equation_start = time.time()
    score = 0
    while run:
        block_count += clock.tick(90)
        elapsed_time = time.time() - start_time
        if block_count > block_add_increment:
            block_add_increment = spawn_blocks(blocks, blocks_text, 
                                               block_add_increment, total,
                                               equation_start)
            block_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
        
        keys = pygame.key.get_pressed()
        handle_player_movement(keys, player)
        
        hit, correct = update_blocks(blocks, blocks_text, 
                                     player, total)
        
        if hit and correct:
            correct_sound = pygame.mixer.Sound("hit_correct.mp3")
            sfx_channel = pygame.mixer.Channel(2)
            sfx_channel.play(correct_sound)
            sfx_channel.set_volume(1.0)
            score += total
            equation, total = new_equation()
            equation_start = time.time()
            draw_score(score)
            draw_screen(player, elapsed_time, blocks, blocks_text, heart_list,
                        equation, score)
            pygame.display.update() 
            pygame.time.delay(200) 
        elif hit and not correct:
            #sound effect plays
            if len(heart_list) > 1:
                incorrect_sound = pygame.mixer.Sound("incorrect.mp3")
                inc_channel = pygame.mixer.Channel(1)
                inc_channel.play(incorrect_sound)
                inc_channel.set_volume(1.0)
            
            #hearts remove
            heart_list.pop()
            draw_screen(player, elapsed_time, blocks, blocks_text, heart_list,
                        equation, score)
            pygame.display.update() 
            pygame.time.delay(200)  
        
        if len(heart_list) == 0:
            lost_lives = pygame.mixer.Sound("lost_sound.mp3")
            lost_channel = pygame.mixer.Channel(3)
            lost_channel.play(lost_lives)
            lost_channel.set_volume(1.0)
            music_channel.stop()
            display_game_over(score, elapsed_time)
            restart_quit()
            return
        
        if elapsed_time >= 60:
            finished_sound = pygame.mixer.Sound("finished_sound.mp3")
            finished_channel = pygame.mixer.Channel(4)
            finished_channel.play(finished_sound)
            finished_channel.set_volume(1.0)
            music_channel.stop()
            display_game_over(score, elapsed_time)
            restart_quit()
            return
            
        draw_screen(player, elapsed_time, blocks, blocks_text, heart_list, 
                    equation, score)
    
if __name__ == "__main__":
    while True:
        main()
    