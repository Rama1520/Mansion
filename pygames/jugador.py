import pygame

#/Esta clase representa al jugador en el juego. 
# El jugador es un sprite controlado por el usuario y tiene propiedades como image (la superficie del jugador),
# rect (el rectángulo que representa la posición y el tamaño del jugador)  y métodos para mover al jugador y cambiar su velocidad.#/

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(r"Labo1\pygames\imagenes_mansion\dron1.png")
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
