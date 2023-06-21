import pygame
import math

#/ Esta clase representa a un enemigo en el juego. 
# El enemigo es un sprite controlado por la computadora y tiene propiedades similares a las del jugador. 
# El enemigo tiene un método update() que verifica si ha golpeado al jugador.#/
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        self.image = pygame.image.load(r"Labo1\pygames\imagenes_mansion\fantasma (1).png")
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