import sys
import random
import pygame

# --- INITIALIZATION ---
pygame.init()
SCREENWIDTH, SCREENHEIGHT = 288, 512
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption("Flappy Bird - Tejaswi Edition")
CLOCK = pygame.time.Clock()

# Fonts
FONT = pygame.font.SysFont("Arial", 40, bold=True)
SMALL_FONT = pygame.font.SysFont("Arial", 20, bold=True)

# --- GAME CONSTANTS ---
GRAVITY = 0.4
FLAP_STRENGTH = -7.5
MAX_VELOCITY = 10     
PIPE_SPEED = 3.5

PIPE_WIDTH = 141
PIPE_HEIGHT = 386     
PIPE_GAP = 150        
PIPE_SPACING = 320    

BIRD_WIDTH = 34
BIRD_HEIGHT = 24
PLAYER_X = 50

TEXT_COLOR = (255, 255, 255)
OUTLINE_COLOR = (0, 0, 0)
GROUND_COLOR = (222, 216, 149)

high_score = 0

# --- LOAD ASSETS & MASKS ---
try:
    BG_IMG = pygame.image.load("bg.png").convert()
    BG_IMG = pygame.transform.scale(BG_IMG, (SCREENWIDTH, SCREENHEIGHT))

    PIPE_IMG_BOTTOM = pygame.image.load("pipe.png").convert_alpha()
    PIPE_IMG_BOTTOM = pygame.transform.scale(PIPE_IMG_BOTTOM, (PIPE_WIDTH, PIPE_HEIGHT))
    PIPE_IMG_TOP = pygame.transform.flip(PIPE_IMG_BOTTOM, False, True)
    
    pipe_bottom_mask = pygame.mask.from_surface(PIPE_IMG_BOTTOM)
    pipe_top_mask = pygame.mask.from_surface(PIPE_IMG_TOP)
    
    BIRD_IMG = pygame.image.load("bird.png").convert_alpha()
    BIRD_IMG = pygame.transform.scale(BIRD_IMG, (BIRD_WIDTH, BIRD_HEIGHT))
    bird_mask = pygame.mask.from_surface(BIRD_IMG)
    
except FileNotFoundError:
    print("ERROR: Assets missing! 'bg.png', 'pipe.png', 'bird.png' check karein.")
    sys.exit()

def draw_text(text, font, x, y, center=True):
    surf = font.render(str(text), True, TEXT_COLOR)
    outline = font.render(str(text), True, OUTLINE_COLOR)
    rect = surf.get_rect()
    if center: rect.center = (x, y)
    else: rect.topleft = (x, y)
    
    SCREEN.blit(outline, (rect.x - 2, rect.y))
    SCREEN.blit(outline, (rect.x + 2, rect.y))
    SCREEN.blit(outline, (rect.x, rect.y - 2))
    SCREEN.blit(outline, (rect.x, rect.y + 2))
    SCREEN.blit(surf, rect)

def main():
    global high_score
    
    player_y = SCREENHEIGHT // 2
    player_velocity = 0
    score = 0
    state = "START" 
    
    pipes = []
    def add_pipe(x_pos):
        top_height = random.randint(50, SCREENHEIGHT - PIPE_GAP - 120) 
        pipes.append({'x': x_pos, 'top': top_height, 'passed': False})
        
    add_pipe(SCREENWIDTH + 50)

    running = True
    while running:
        # --- EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                if state == "START":
                    state = "PLAY"
                    player_velocity = FLAP_STRENGTH
                elif state == "PLAY":
                    player_velocity = FLAP_STRENGTH
                elif state == "OVER":
                    return 

        # --- LOGIC & PHYSICS ---
        if state == "PLAY":
            player_velocity += GRAVITY
            if player_velocity > MAX_VELOCITY:
                player_velocity = MAX_VELOCITY
            player_y += player_velocity

            for pipe in pipes:
                pipe['x'] -= PIPE_SPEED
                if not pipe['passed'] and pipe['x'] + PIPE_WIDTH < PLAYER_X:
                    pipe['passed'] = True
                    score += 1

            if pipes[0]['x'] < -PIPE_WIDTH:
                pipes.pop(0)
            
            if pipes[-1]['x'] < SCREENWIDTH - PIPE_SPACING + PIPE_WIDTH:
                add_pipe(SCREENWIDTH)

            # --- COLLISION ---
            if player_y < -50 or player_y + BIRD_HEIGHT > SCREENHEIGHT - 50:
                state = "OVER"
                if score > high_score: high_score = score
                
            for pipe in pipes:
                offset_top = (pipe['x'] - PLAYER_X, (pipe['top'] - PIPE_HEIGHT) - int(player_y))
                offset_bot = (pipe['x'] - PLAYER_X, (pipe['top'] + PIPE_GAP) - int(player_y))
                
                if bird_mask.overlap(pipe_top_mask, offset_top) or bird_mask.overlap(pipe_bottom_mask, offset_bot):
                    state = "OVER"
                    if score > high_score: high_score = score

        # --- RENDER ---
        SCREEN.blit(BG_IMG, (0, 0))
        
        for pipe in pipes:
            SCREEN.blit(PIPE_IMG_TOP, (pipe['x'], pipe['top'] - PIPE_HEIGHT))
            SCREEN.blit(PIPE_IMG_BOTTOM, (pipe['x'], pipe['top'] + PIPE_GAP))
        
        pygame.draw.rect(SCREEN, GROUND_COLOR, (0, SCREENHEIGHT - 50, SCREENWIDTH, 50))
        pygame.draw.rect(SCREEN, OUTLINE_COLOR, (0, SCREENHEIGHT - 50, SCREENWIDTH, 50), 2)

        SCREEN.blit(BIRD_IMG, (PLAYER_X, int(player_y)))
        
        # --- UI STATES ---
        if state == "START":
            draw_text("TAP TO START", SMALL_FONT, SCREENWIDTH // 2, SCREENHEIGHT // 2 - 40)
            # Aapka signature branding yahan add ho gaya hai!
            draw_text("Created by Indian 💖 Tejaswi!", SMALL_FONT, SCREENWIDTH // 2, SCREENHEIGHT // 2 + 10)
        elif state == "PLAY":
            draw_text(score, FONT, SCREENWIDTH // 2, 50)
        elif state == "OVER":
            draw_text("GAME OVER", FONT, SCREENWIDTH // 2, SCREENHEIGHT // 2 - 80)
            draw_text(f"Score: {score}", SMALL_FONT, SCREENWIDTH // 2, SCREENHEIGHT // 2 - 20)
            draw_text(f"High Score: {high_score}", SMALL_FONT, SCREENWIDTH // 2, SCREENHEIGHT // 2 + 10)
            draw_text("TAP TO RESTART", SMALL_FONT, SCREENWIDTH // 2, SCREENHEIGHT // 2 + 70)

        pygame.display.update()
        CLOCK.tick(60) 

if __name__ == "__main__":
    while True:
        main()