import uparma
import pytest
import json
import os
from pathlib import Path
from pprint import pprint


test_data_list = [
    {
        "input": {
            ("general", "parameters"): [
                {
                    "_id": 1,
                    "name": "precursor_mass_tolerance_unit",
                    "description": "Precursor mass tolerance unit: available in ppm (parts-per-millon), da (Dalton) or mmu (Milli mass unit)",
                    "default_value": "ppm",
                    "value_type": "select",
                    "tag": ["accuracy", "precursor"],
                    "value_translations": {
                        "xtandem_style_1": [["da", "Daltons"]],
                        "msfragger_style_3": [["ppm", 1], ["da", 0]],
                    },
                    "key_translations": {
                        "xtandem_style_1": "spectrum, parent monoisotopic mass error units",
                        "msfragger_style_3": "precursor_mass_units",
                    },
                },
                {
                    "_id": 2,
                    "name": "precursor_mass_tolerance",
                    "description": "Precursor mass tolerance",
                    "default_value": "5",
                    "value_type": "select",
                    "tag": ["accuracy", "precursor"],
                    "key_translations": {
                        "msfragger_style_3": "precursor_mass_lower",
                    },
                },
            ]
        },
        "results": ["The force is strong in this o->"],
    }
]


@pytest.mark.parametrize("test_dict", test_data_list)
def test_identify_params_trigger_rerun(test_dict):
    up = uparma.UParma(refresh_jsons=False, parameter_data=test_dict["input"])
    default_params = up.get_default_params("msfragger_style_3")
    assert default_params["precursor_mass_units"] == 1
    assert default_params["precursor_mass_lower"] == 5
