from dataclasses import dataclass
from typing import list


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * Training.LEN_STEP) / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CAL_COEF_1 = 18
    CAL_COEF_2 = 20
    MIN = 60

    def get_spent_calories(self) -> float:
        calories = (self.CAL_COEF_1
                    * self.get_mean_speed() - self.CAL_COEF_2)
        return (calories * self.weight / Training.M_IN_KM
                * self.duration * self.MIN)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEF_CAL_3 = 0.035
    COEF_CAL_4 = 2
    COEF_CAL_5 = 0.029
    height: int

    def get_spent_calories(self) -> float:
        calories_1 = self.COEF_CAL_3 * self.weight
        calories_2 = self.get_mean_speed()**self.COEF_CAL_4 // self.height
        calories_3 = calories_2 * self.COEF_CAL_5 * self.weight
        return (calories_1 + calories_3) * self.duration * Running.MIN


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    COEF_CAL_6 = 1.1
    COEF_CAL_7 = 2
    length_pool: float
    count_pool: float

    def get_distance(self) -> float:
        """Переопределяем метод: получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.length_pool * self.count_pool
        return mean_speed / Training.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        calories = self.get_mean_speed() + self.COEF_CAL_6
        return calories * self.COEF_CAL_7 * self.weight


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_dict = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return type_dict[workout_type](*data)


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
        if training is None:
            print('Тип тренировки не определен')
        else:
            main(training)
