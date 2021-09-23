from typing import Dict, Tuple
from Types import DataType
from CalcRating import CalcRating
import pytest

RatingsType = Dict[str, float]


class TestCalcRating():

    @pytest.fixture()
    def input_data(self) -> Tuple[DataType, RatingsType]:
        data: DataType = {
            "Abramov Petr Sergeevich":
            [
                ("mat", 80),
                ("rus", 76),
                ("progr", 100)
            ],
            "Petrov Igor Sergeevich":
            [
                ("mat", 61),
                ("rus", 80),
                ("progr", 78),
                ("lit", 97)
            ]
        }
        rating_scores: RatingsType = {
            "Abramov Petr Sergeevich": 85.3333,
            "Petrov Igor Sergeevich": 79.0000
        }
        return data, rating_scores

    def test_init_calc_rating(self, input_data:
                              Tuple[DataType,
                                    RatingsType]) -> None:

        calc_rating = CalcRating(input_data[0])
        assert input_data[0] == calc_rating.data

    def test_calc(self, input_data:
                  Tuple[DataType, RatingsType]) -> None:

        rating = CalcRating(input_data[0]).calc()
        for student in rating.keys():
            rating_score = rating[student]
            assert pytest.approx(rating_score,
                                 abs=0.001) == input_data[1][student]
