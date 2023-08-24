import uparma
import pytest
import pprint
import json
import os
from pathlib import Path

test_input_dict = {
    "allow_multiple_variable_mods_on_residue": False,
    "mass_diff_to_variable_mod": False,
    "enzyme_specificity": "full"
}

test_parameter_list = [
    {
        "input": {
            ("general", "parameters"): [
                {
                    "default_value": False,
                    "description": " Put mass difference as a variable modification.",
                    "key_translations": {
                        "msfragger_style_3": "mass_diff_to_variable_mod",
                        "ursgal_style_1": "mass_diff_to_variable_mod"
                    },
                    "name": "write_mass_diff_to_variable_mod",
                    "tag": [],
                    "triggers_rerun": True,
                    "value_translations": {
                        "msfragger_style_3": [
                            [
                                False,
                                0
                            ],
                            [
                                True,
                                1
                            ]
                        ]
                    },
                    "value_type": "bool"
                },
                {
                    "default_value": False,
                    "description": " Static mods are not considered ",
                    "key_translations": {
                        "mascot_style_1": "MULTI_SITE_MODS",
                        "msfragger_style_1": "allow_multiple_variable_mods_on_residue",
                        "msfragger_style_2": "allow_multiple_variable_mods_on_residue",
                        "msfragger_style_3": "allow_multiple_variable_mods_on_residue",
                        "ursgal_style_1": "allow_multiple_variable_mods_on_residue"
                    },
                    "name": "allow_multiple_variable_mods_on_residue",
                    "tag": [
                        "modifications"
                    ],
                    "triggers_rerun": True,
                    "value_translations": {
                        "mascot_style_1": [
                            [
                                False,
                                0
                            ],
                            [
                                True,
                                1
                            ]
                        ],
                        "msfragger_style_1": [
                            [
                                False,
                                0
                            ],
                            [
                                True,
                                1
                            ]
                        ],
                        "msfragger_style_2": [
                            [
                                False,
                                0
                            ],
                            [
                                True,
                                1
                            ]
                        ],
                        "msfragger_style_3": [
                            [
                                False,
                                0
                            ],
                            [
                                True,
                                1
                            ]
                        ],
                        "ursgal_style_1": [
                            [
                                False,
                                False
                            ],
                            [
                                True,
                                True
                            ]
                        ]
                    },
                    "value_type": "bool"
                }
            ]
        }
    }
]
@pytest.mark.parametrize("test_parameters", test_parameter_list)
def test_load_data(test_parameters):
    up = uparma.UParma(refresh_jsons=False, parameter_data=test_parameter_list[0]["input"])
    translation = up.convert(param_dict=test_input_dict,  translated_style="msfragger_style_3")
    up_with_parameter_json = uparma.UParma(refresh_jsons=False)
    translation_params = up_with_parameter_json.convert(param_dict=test_input_dict, translated_style="msfragger_style_3")
    assert translation_params["enzyme_specificity"]["was_translated"]
    assert translation["allow_multiple_variable_mods_on_residue"]["was_translated"]
    assert translation["allow_multiple_variable_mods_on_residue"]["translated_value"] == 0
    assert translation["write_mass_diff_to_variable_mod"]["was_translated"]
    assert translation["write_mass_diff_to_variable_mod"]["translated_value"] == 0