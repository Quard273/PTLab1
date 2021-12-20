[![Build Status](https://app.travis-ci.com/Quard273/PTLab1.svg?branch=main)](https://app.travis-ci.com/Quard273/PTLab1)
# Лабораторная 1 по дисциплине "Технологии программирования" "Git_TravisCI"
# Цели данной работы:
1) Познакомиться c распределенной системой контроля версий кода Git и ее функциями;
2) Познакомиться с понятиями «непрерывная интеграция» (CI) и «непрерывное развертывание» (CD), определить их место в современной разработке программного обеспечения;
3) Получить навыки разработки ООП-программ и написания модульных тестов к ним на современных языках программирования;
4) Получить навыки работы с системой Git для хранения и управления версиями ПО;
5) Получить навыки управления автоматизированным тестированием программного обеспечения, расположенного в системе Git, с помощью инструмента Travis CI.
6) Выполнить индивидуальное задание (вариант 9): Определить и вывести на экран студента, имеющего 90 баллов по всем дисциплинам. Если таких студентов несколько, нужно вывести любого из них. Если таких студентов нет, необходимо вывести сообщение об их отсутствии. Формат - YAML.

# Порядок выполнения задания:
1) Создадим файл, который будет реагировать на чтение данных из файлов с расширением "yaml":

from Types import DataType
from DataReader import DataReader
import yaml
from yaml.loader import SafeLoader


class YAMLDataReader(DataReader):
    def __init__(self) -> None:
        self.key = ""
        self.students = {}

    def read(self, path):
        with open(path) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        for student in data:
            for name, subjects in student.items():
                self.key = name
                self.students[self.key] = []
                for subject, rating in subjects.items():
                    self.students[name].append((subject, int(rating)))
        return self.students

2) Напишем для него тест:

import pytest
from typing import Tuple
from Types import DataType
from YAMLDataReader import YAMLDataReader


class TestYAMLDataReader:

    @pytest.fixture()
    def file_and_data_content(self) -> Tuple[str, DataType]:
        text = "---\n" +\
            "- Иванов Иван Иванович:\n" + \
            "    математика: 67\n" + \
            "    литература: 100\n" + \
            "- Петров Петр Петрович:\n" + \
            "    химия: 78\n" + \
            "    социология: 87\n"

        data = {
            "Иванов Иван Иванович": [
                ("математика", 67), ("литература", 100)
            ],
            "Петров Петр Петрович": [
                ("химия", 78), ("социология", 87)
            ]
        }
        return text, data

    @pytest.fixture()
    def filepath_and_data(self,
                          file_and_data_content: Tuple[str, DataType],
                          tmpdir) -> Tuple[str, DataType]:
        p = tmpdir.mkdir("datadir").join("my_data.yaml")
        p.write(file_and_data_content[0])
        return str(p), file_and_data_content[1]

    def test_read(self, filepath_and_data:
                  Tuple[str, DataType]) -> None:
        file_content = YAMLDataReader().read(filepath_and_data[0])
        assert file_content == filepath_and_data[1]

3) Сделаем файл для обработки входных данных:

from typing import Dict
from Types import DataType

RatingType = Dict[str, float]


class CheckAll90Ratings():

    def __init__(self, data: DataType) -> None:
        self.data: DataType = data
        self.rating: RatingType = {}

    def calc(self) -> RatingType:
        for key in self.data:
            ratingCount = 0
            for subject in self.data[key]:
                if subject[1] >= 90:
                    ratingCount = ratingCount + 1
            if ratingCount == len(self.data[key]):
                self.rating[key] = 90
        return self.rating

4) Напишем для него тест:

from typing import Dict, Tuple
from Types import DataType
from CheckAll90Ratings import CheckAll90Ratings
import pytest

RatingsType = Dict[str, float]


class TestCheckAll90Ratings():

    @pytest.fixture()
    def input_data(self) -> Tuple[DataType, RatingsType]:
        data: DataType = {
            "Петров Петр Андреевич":
            [
                ("математика", 95),
                ("русский язык", 99),
                ("программирование", 90)
            ],
            "Игорев Игорь Игоревич":
            [
                ("математика", 65),
                ("русский язык", 80),
                ("программирование", 75),
                ("литература", 95)
            ],
            "Иванов Иван Иванович":
            [
                ("математика", 90),
                ("русский язык", 90),
                ("программирование", 90),
                ("литература", 90)
            ]
        }
        rating_scores: RatingsType = {
            "Абрамов Петр Сергеевич": 90,
            "Иванов Иван Иванович": 90
        }
        return data, rating_scores

    def test_init_calc_rating(self, input_data:
                              Tuple[DataType,
                                    RatingsType]) -> None:
        calc_rating = CheckAll90Ratings(input_data[0])
        assert input_data[0] == calc_rating.data

    def test_calc(self, input_data:
                  Tuple[DataType, RatingsType]) -> None:
        rating = CheckAll90Ratings(input_data[0]).calc()

        for student in rating.keys():
            rating_score = rating[student]

            assert pytest.approx(rating_score,
                                 abs=0.001) == input_data[1][student]

        for student in input_data[1]:
            rating_score = input_data[1][student]

            assert pytest.approx(rating_score,
                                 abs=0.001) == rating[student]

5) Отредактируем main для правильной работы:

from YAMLDataReader import YAMLDataReader
from CalcRating import CalcRating
import argparse
import sys


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def main():
    path = get_path_from_arguments(sys.argv[1:])
    reader = YAMLDataReader()
    students = reader.read(path)
    print("Students: ", students)
    rating = CalcRating(students).calc()
    print("Ratings: ", rating)


if __name__ == "__main__":
    main()
    
    # Pull request и graph:
![Скриншот 20-12-2021 131504](https://user-images.githubusercontent.com/91258441/146751654-9e487abf-5d2d-4d28-8343-306128ba337b.jpg)
