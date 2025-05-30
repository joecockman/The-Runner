import pygame
from sys import exit
from random import randint

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Woofins')
clock = pygame.time.Clock()

game_music = pygame.mixer.Sound('audio/music.wav')
game_music.set_volume(0.1)
game_music.play(loops = -1)
jump_sound = pygame.mixer.Sound('audio/jump.mp3')
jump_sound.set_volume(0.1)

test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = True
start_time  = 0
score = 0

sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

title_surface = test_font.render('Varnishwoods Nematode Adventure', False, 'Black')
title_rect = title_surface.get_rect(midbottom = (400, 100))

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf,obstacle_rect)
            else: screen.blit(fly_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle  in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animations():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]



#obstacles
snail_frame_1 = pygame.image.load('graphics/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail2.png').convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly2.png').convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_index = 0
fly_surf = fly_frames[fly_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load('graphics/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

player_stand = pygame.image.load('graphics/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_over_text_surface = test_font.render('Game Over. Press Space Bar to Play Again.', False, 'Black')
game_over_text_rect = game_over_text_surface.get_rect(midbottom = (400, 100))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,900)

snail_animation_timer = pygame.USEREVENT +2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT +3
pygame.time.set_timer(fly_animation_timer,200)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                player_gravity = -20
                jump_sound.play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20
                    jump_sound.play()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900,2100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900,2100),150)))
            
            if event.type == snail_animation_timer:
                if snail_frame_index ==  0:
                    snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_index ==  0:
                    fly_index = 1
                else: fly_index = 0 
                fly_surf = fly_frames[fly_index]

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()
        
        # snail_rect.x -= 4
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        # screen.blit(snail_surface,(snail_rect))
        

        player_gravity  += 1
        player_rect.y +=  player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animations()    
        screen.blit(player_surf, player_rect)

        #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        game_active  = collisions(player_rect,obstacle_rect_list)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(title_surface, title_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0
        
        if score == 0:
            screen.blit(game_over_text_surface,game_over_text_rect)
        else:
            final_score_surface = test_font.render(f'Final Score: {score}', False, 'Black')
            final_score_rect = final_score_surface.get_rect(midbottom = (400,330))
            play_again = test_font.render('Press Spacebar to Play Again', False, 'Black')
            play_again_rect = play_again.get_rect(midbottom = (400,360))
            screen.blit(final_score_surface,final_score_rect)
            screen.blit(play_again,play_again_rect)
        

    pygame.display.update()
    clock.tick(60)