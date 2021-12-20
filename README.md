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
