import pygame
import sys
import math
import pygame.font
from pygame import mixer

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
        self.image = pygame.image.load(r"PP_TN2023_FEB DIV_H\PP_TN2023_FEB DIV_H\pygames\dron1.png")
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
        self.image = pygame.image.load(r"PP_TN2023_FEB DIV_H\PP_TN2023_FEB DIV_H\pygames\fantasma (1).png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player
        self.update_counter = 0  # Agregar el contador de actualización

    def update(self):
        self.update_counter += 1  # Incrementar el contador en cada actualización

        # Verificar si ha alcanzado la frecuencia deseada de actualización
        if self.update_counter >= 2:  
            self.update_counter = 0  # Reiniciar el contador

            dx = self.player.rect.x - self.rect.x
            dy = self.player.rect.y - self.rect.y
            distance = math.hypot(dx, dy)
            if distance != 0:
                dx /= distance
                dy /= distance

            speed = 0.9 * math.hypot(self.player.change_x, self.player.change_y)

            self.rect.x += int(dx * speed)
            self.rect.y += int(dy * speed)

            if pygame.sprite.collide_rect(self, self.player):
                return True
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
            [0, 0, 16, 604, PURPLE],
            [0, 0, 16, 254, PURPLE],
            [0, 350, 16, 254, PURPLE],
            [784, 0, 16, 254, PURPLE],
            [784, 350, 16, 254, PURPLE],
            [16, 0, 768, 16, PURPLE],
            [16, 588, 768, 16, PURPLE],
            [390, 60, 16, 480, BLUE]
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
            [0, 0, 16, 604, PURPLE],
            [0, 0, 16, 254, PURPLE],
            [0, 350, 16, 254, PURPLE],
            [784, 0, 16, 254, PURPLE],
            [784, 350, 16, 254, PURPLE],
            [16, 0, 768, 16, PURPLE],
            [16, 588, 768, 16, PURPLE],
            [190, 16, 16, 500, GREEN],
            [590, 88, 16, 500, GREEN]
        ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

    def get_starting_position(self):
        return 50, 50


class Room3(Room):
    def __init__(self):
        super().__init__()
        self.is_last_room = True
        walls = [
            [0, 0, 16, 604, PURPLE],
            [0, 0, 16, 254, PURPLE],
            [0, 350, 16, 254, PURPLE],
            [784, 0, 16, 254, PURPLE],
            [784, 350, 16, 254, PURPLE],
            [16, 0, 768, 16, PURPLE],
            [16, 588, 768, 16, PURPLE]
        ]
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)
        for x in range(100, 800, 100):
            for y in range(16, 451, 372):
                wall = Wall(x, y, 16, 200, RED)
                self.wall_list.add(wall)
        for x in range(150, 700, 100):
            wall = Wall(x, 200, 16, 200, WHITE)
            self.wall_list.add(wall)

    def get_starting_position(self):
        return 50, 350


def show_menu():
    pygame.init()
    size = [800, 600]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Laberinto")

    done = False
    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True
                    clock = pygame.time.Clock()
                    current_time = pygame.time.get_ticks()

        screen.fill(BLACK)

        fondoini = pygame.image.load(r"PP_TN2023_FEB DIV_H\PP_TN2023_FEB DIV_H\pygames\inicio.png").convert()
        screen.blit(fondoini, [0,0])

        pygame.display.flip()
        clock.tick(60)


def game_loop():
    pygame.init()
    screen_width = 800  # Ancho de la pantalla
    screen_height = 600  # Alto de la pantalla
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Laberinto")
    

    clock = pygame.time.Clock()
    
    current_time = pygame.time.get_ticks()

    pygame.display.flip()

    current_room_no = 1
    current_room = Room1()
    rooms = [current_room, Room2(), Room3()]

    player = Player(50, 50)
    enemy = Enemy(250, 300, player)

    active_sprite_list = pygame.sprite.Group()
    player.walls = current_room.wall_list
    enemy.walls = current_room.wall_list

    player.set_position(current_room.get_starting_position())
    active_sprite_list.add(player)
    active_sprite_list.add(enemy)

    done = False



    mixer.music.load("PP_TN2023_FEB DIV_H\PP_TN2023_FEB DIV_H\pygames/musicaplimplum.mp3")
    mixer.music.play(-1)
    mixer.music.set_volume(0.2)

    flag= True
    while not done:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time 
        for event in pygame.event.get():
            if flag == True:
                flag = False
                current_time =0
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-3, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(3, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, -3)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, 3)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(3, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-3, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, 3)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -3)

        player.move(current_room.wall_list)

        if enemy.update():
            show_defeat_screen()
            # El jugador ha sido golpeado por el enemigo
            done = True

        if player.rect.x > 801:
            if current_room.is_last_room:
                done = True
                show_victory_screen()
            else:
                current_room_no += 1
                current_room = rooms[current_room_no - 1]
                player.walls = current_room.wall_list
                player.set_position(current_room.get_starting_position())
        screen.fill(BLACK)
    
        if current_room_no == 1:
            fondo2 = pygame.image.load(r"PP_TN2023_FEB DIV_H\PP_TN2023_FEB DIV_H\pygames\room1.png").convert()
            
            screen.blit(fondo2, [0,0])
            pass
        elif current_room_no == 2:
            fondo2 = pygame.image.load(r"PP_TN2023_FEB DIV_H\PP_TN2023_FEB DIV_H\pygames\room2.png").convert()
            
            screen.blit(fondo2, [0,0])
            pass
        elif current_room_no == 3:
            fondo2 = pygame.image.load(r"PP_TN2023_FEB DIV_H\PP_TN2023_FEB DIV_H\pygames\room3.png").convert()
            
            screen.blit(fondo2, [0,0])
            pass
        current_room.wall_list.draw(screen)
            
        active_sprite_list.draw(screen)

        font = pygame.font.Font(None, 30)
        time_text = font.render("Tiempo: " + str(int(elapsed_time / 1000)) + " segundos", True, WHITE)
        screen.blit(time_text, (1, 1))


        pygame.display.flip()
        clock.tick(60)



def show_victory_screen():
    mixer.music.stop()
    pygame.init()
    size = [800, 600]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Laberinto")

    done = False
    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True

        fondovictoria = pygame.image.load(r"PP_TN2023_FEB DIV_H\PP_TN2023_FEB DIV_H\pygames\victoria.png").convert()
        screen.blit(fondovictoria, [0,0])

        pygame.display.flip()
        clock.tick(60)


def show_defeat_screen():
    mixer.music.stop()
    pygame.init()
    size = [800, 600]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Laberinto")

    done = False
    clock = pygame.time.Clock()

    fondo2 = pygame.image.load(r"PP_TN2023_FEB DIV_H\PP_TN2023_FEB DIV_H\pygames\derrota1.png").convert()
    screen.blit(fondo2,(0,0))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True

        fondoderrota = pygame.image.load(r"PP_TN2023_FEB DIV_H\PP_TN2023_FEB DIV_H\pygames\derrota1.png").convert()
        screen.blit(fondoderrota, [0,0])

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


show_menu()
game_loop()
