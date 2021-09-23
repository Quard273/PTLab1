import pytest
from typing import Tuple
from Types import DataType
from TextDataReader import TextDataReader


class TestTextDataReader:

    @pytest.fixture()
    def file_and_data_content(self) -> Tuple[str, DataType]:

        text = "ivanov ivan ivanovich\n" + \
            " mat:91\n" + " xim:100\n" + \
            "petrov petr petrovich\n" + \
            " rus:87\n" + " lit:78\n"

        data = {
            "ivanov ivan ivanovich": [
                ("mat", 91), ("xim", 100)
            ],
            "petrov petr petrovich": [
                ("rus", 87), ("lit", 78)
            ]
        }
        return text, data

    @pytest.fixture()
    def filepath_and_data(self,
                          file_and_data_content: Tuple[str,
                                                       DataType],
                          tmpdir) -> Tuple[str,
                                           DataType]:
        p = tmpdir.mkdir("datadir").join("my_data.txt")
        p.write(file_and_data_content[0])
        return str(p), file_and_data_content[1]

    def test_read(self, filepath_and_data:
                  Tuple[str, DataType]) -> None:
        file_content = TextDataReader().read(filepath_and_data[0])
        assert file_content == filepath_and_data[1]
