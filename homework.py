class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км; '
                   f'Ср. скорость: {self.speed:.3f} км/ч; '
                   f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65  # Расстояние, которое спортсмен
    M_IN_KM = 1000  # Константа для перевода значений из метров в километры.
    MIN_IN_H = 60  # Перевод из часов в минуты

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action  # количество совершённых действий.
        self.duration = duration  # длительность тренировки.
        self.weight = weight  # вес спортсмена.

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 20

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 - self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight
                / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    wlk_calorie_2 = 2
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height  # рост спортсмена

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER
                 * self.weight
                 + (self.get_mean_speed()
                    ** self.wlk_calorie_2
                    // self.weight)
                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                 * self.weight)
                * self.duration
                * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38  # Переопределяю Расстояние за один гребок.
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float):
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool  # Длина бассейна.
        self.count_pool = count_pool  # Сколько раз переплыл бассейн.

    def get_mean_speed(self) -> float:
        return (self.lenght_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type in workout:
        return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    info = info.get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)