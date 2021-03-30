#!/usr/bin/env python3
import uparma
import pytest


test_data_list = [
    {
        "input": {
            ("general", "parameters"): [
                {
                    "_id": 1,
                    "name": "Luke",
                    "triggers_rerun": True,
                    "key_translations": {
                        "ursgal_style_1": "The force is strong in this o->",
                    },
                },
                {
                    "_id": 2,
                    "name": "Leia",
                    "key_translations": {
                        "ursgal_style_1": "The force is strong in this o+",
                    },
                },
            ]
        },
        "results": ["The force is strong in this o->"],
    }
]


@pytest.mark.parametrize("test_dict", test_data_list)
def test_identify_parameters_triggering_rerun(test_dict):
    up = uparma.UParma(parameter_data=test_dict["input"])
    rerun_params = up.identify_parameters_triggering_rerun(
        [
            "The force is strong in this o+",
            "The force is strong in this o->",
        ]
    )
    assert rerun_params == test_dict["results"]

