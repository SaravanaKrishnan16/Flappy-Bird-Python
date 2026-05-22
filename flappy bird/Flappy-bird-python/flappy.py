
import pygame
import random
import sys
from pygame.locals import *

# Global Variables
screen_width = 289
screen_height = 511
screen = pygame.display.set_mode((screen_width, screen_height))
ground_y = screen_height * 0.8
game_sprites = {}
game_sounds = {}
player = 'assets/sprites/bluebird-midflap.png'
background = 'assets/sprites/background-day.png'
pipe = 'assets/sprites/pipe.png'

def welcome_screen():
    playerx = int(screen_width / 5)
    playery = int(screen_height / 2)
    messagex = int((screen_width - game_sprites['message'].get_width()) / 2)
    messagey = int(screen_height * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                screen.blit(game_sprites['background'], (0, 0))
                screen.blit(game_sprites['player'], (playerx, playery))
                screen.blit(game_sprites['message'], (messagex, messagey))
                screen.blit(game_sprites['base'], (basex, ground_y))
                pygame.display.update()
                pygame.time.Clock().tick(30)

def main_game():
    score = 0
    playerx = int(screen_width / 5)
    playery = int(screen_height / 2)
    basex = 0

    new_pipe1 = get_random_pipe()
    new_pipe2 = get_random_pipe()

    upper_pipes = [
        {'x': screen_width + 200, 'y': new_pipe1[0]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': new_pipe2[0]['y']}
    ]
    lower_pipes = [
        {'x': screen_width + 200, 'y': new_pipe1[1]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': new_pipe2[1]['y']}
    ]

    pipe_vel_x = -4
    player_vel_y = -9
    player_max_vel_y = 10
    player_min_vel_y = -8
    player_acc_y = 1

    player_flap_accv = -8
    player_flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    player_vel_y = player_flap_accv
                    player_flapped = True

        crash_test = is_collide(playerx, playery, upper_pipes, lower_pipes)
        if crash_test:
            return False, score

        player_mid_pos = playerx + game_sprites['player'].get_width() / 2
        for pipe in upper_pipes:
            pipe_mid_pos = pipe['x'] + game_sprites['pipe'][0].get_width() / 2
            if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
                score += 1
                game_sounds['point'].play()

        if player_vel_y < player_max_vel_y and not player_flapped:
            player_vel_y += player_acc_y

        if player_flapped:
            player_flapped = False
        player_height = game_sprites['player'].get_height()
        playery = playery + min(player_vel_y, ground_y - playery - player_height)

        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            upper_pipe['x'] += pipe_vel_x
            lower_pipe['x'] += pipe_vel_x

        if 0 < upper_pipes[0]['x'] < 5:
            new_pipe = get_random_pipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])

        if upper_pipes[0]['x'] < -game_sprites['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

        screen.blit(game_sprites['background'], (0, 0))
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            screen.blit(game_sprites['pipe'][0], (upper_pipe['x'], upper_pipe['y']))
            screen.blit(game_sprites['pipe'][1], (lower_pipe['x'], lower_pipe['y']))

        screen.blit(game_sprites['base'], (basex, ground_y))
        screen.blit(game_sprites['player'], (playerx, playery))
        my_digits = [int(x) for x in list(str(score))]
        width = 0
        for digit in my_digits:
            width += game_sprites['numbers'][digit].get_width()
        xoffset = (screen_width - width) / 2
        for digit in my_digits:
            screen.blit(game_sprites['numbers'][digit], (xoffset, screen_height * 0.12))
            xoffset += game_sprites['numbers'][digit].get_width()

        pygame.display.update()
        pygame.time.Clock().tick(30)

def is_collide(playerx, playery, upper_pipes, lower_pipes):
    if playery > ground_y - 25 or playery < 0:
        game_sounds['hit'].play()
        return True

    # Create bird bounding rectangle
    player_rect = pygame.Rect(playerx, playery,
                              game_sprites['player'].get_width(),
                              game_sprites['player'].get_height())

    # Check collision with upper pipes
    for pipe in upper_pipes:
        pipe_rect = pygame.Rect(pipe['x'], pipe['y'],
                                game_sprites['pipe'][0].get_width(),
                                game_sprites['pipe'][0].get_height())
        if player_rect.colliderect(pipe_rect):
            game_sounds['hit'].play()
            return True

    # Check collision with lower pipes
    for pipe in lower_pipes:
        pipe_rect = pygame.Rect(pipe['x'], pipe['y'],
                                game_sprites['pipe'][1].get_width(),
                                game_sprites['pipe'][1].get_height())
        if player_rect.colliderect(pipe_rect):
            game_sounds['hit'].play()
            return True
    return False

def get_random_pipe():
    pipe_height = game_sprites['pipe'][0].get_height()
    offset = screen_height / 3
    y2 = offset + random.randrange(0, int(screen_height - game_sprites['base'].get_height() - 1.2 * offset))
    pipe_x = screen_width + 10
    y1 = pipe_height - y2 + offset
    pipe = [
        {'x': pipe_x, 'y': -y1},
        {'x': pipe_x, 'y': y2}
    ]
    return pipe

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Flappy Bird')

    game_sprites['numbers'] = tuple(pygame.image.load(f'assets/sprites/{i}.png').convert_alpha() for i in range(10))
    game_sprites['message'] = pygame.image.load('assets/sprites/message.png').convert_alpha()
    game_sprites['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()
    game_sprites['pipe'] = (
        pygame.transform.rotate(pygame.image.load('assets/sprites/pipe-green.png').convert_alpha(), 180),
        pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
    )
    game_sprites['background'] = pygame.image.load(background).convert()
    game_sprites['player'] = pygame.image.load(player).convert_alpha()

    game_sounds['die'] = pygame.mixer.Sound('assets/audio/die.wav')
    game_sounds['hit'] = pygame.mixer.Sound('assets/audio/hit.wav')
    game_sounds['point'] = pygame.mixer.Sound('assets/audio/point.wav')
    game_sounds['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh.wav')
    game_sounds['wing'] = pygame.mixer.Sound('assets/audio/wing.wav')

    while True:
        welcome_screen()
        game_over, final_score = main_game()
        print(f"Game Over! Your Score: {final_score}")
        print("Do you want to play again? (Y/N): ", end="")
        ans = input().strip().lower()
        if ans != 'y':
            pygame.quit()
            sys.exit()
