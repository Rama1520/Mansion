import pygame
import sys
import math
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.change_x = 0
        self.change_y = 0

    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def move(self, walls):
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

    def set_position(self, position):
        self.rect.x, self.rect.y = position

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player

    def update(self):
        # Calcula la dirección hacia la posición del jugador
        dx = self.player.rect.x - self.rect.x
        dy = self.player.rect.y - self.rect.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx /= distance
            dy /= distance

        # Calcula la velocidad del enemigo (60% de la velocidad del jugador)
        speed = 0.6 * math.hypot(self.player.change_x, self.player.change_y)

        # Mueve el enemigo hacia el jugador
        self.rect.x += int(dx * speed)
        self.rect.y += int(dy * speed)

        # Verifica si colisiona con el jugador
        if pygame.sprite.collide_rect(self, self.player):
            return True  # El jugador ha sido golpeado por el enemigo
        return False

class Room(object):
    def __init__(self):
        self.wall_list = pygame.sprite.Group()

    def get_starting_position(self):
        pass


class Room1(Room):
    def __init__(self):
        super().__init__()
        self.is_last_room = False
        walls = [
            [0, 0, 20, 600, WHITE],
            [0, 0, 20, 250, WHITE],
            [0, 350, 20, 250, WHITE],
            [780, 0, 20, 250, WHITE],
            [780, 350, 20, 250, WHITE],
            [20, 0, 760, 20, WHITE],
            [20, 580, 760, 20, WHITE],
            [390, 50, 20, 500, BLUE]
        ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

    def get_starting_position(self):
        return 50, 50


class Room2(Room):
    def __init__(self):
        super().__init__()
        self.is_last_room = False
        walls = [
            [0, 0, 20, 600, RED],
            [0, 0, 20, 250, RED],
            [0, 350, 20, 250, RED],
            [780, 0, 20, 250, RED],
            [780, 350, 20, 250, RED],
            [20, 0, 760, 20, RED],
            [20, 580, 760, 20, RED],
            [190, 50, 20, 500, GREEN],
            [590, 50, 20, 500, GREEN]
        ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        self.enemy = Enemy(400, 300, Player)  # Crea una instancia del enemigo
        self.enemy_sprites = pygame.sprite.Group()
        self.enemy_sprites.add(self.enemy) 
    def get_starting_position(self):
        return 50, 50


class Room3(Room):
    def __init__(self):
        super().__init__()
        self.is_last_room = True
        walls = [
            [0, 0, 20, 600, PURPLE],
            [0, 0, 20, 250, PURPLE],
            [0, 350, 20, 250, PURPLE],
            [780, 0, 20, 250, PURPLE],
            [780, 350, 20, 250, PURPLE],
            [20, 0, 760, 20, PURPLE],
            [20, 580, 760, 20, PURPLE]
        ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)
        for x in range(100, 800, 100):
            for y in range(50, 451, 300):
                wall = Wall(x, y, 20, 200, RED)
                self.wall_list.add(wall)
        for x in range(150, 700, 100):
            wall = Wall(x, 200, 20, 200, WHITE)
            self.wall_list.add(wall)

    def get_starting_position(self):
        return 50, 50


def show_menu():
    pygame.init()
    screen = pygame.display.set_mode([800, 600])
    pygame.display.set_caption('Maze Runner')

    font = pygame.font.Font(None, 36)
    menu_text = font.render("Jugar (Pulsa 'J')   Salir (Pulsa 'S')", True, WHITE)
    menu_rect = menu_text.get_rect(center=(400, 300))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    pygame.quit()
                    return True
                elif event.key == pygame.K_s:
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        screen.blit(menu_text, menu_rect)
        pygame.display.flip()


def game_loop():
    pygame.init()
    screen = pygame.display.set_mode([800, 600])
    pygame.display.set_caption('Maze Runner')
    
    clock = pygame.time.Clock()
    done = False

    start_time = pygame.time.get_ticks()
    elapsed_time = 0

    player = Player(50, 50)
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)

    rooms = [Room1(), Room2(), Room3()]

    current_room_no = 0
    current_room = rooms[current_room_no]

    done = False

    victory_image = pygame.image.load("PP_TN2023_FEB DIV_H\PP_TN2023_FEB DIV_H\pygames/victoria2.png")
    victory_image_rect = victory_image.get_rect(center=(400, 300))
    victory_shown = False

    derrota_image = pygame.image.load("PP_TN2023_FEB DIV_H\PP_TN2023_FEB DIV_H\pygames\derrota.png")
    derrota_image_rect = derrota_image.get_rect(center=(400, 300))

    while not done:
        for event in pygame.event.get():
            
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time

            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and player.change_x == 0:
                    player.changespeed(5, 0)
                if event.key == pygame.K_LEFT and player.change_x == 0:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_UP and player.change_y == 0:
                    player.changespeed(0, -5)
                if event.key == pygame.K_DOWN and player.change_y == 0:
                    player.changespeed(0, 5)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.changespeed(5, 0)
                if event.key == pygame.K_UP and player.change_y < 0:
                    player.changespeed(0, 5)
                if event.key == pygame.K_DOWN and player.change_y > 0:
                    player.changespeed(0, -5)

        player.move(current_room.wall_list)


        if player.rect.x >= 800:
            if current_room_no < len(rooms) - 1:
                current_room_no += 1
                current_room = rooms[current_room_no]
                player.set_position(current_room.get_starting_position())
                victory_shown = False
        elif player.rect.x <= 0:
            if current_room_no > 0:
                current_room_no -= 1
                current_room = rooms[current_room_no]
                player.set_position(current_room.get_starting_position())
                victory_shown = False
        elif player.rect.y >= 600:
            if current_room_no < len(rooms) - 1:
                current_room_no += 1
                current_room = rooms[current_room_no]
                player.set_position(current_room.get_starting_position())
                victory_shown = False
        elif player.rect.y <= 0:
            if current_room_no > 0:
                current_room_no -= 1
                current_room = rooms[current_room_no]
                player.set_position(current_room.get_starting_position())
                victory_shown = False

        screen.fill(BLACK)
        movingsprites.draw(screen)
        current_room.wall_list.draw(screen)

        if current_room.is_last_room and player.rect.x >= 800 and not victory_shown:
            screen.fill(BLACK)
            current_room.wall_list.draw(screen)
            screen.blit(victory_image, victory_image_rect)
            pygame.display.flip()
            victory_shown = True
            pygame.time.wait(2000)  # Esperar 2 segundos antes de volver al menú

        if victory_shown:
            show_menu()
            game_loop()

        screen.fill(BLACK)
        movingsprites.draw(screen)
        current_room.wall_list.draw(screen)

        font = pygame.font.Font(None, 36)
        time_text = font.render("Time: " + str(int(elapsed_time / 1000)) + " seconds", True, PURPLE)
        screen.blit(time_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    show_menu()
    game_loop()