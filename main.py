import pygame
import sys
import os

# Инициализация Pygame
pygame.init()

# --- Настройки экрана ---
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Моя Pygame Игра")

# --- Цвета ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (122, 122, 122)
RED = (255, 0, 0)

# --- Переменные игры ---
game_running = True
clock = pygame.time.Clock()  # для управления FPS


# --- Функции игры ---

def draw_scene():
    """ Функция для отрисовки сцены игры """
    screen.fill(GRAY)  # Заливаем фон белым

    # Тут можно добавить отрисовку игровых элементов
    pygame.draw.rect(screen, WHITE, (320, 180, 1280, 720))  # Пример квадрата

    pygame.display.flip()  # Обновляем экран

    # создадим группу, содержащую все спрайты
    all_sprites = pygame.sprite.Group()

    # создадим спрайт
    button = pygame.sprite.Sprite()
    # определим его вид
    button.image = load_image("button.jpg")
    # и размеры
    button.rect = button.image.get_rect()
    # добавим спрайт в группу
    all_sprites.add(button)

    button.rect.x = 500
    button.rect.y = 700

    all_sprites.draw(screen)


def handle_input():
    """ Функция для обработки ввода """
    global game_running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        # Тут обрабатываются нажатия кнопок, мыши и т.п.

def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def update_game():
    """ Функция для обновления состояния игры """
    # тут обновляется логика игры - движение объектов, проверка столкновений и тп.

# --- Главный игровой цикл ---
while game_running:
    # --- 1. Обрабатываем ввод ---
    handle_input()

    # --- 2. Обновляем состояние игры ---
    update_game()

    # --- 3. Отрисовываем сцену ---
    draw_scene()

    # --- Управление FPS ---
    clock.tick(60)  # Ограничиваем частоту кадров до 60 FPS

# Выход из Pygame
pygame.quit()
sys.exit()
