import pygame
import sys
import math
import pygame.font
import sqlite3
from pygame import mixer
from jugador import Player
from ene_my import Enemy
from pantalladerrota import show_defeat_screen
from pantallavictoria import show_victory_screen


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

class Room(object):
    def __init__(self):
        self.wall_list = pygame.sprite.Group()

    def get_starting_position(self):
        pass

#Define como sera la habitacion construyendo los muros 
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

#Define como sera la habitacion construyendo los muros 
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

#Define como sera la habitacion construyendo los muros 
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
    clock = pygame.time.Clock()

    done = False
    #Se queda en bucle esperando que el usuario le de al "space"
    while done == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True

        fondoini = pygame.image.load(r"Labo1\pygames\imagenes_mansion\inicio.png").convert()
        screen.blit(fondoini, [0,0])

        pygame.display.flip()
        clock.tick(30)


def game_loop():
    pygame.init()
    screen_width = 800  # Ancho de la pantalla
    screen_height = 600  # Alto de la pantalla
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Laberinto")

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
    mixer.music.load("Labo1\pygames\musica mansion\musicaplimplum.mp3")
    mixer.music.play(-1)
    mixer.music.set_volume(0.2)

    clock = pygame.time.Clock()
    while not done:
        tiempo_juego=pygame.time.get_ticks()/1000
        tiempo_juego=float(tiempo_juego)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Aceleracion del personaje segun presiono o suelto una tecla
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

        # El jugador ha sido golpeado por el enemigo
        if enemy.update():
            show_defeat_screen(tiempo_juego)
            
            done = True

        if player.rect.x > 801:
            if current_room.is_last_room:
                done = True
                show_victory_screen(tiempo_juego)
                
            else:
                current_room_no += 1
                current_room = rooms[current_room_no - 1]
                player.walls = current_room.wall_list
                player.set_position(current_room.get_starting_position())
        screen.fill(BLACK)
    

        if current_room_no == 1:
            fondo2 = pygame.image.load(r"Labo1\pygames\imagenes_mansion\room1.png").convert()
            screen.blit(fondo2, [0,0])
            pass
        elif current_room_no == 2:
            fondo2 = pygame.image.load(r"Labo1\pygames\imagenes_mansion\room2.png").convert()
            screen.blit(fondo2, [0,0])
            pass
        elif current_room_no == 3:
            fondo2 = pygame.image.load(r"Labo1\pygames\imagenes_mansion\room3.png").convert()
            screen.blit(fondo2, [0,0])
            pass
        active_sprite_list.draw(screen)
        
        font = pygame.font.Font(None, 30)
        time_text = font.render("Tiempo: " + str(int(tiempo_juego / 1000)) + " segundos", True, WHITE)
        screen.blit(time_text, (1, 1))

        pygame.display.flip()
        clock.tick(60)


show_menu()
game_loop()
