from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        as_data = asdict(self)
        return ('Тип тренировки: {}; '
                'Длительность: {:.3f} ч.; '
                'Дистанция: {:.3f} км; '
                'Ср. скорость: {:.3f} км/ч; '
                'Потрачено ккал: {:.3f}.').format(*as_data.values())


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

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
        raise NotImplementedError(
            f'Определи get_spent_calories в {self.__class__.__name__}.')

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
    SPEED_MULTIPLIER: int = 18
    SPEED_SHIFT: int = 20

    def get_spent_calories(self) -> float:
        return ((self.SPEED_MULTIPLIER * self.get_mean_speed()
                - self.SPEED_SHIFT)
                * self.weight
                / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MULTIPLIER: float = 0.035
    EXPONENT: int = 2
    HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height  # рост спортсмена

    def get_spent_calories(self) -> float:
        return ((self.WEIGHT_MULTIPLIER
                 * self.weight
                 + (self.get_mean_speed()
                    ** self.EXPONENT
                    // self.weight)
                 * self.HEIGHT_MULTIPLIER
                 * self.weight)
                * self.duration
                * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SPEED_SHIFT: float = 1.1
    WEIGHT_MULTIPLIER: int = 2

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
                 + self.SPEED_SHIFT)
                * self.WEIGHT_MULTIPLIER
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    TRAINING_CLASSES: dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type in TRAINING_CLASSES:
        return TRAINING_CLASSES[workout_type](*data)
    else:
        raise ValueError('Тренировки нет.')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
