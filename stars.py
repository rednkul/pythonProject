import pygame
from pygame.sprite import Sprite
from random import randint
class Star(Sprite):

    def __init__(self, ai_game):
        """Инициализирует звезду и задает ее начальную позицию"""
        super().__init__()

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Загрузка изображения звезды и назначение атрибута rect
        self.type_star = randint(0,1)
        if self.type_star == 0:
            self.image = pygame.image.load('images/star_1.png').convert_alpha()
        else:
            self.image = pygame.image.load('images/star_2.png').convert_alpha()
        self.angle = randint(1, 90)

        self.rotated_image = pygame.transform.rotate(self.image, 45)

        self.rect = self.rotated_image.get_rect()

        # Каждая новая звезда появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной горизонтальной позиции звезды.
        self.x = float(self.rect.x)

