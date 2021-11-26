#!/usr/bin/env python3
import uparma
import pytest


test_data_list = [
    {
        "uparma_jsons": {
            ("general", "parameters"): [
                {
                    "name": "Luke",
                    "triggers_rerun": True,
                    "key_translations": {
                        "ursgal_style_1": "The force is strong in this o->",
                    },
                },
                {
                    "name": "Leia",
                    "key_translations": {
                        "ursgal_style_1": "The force is strong in this o+",
                    },
                },
            ]
        },
        "input": [
            "The force is strong in this o+",
            "The force is strong in this o->",
        ],
        "results": ["The force is strong in this o->"],
    },
    {
        "uparma_jsons": {
            ("general", "parameters"): [
                {
                    "name": "Luke",
                    "triggers_rerun": True,
                    "key_translations": {
                        "ursgal_style_1": "The force is strong in this o->",
                    },
                },
                {
                    "name": "Leia",
                    "key_translations": {
                        "ursgal_style_1": "The force is strong in this o+",
                    },
                },
            ]
        },
        "input": [
            "The force is strong in this o+",
            "The force is strong in this o->",
            [
                "The force is strong in this o+",
                "The force is strong in this o->",
            ],
        ],
        "descriptions": "A combined parameters should trigger re-run as soon as at least one triggers rerun",
        "results": [
            "The force is strong in this o->",
            [
                "The force is strong in this o+",
                "The force is strong in this o->",
            ],
        ],
    },
    {
        "uparma_jsons": {
            ("general", "parameters"): [
                {
                    "default_value": "tdc",
                    "description": " Method to assign FDR and PEP to PSMs",
                    "key_translations": {
                        "percolator_style_1": ["-y", "-Y"],
                        "percolator_style_2": ["-y", "-Y"],
                        "ursgal_style_1": "percolator_post_processing",
                    },
                    "name": "percolator_post_processing",
                    "tag": ["validation"],
                    "triggers_rerun": True,
                    "value_translations": {},
                    "value_type": "select",
                },
            ]
        },
        "input": [["-y", "-Y"]],
        "results": ["-y", "-Y"],
    },
]


@pytest.mark.parametrize("test_dict", test_data_list)
def test_identify_params_trigger_rerun(test_dict):
    up = uparma.UParma(parameter_data=test_dict["uparma_jsons"])
    rerun_params = up.identify_parameters_triggering_rerun(test_dict["input"])
    assert rerun_params == test_dict["results"]


# def test_identify_params_trigger_rerun_list_param():

#     up = uparma.UParma(parameter_data=test_dict["uparma_jsons"])
#     params_list = [
#         ["-y", "-Y"],
#     ]
#     style = "percolator_style_1"
#     rerun_params = up.identify_parameters_triggering_rerun(params_list)
