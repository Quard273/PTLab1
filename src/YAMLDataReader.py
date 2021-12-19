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
