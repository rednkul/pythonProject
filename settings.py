class Settings():
    """Класс для хранения всех настроек игры Alien Invasion."""

    def __init__(self):
        """Инициализирует настройки игры."""
        # Параметры экрана
        #self.screen_width = 1200
        #self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Скорость корабля бля
        self.ship_speed = 2

        # Параметры снаряда
        self.bullet_speed = 10
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (229, 81, 55)

        # Максимальное количество снарядов на экране
        self.bullets_allowed = 3

        # Настройки пришельцев
        self.alien_speed = 1.0
        self.fleet_drop_speed = 50
        #fleet_direction = 1 - движение вправо; -1 - влево
        self.fleet_direction = 1

