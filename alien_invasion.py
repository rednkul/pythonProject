import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Класс для управления ресурсами и повоедением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресуры."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()
        self._create_fleet()


    def run_game(self):

        """Запуск основного цикла игры."""
        while True:
            self._chek_events()
            self._update_screen()
            self._update_bullets()
            self.ship.update()




    def _chek_events(self):
        """Обрабатывает нажатия клавиш и события мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
               self._chek_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._chek_keyup_events(event)

    def _chek_keydown_events(self, event):
        """Реагирует на нажатие клавиш"""
        if event.key == pygame.K_RIGHT:
            # Переместить корабль вправо.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Переместить корабль влево.
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            # Выход из игры
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _chek_keyup_events(self, event):
        """Реагирует на отпускание клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        new_bullet = Bullet(self)
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позицию снаряда и удаляет его при уходе за экран"""
        # Обновление позиции снаряда .
        self.bullets.update()

        # Удаление снаряда, вышедшего за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        print(len(self.bullets))

    def _update_screen(self):
        """Обновляет отображение экрана"""
        # При каждом проходе цикла перерисовывается экран.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

    def _create_fleet(self):
        """Создание флота вторжения"""
        # Cоздание пришельца
        alien = Alien(self)
        self.aliens.add(alien)


if __name__ == '__main__':
    # Создание экземпялра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
