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
                        "ursgal_style_1": "The force is strong in this o->",
                    },
                },
                {
                    "name": "Leia",
                    "key_translations": {
                        "ursgal_style_1": "The force is strong in this o+",
                        "ze_other": "...",
                    },
                },
            ]
        },
    }
]


@pytest.mark.parametrize("test_dict", test_data_list)
def test_load_data(test_dict):
    up = uparma.UParma(refresh_jsons=False, parameter_data=test_dict["input"])
    assert len(up.available_styles) == 2
    assert len(up.parameter2id.keys()) == 2
    assert list(up.parameters.keys()) == [0, 1]
