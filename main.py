import pygame
import math
import random

pygame.init()

score = 0
SCREEN_WIDTH = 864
SCREEN_HEIGHT = 936

clock = pygame.time.Clock()
frame_rate_per_second = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
background = pygame.image.load("background.png")
ground = pygame.image.load("ground.png")

scroll = 0
bg_width = background.get_width()
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

BIRD_IMAGES = [pygame.image.load("bird1.png"), pygame.image.load("bird2.png"), pygame.image.load("bird3.png")]
bird_x = 50
bird_y = 300
bird_y_change = 0

current_bird_index = 0
BIRD_ANIMATION_SPEED = 5
bird_animation_counter = 0

pipe = pygame.image.load("pipe.png")
startFont = pygame.font.Font('freesansbold.ttf', 32)
def start():
    # displays: "press space bar to start)
    display = startFont.render(f"PRESS SPACE BAR TO START", True, (255, 255, 255))
    screen.blit(display, (20, 200))
    pygame.display.update()

def display_bird():
    screen.blit(BIRD_IMAGES[current_bird_index], (bird_x, bird_y))

pipe_gap = 200  # Gap between top and bottom pipes
pipe_frequency = 1500  # Milliseconds between new pipe generation
last_pipe = pygame.time.get_ticks() - pipe_frequency



class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = pygame.transform.scale(pipe, (pipe.get_width(), SCREEN_HEIGHT // 2))
        self.rect = self.image.get_rect()
        self.passed = False
        # Position 1 for bottom pipe, -1 for top pipe
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - pipe_gap // 2)
        else:
            self.rect.topleft = (x, y + pipe_gap // 2)

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()


    def check_collision(self, bird_rect):
        return self.rect.colliderect(bird_rect)

    def set_passed(self):
        self.passed = True

    def has_passed(self, bird_x):
        if not self.passed and self.rect.right < bird_x:
            self.passed = True
            return True
        return False


pipe_group = pygame.sprite.Group()
score_font = pygame.font.Font('freesansbold.ttf', 32)

def display_score():
    score_display = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_display, (20, 20))

def check_collision():
    global bird_y, bird_y_change, run, score, bird_x

    bird_rect = BIRD_IMAGES[current_bird_index].get_rect(topleft=(bird_x, bird_y))
    for pipe in pipe_group:
        if pipe.check_collision(bird_rect):
            # Collision detected
            bird_y_change = 0  # Stop bird movement
            #run = False
            game_over()
            return True

        # Check if bird has passed the current pair of pipes
        if pipe.has_passed(bird_x):
            score += .5  # Increment score by 1

    return False

restart_button = pygame.image.load("restart_sign.png")
restart_button_rect = restart_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))

def game_over():
    global score, bird_y, bird_y_change, current_bird_index, bird_animation_counter, pipe_group, game_started

    # Display final score
    final_score_text = score_font.render(f"Final Score: {score}", True, (255, 255, 255))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    # Display restart button
    screen.blit(restart_button, restart_button_rect)

    pygame.display.update()

    # Freeze the screen until the player clicks the restart button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if restart_button_rect.collidepoint(mouse_x, mouse_y):
                    # Reset variables
                    score = 0
                    bird_y = 300
                    bird_y_change = 0
                    current_bird_index = 0
                    bird_animation_counter = 0
                    pipe_group.empty()
                    game_started = False
                    return

        pygame.display.update()


run = True
game_started = False  # Track if the game has started

while run:

    clock.tick(frame_rate_per_second)
    current_time = pygame.time.get_ticks()

    screen.blit(background, (0, 0))  # Draw background

    # Draw ground
    screen.blit(ground, (scroll, SCREEN_HEIGHT - ground.get_height()))
    screen.blit(ground, (scroll + bg_width, SCREEN_HEIGHT - ground.get_height()))

    scroll -= 5
    if scroll <= -bg_width:
        scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if not game_started:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True  # Start the game

        if game_started:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_y_change = -6
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    bird_y_change = 2

    if not game_started:
        start()  # Display start message if game not started
    else:
        # Update bird position
        bird_y += bird_y_change
        if bird_y <= 0:
            bird_y = 0
        if bird_y >= 735:
            bird_y = 735

        # Update pipes
        if current_time - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            bottom_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT // 2 + pipe_height, 1)
            top_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT // 2 + pipe_height, -1)
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            last_pipe = current_time

        pipe_group.update()
        pipe_group.draw(screen)

        # Check collisions
        if check_collision():
            game_over()

        # Update bird animation
        bird_animation_counter += 1
        if bird_animation_counter >= BIRD_ANIMATION_SPEED:
            current_bird_index = (current_bird_index + 1) % len(BIRD_IMAGES)
            bird_animation_counter = 0
        display_bird()
        display_score()

    pygame.display.update()

pygame.quit()
