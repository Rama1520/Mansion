import pygame
import sys
import pygame.font
import sqlite3
from pygame import mixer
from sqlite import guardar_datos

def dato_sanitizado(fila):
    elementos = [str(elemento).strip('\'\"') for elemento in fila]
    lista = ' - '.join(elementos)
    return lista


def show_victory_screen(tiempo_juego):
    mixer.music.stop()
    pygame.init()
    size = [800, 600]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Laberinto")
    fondovictoria = pygame.image.load(r"Labo1\pygames\imagenes_mansion\victoria.png").convert()
    screen.blit(fondovictoria, [0,0])
    nombre1=input("Ingrese su nombre: ")
    guardar_datos(nombre1,tiempo_juego)
    mixer.music.load(r"Labo1\pygames\musica mansion\victoria1.mp3")
    mixer.music.play(-1)
    mixer.music.set_volume(0.2)

    done = False
    clock = pygame.time.Clock()

    pos = 75
    with sqlite3.connect("puntuacion.db") as conexion:
        cursor = conexion.execute("SELECT Nombre, Tiempo FROM MansionSpooky")
        for fila in cursor:
            print(fila)
            fila_sanitizada = dato_sanitizado(fila)
            pos = pos + 25
            font = pygame.font.SysFont("microsoftjhengheimicrosoftjhengheiui", 20)
            fila_sanitizada = font.render(fila_sanitizada, True, "RED")
            screen.blit(fila_sanitizada, (300, pos))  
            pygame.display.flip()
    #Se queda en bucle esperando que el usuario le de al "space"
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    done = True


        pygame.display.flip()
        clock.tick(60)
