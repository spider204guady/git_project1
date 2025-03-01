import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ну, погоди!")

# Загрузка изображений
wolf = pygame.image.load("wolf.png")
egg = pygame.image.load("egg.png")
background = pygame.image.load("background.jpg")

# Масштабирование изображений
wolf = pygame.transform.scale(wolf, (100, 150))
egg = pygame.transform.scale(egg, (40, 50))

# Параметры волка
wolf_x = WIDTH // 2 - 50
wolf_y = HEIGHT - 160
wolf_speed = 10

# Параметры яиц
eggs = []
egg_speed = 5
spawn_time = 1000  # время появления нового яйца (мс)
last_spawn = pygame.time.get_ticks()
score = 0

# Шрифт для счета
font = pygame.font.Font(None, 36)

# Главный цикл игры
running = True
while running:
    screen.blit(background, (0, 0))
    screen.blit(wolf, (wolf_x, wolf_y))

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление волком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and wolf_x > 0:
        wolf_x -= wolf_speed
    if keys[pygame.K_RIGHT] and wolf_x < WIDTH - 100:
        wolf_x += wolf_speed

    # Создание новых яиц
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn > spawn_time:
        egg_x = random.randint(50, WIDTH - 50)
        eggs.append([egg_x, 0])
        last_spawn = current_time

    # Обновление положения яиц
    for egg in eggs[:]:
        egg[1] += egg_speed
        screen.blit((egg, (egg[0], egg[1])))

        # Проверка столкновения волка с яйцом
        if wolf_x < egg[0] < wolf_x + 100 and wolf_y < egg[1] < wolf_y + 150:
            eggs.remove(egg)
            score += 1
        elif egg[1] > HEIGHT:
            eggs.remove(egg)
            score -= 1

    # Отображение счета
    score_text = font.render(f"Счет: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
