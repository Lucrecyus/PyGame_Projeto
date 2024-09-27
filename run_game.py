import pygame
import math
import random
from pygame import mixer

pygame.init()

# Definir tamanho da janela
SCREEN_WIDTH = 800
SCREEN_HEIGTH = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
#Background
bg_img = pygame.image.load('galaxia.jpg')
#Background
mixer.music.load('trilha.wav')


menu_font = pygame.font.Font('freesansbold.ttf', 40)
start_text = menu_font.render("Aperte Enter para Começar", True, (255, 255, 255))
exit_text = menu_font.render("Aperte Esc para Sair", True, (255, 255, 255))
start_text_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGTH // 2 - 30))
exit_text_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGTH // 2 + 30))

run_menu = True
game_start = False  # Variável para controlar o estado do jogo (menu ou em execução)

while run_menu:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_menu = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not game_start:
         # Iniciar o jogo com Enter
                game_start = True
                mixer.music.play(-1)
                #Player
                player_img = pygame.image.load('player.png')
                playerX = 360
                playerY = 480
                playerX_move = 0

                #Enemy
                enemy_img = []
                enemyX = []
                enemyY = []
                enemyX_move = []
                enemyY_move = []

                num_of_enemies = 6

                for i in range(num_of_enemies):

                    enemy_img.append(pygame.image.load('enemy_alien.png'))
                    enemyX.append(random.randint(0, 735))
                    enemyY.append(random.randint(50, 150))
                    enemyX_move.append(0.5)
                    enemyY_move.append(40)

                #Laser
                laser_img = pygame.image.load('laser.png')
                laserX = 0
                laserY = 480
                laserX_move = 0
                laserY_move = 1
                laser_state = "pronto"

                #Score
                score_value = 0
                font = pygame.font.Font('freesansbold.ttf', 32)
                textX = 10
                textY = 10

            if event.key == pygame.K_ESCAPE:  # Sair do jogo com Esc
                run_menu = False

    if not game_start:  # Mostrar o menu se o jogo não tiver começado
       
        screen.blit(start_text, start_text_rect)
        screen.blit(exit_text, exit_text_rect)
        pygame.display.update()
    else:
            # Background
            screen.blit(bg_img, (0, 0))
            # Mostrar tela
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
            game_start = False
            pygame.display.set_caption("Space Invaders")
            icon = pygame.image.load('spaceship.png')
            pygame.display.set_icon(icon)

            
            #Game over text
            over_font = pygame.font.Font('freesansbold.ttf', 64)

            def show_score(x,y):
                score = font.render("Score: " + str(score_value), True,(255,255,255) )
                screen.blit(score, (x,y))

            def game_over_text():
                over_text = over_font.render("GAME OVER", True,(255,255,255) )
                screen.blit(over_text, (200,250))

            def player(x,y):
                screen.blit(player_img, (x,y))

            def enemy(x,y,i):
                screen.blit(enemy_img[i], (x,y))

            def fire_laser(x,y):
                global laser_state
                laser_state = "fire"
                screen.blit(laser_img, (x + 16, y + 10))


            def iscollision(enemyX,enemyY,laserX,laserY):

                distance = math.sqrt(math.pow(enemyX-laserX,2) + (math.pow(enemyY - laserY,2)))
                if distance < 27:
                    return True
                else:
                    return False



            run = True
            while run:

                #RGB = Red, Green, Blue
                screen.fill((0,0,0))
                
                #Background
                screen.blit(bg_img, (0,0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                
                    #Obter input do player
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            playerX_move -= 0.6
                        if event.key == pygame.K_RIGHT:
                            playerX_move += 0.6
                        if event.key == pygame.K_SPACE:
                            if laser_state is "pronto":
                                laser_sound = mixer.Sound('laser.wav')
                                laser_sound.play()
                                laserX = playerX
                                fire_laser(playerX,laserY)

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            playerX_move = 0

                #Checar os limites da nave na tela
                playerX += playerX_move

                if playerX <= 0:
                    playerX = 0
                elif playerX >=736:
                    playerX = 736
                
                #Checar os limites dos inimigos na tela e mover para o outro lado se chegar no limite
                for i in range(num_of_enemies):

                    #Game over
                    if enemyY[i] > 440:
                        for j in range(num_of_enemies):
                            enemyY[i] = 2000
                        game_over_text()
                        game_start = False
                        run = False
                        break

                    enemyX[i] += enemyX_move[i]

                    if enemyX[i] <= 0:
                        enemyX_move[i] = 0.5
                        enemyY[i] += enemyY_move[i]
                    elif enemyX[i] >=736:
                        enemyX_move[i] = -0.5
                        enemyY[i] += enemyY_move[i]

                    #Colisão
                    collision = iscollision(enemyX[i],enemyY[i],laserX,laserY)
                    if collision:
                        explosion_sound = mixer.Sound('boom.wav')
                        explosion_sound.play()
                        laserY = 480
                        laser_state = "pronto"
                        score_value += 1
                        enemyX[i] = random.randint(0, 735)
                        enemyY[i] = random.randint(50, 150)
                    
                    enemy(enemyX[i],enemyY[i],i)


                #Movimento do laser
                if laserY <= 0:
                    laserY = 480
                    laser_state = "pronto"

                if laser_state is "fire":
                    fire_laser(laserX,laserY)
                    laserY -= laserY_move

                player(playerX,playerY)
                show_score(textX,textY)
                

                # Atualiza o que é mostrado na tela
                pygame.display.update()


pygame.quit()