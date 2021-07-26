import sys
from random import randint
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from stars import Star


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

        self.stars = pygame.sprite.Group()
        self._create_stars()

    def run_game(self):

        """Запуск основного цикла игры."""
        while True:
            self._chek_events()
            self._update_screen()
            self._update_bullets()
            self.ship.update()
            self._update_aliens()


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

        self._chek_bullet_alien_collisions()

    def _chek_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами"""
        # При обнаружениии попадания удалить снаряд и пришельца
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, False, True)
        # Уничтожение существующих снарядов и создание нового флота.
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте"""
        self.aliens.update()
        self._check_fleet_edges()

        # Проверка коллизий "пришелец - корабль".
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print('Кораблю №?@$%!!!')

    def _update_screen(self):
        """Обновляет отображение экрана"""
        # При каждом проходе цикла перерисовывается экран.
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

    def _create_fleet(self):
        """Создание флота вторжения"""
        # Cоздание пришельца и вычисление количества пришельцев в ряду
        # Интервал между соседними пришельцами равен ширине пришельца.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """Определяет количество рядов, помещающихся на экране."""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Создание флота пришельцев.
        for row_number in range(number_rows - 2):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_stars(self):
        """Создание случайного фона из звезд"""
        star = Star(self)
        star_width, star_height = star.rect.size
        # Определение количества звезд в ряду
        stars_available_space_x = self.settings.screen_width - (2 * star_width)
        number_stars_x = stars_available_space_x // (2 * star_width)

        """Определяет количество рядов звезд на экране"""
        stars_available_space_y = self.settings.screen_height - 3 * star_height
        stars_number_rows = stars_available_space_y // (2 * star_height)

        # Создание звездного фона
        for row_number in range(stars_number_rows):
            for star_number in range(number_stars_x):
                self._create_star(star_number, row_number)

    def _create_star(self, star_number, row_number):
        """Создание звезды"""
        star = Star(self)
        star_width, star_height = star.rect.size
        star.x = (star_width + 2 * star_width * star_number) * randint(2, 4)
        star.rect.x = star.x
        star.rect.y = (star_height + 2 * star_height * row_number) * randint(2, 4)
        self.stars.add(star)


if __name__ == '__main__':
    # Создание экземпялра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
