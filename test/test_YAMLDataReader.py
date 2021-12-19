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
