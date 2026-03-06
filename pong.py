import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('PONG')
clock = pygame.time.Clock()
dt = 0
running = True

game_state = "start_menu"
winner = None
dificuldade = 1

score1 = 0
score2 = 0
color = "white"

player1 = pygame.Rect(30, screen.get_height() / 2 - 50, 20, 100)
player2 = pygame.Rect(950, screen.get_height() / 2 - 50, 20, 100)

base_speed = 300
MAX_SPEED = 900
radius = 10

ball_rect = pygame.Rect(
    screen.get_width() / 2 - radius,
    screen.get_height() / 2 - radius,
    radius * 2,
    radius * 2
)

def start_ball(dificuldade):
    global base_speed

    lado = random.choice([-1,1])
    
    if dificuldade == 1:
        base_speed = 300
    elif dificuldade == 2:
        base_speed = 400
    elif dificuldade == 3:
        base_speed = 500
    elif dificuldade == 4:
        base_speed = 700

    vel_x = base_speed * lado
    vel_y = random.randint(-150, 150)

    while -50 < vel_y < 50:
        vel_y = random.randint(-150, 150)

    ball_vel.update(vel_x, vel_y)

def reset_ball():
    ball_rect.center = (screen.get_width() / 2, screen.get_height() / 2)
    
    ball_vel.x = base_speed
    ball_vel.y = random.randint(-150, 150)

    while -50 < ball_vel.y < 50:
        ball_vel.y = random.randint(-150, 150)

    player1.y = screen.get_height() / 2 - 50
    player2.y = screen.get_height() / 2 - 50

def start_game(dificuldade):
    global score1, score2, winner, game_state, ball_vel
    score1 = 0
    score2 = 0
    winner = None
    ball_vel = pygame.Vector2(0, 0)
    game_state = "playing"
    start_ball(dificuldade)

def draw_text(text, size, x, y):
    font = pygame.font.Font("PressStart2P-Regular.ttf", size)    
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

while running:
    dt = clock.tick(60) / 1000

    margem = 10
    bounds = screen.get_rect().inflate(0, -margem * 2)
    player1.clamp_ip(bounds)
    player2.clamp_ip(bounds)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "start_menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_game(dificuldade)

                if event.key == pygame.K_LEFT:
                    if dificuldade > 1:
                        dificuldade -= 1

                if event.key == pygame.K_RIGHT:
                    if dificuldade < 4:
                        dificuldade += 1
        elif game_state == "winner_screen":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state = "start_menu"

                if event.key == pygame.K_SPACE:
                    start_game(dificuldade)

    
    screen.fill("black")

    if game_state == "start_menu":
        mouse_pos = pygame.mouse.get_pos()

        draw_text("PONG", 60, screen.get_width() / 2 - 130, 180)
        draw_text("Espaço para jogar", 30, screen.get_width() / 2 - 250, 260)
        draw_text("Dificuldade: ", 30, screen.get_width() / 2 - 250, 310)
        draw_text(f"< {dificuldade} >", 30, screen.get_width() / 2 + 100, 310)

        if dificuldade == 4:
            color = "red"
        else:
            color = "white"

        draw_text("Player 1", 25, 20, screen.get_height() - 140)
        draw_text("W para cima", 15, 20, screen.get_height() - 90)
        draw_text("S para baixo", 15, 20, screen.get_height() - 60)
        draw_text("Player 2", 25, screen.get_width() - 215, screen.get_height() - 140)
        draw_text("Seta para cima", 15, screen.get_width() - 225, screen.get_height() - 90)
        draw_text("Seta para baixo", 15, screen.get_width() - 240, screen.get_height() - 60)

    if game_state == "winner_screen":
        winner_text = f"Player {winner} ganhou!"
        draw_text(winner_text, 30, screen.get_width() / 2 - 230, 150)
        draw_text(f"{score1} - {score2}", 50, screen.get_width() / 2 - 130, 50)
        draw_text("Espaço para jogar novamente", 20, screen.get_width() / 2 - 270, screen.get_height() - 130)
        draw_text("ESC para voltar ao início", 20, screen.get_width() / 2 - 250, screen.get_height() - 80)

        if dificuldade == 4:
            color = "red"
        else:
            color = "white"

    elif game_state == "playing":
        if score1 == 3:
            winner = 1
            ball_vel.update(0, 0)
            game_state = "winner_screen"
        
        if score2 == 3:
            winner = 2
            ball_vel.update(0, 0)
            game_state = "winner_screen"

        draw_text(f"{score1} - {score2}", 50, screen.get_width() / 2 - 130, 50)

        pygame.draw.rect(screen, color, player1)
        pygame.draw.rect(screen, color, player2)
        pygame.draw.circle(screen, color, ball_rect.center, radius)

        ball_rect.x += ball_vel.x * dt
        ball_rect.y += ball_vel.y * dt

        if ball_rect.right < 0:
            score2 += 1
            reset_ball()
            ball_vel.x *= -1
        elif ball_rect.left > screen.get_width():
            score1 += 1
            reset_ball()
            ball_vel.x *= 1

        if ball_rect.top <= 0 or ball_rect.bottom >= screen.get_height():
            ball_vel.y *= -1
        
        if ball_rect.colliderect(player1):
            ball_rect.left = player1.right

            impacto = ball_rect.centery - player1.centery
            impacto_normalizado = impacto / (player1.height / 2)
            impacto_normalizado = max(-1, min(1, impacto_normalizado))

            MAX_ANGLE = math.radians(40)

            angle = impacto_normalizado * MAX_ANGLE
            speed = ball_vel.length() * 1.05
            ball_vel.x = math.cos(angle) * speed
            ball_vel.y = math.sin(angle) * speed


        if ball_rect.colliderect(player2):
            ball_rect.right = player2.left

            impacto = ball_rect.centery - player2.centery
            impacto_normalizado = impacto / (player2.height / 2)
            impacto_normalizado = max(-1, min(1, impacto_normalizado))

            MAX_ANGLE = math.radians(40)

            angle = impacto_normalizado * MAX_ANGLE
            speed = ball_vel.length() * 1.05
            ball_vel.x = -math.cos(angle) * speed
            ball_vel.y = math.sin(angle) * speed
        
        if ball_vel.length() > MAX_SPEED:
            ball_vel = ball_vel.normalize() * MAX_SPEED

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1.y -= 350 * dt
        if keys[pygame.K_s]:
            player1.y += 350 * dt
        if keys[pygame.K_UP]:
            player2.y -= 350 * dt
        if keys[pygame.K_DOWN]:
            player2.y += 350 * dt

    pygame.display.flip()

pygame.quit()
