import uparma
import pytest
import json
import os
from pathlib import Path


test_data_list = [
    {
        "input": {
            ("general", "parameters"): [
                {
                    "name": "Luke",
                    "key_translations": {
                        "ursgal_style_1": "The force is strong in this one",
                    },
                },
                {
                    "name": "Leia",
                    "key_translations": {
                        "ursgal_style_1": "The force is strong in this one",
                    },
                },
            ]
        },
        "results": "Duplicate parameter found: ursgal_style_1 - The force is strong in this one",
    }
]


@pytest.mark.parametrize("test_dict", test_data_list)
def test_load_duplicated_data(test_dict):
    with pytest.raises(ValueError) as err:
        up = uparma.UParma(refresh_jsons=False, parameter_data=test_dict["input"])

    assert str(err.value) == test_dict["results"]
