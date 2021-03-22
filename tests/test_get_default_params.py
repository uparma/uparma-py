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
                    "default_value": 5,
                    "value_type": "select",
                    "tag": ["accuracy", "precursor"],
                    "key_translations": {
                        "msfragger_style_3": "precursor_mass_lower",
                    },
                },
                {
                    "_id": 3,
                    "name": "database",
                    "description": "Precursor mass tolerance",
                    "default_value": None,
                    "tag": ["accuracy", "precursor"],
                    "key_translations": {
                        "msfragger_style_3": "database_name",
                    },
                },
            ]
        },
        "results": ["The force is strong in this o->"],
    }
]


@pytest.mark.parametrize("test_dict", test_data_list)
def test_get_default_params(test_dict):
    up = uparma.UParma(refresh_jsons=False, parameter_data=test_dict["input"])
    default_params = up.get_default_params("msfragger_style_3")
    assert default_params["precursor_mass_units"] == 1
    assert default_params["precursor_mass_lower"] == 5
    assert default_params["database_name"] is None


def test_get_default_params_with_list_of_keys():
    d = {
        "input": {
            ("general", "parameters"): [
                {
                    "_id": 135,
                    "default_value": "14N",
                    "description": "15N if the corresponding amino acid labeling was applied",
                    "key_translations": {
                        "myrimatch_style_1": "label",
                        "omssa_style_1": ["-tem", "-tom"],
                        "pipi_style_1": "15N",
                    },
                    "name": "label",
                    "tag": ["label", "modifications"],
                    "triggers_rerun": True,
                    "value_translations": {"pipi_style_1": [["14N", 0], ["15N", 1]]},
                    "value_type": "select",
                },
            ]
        }
    }
    up = uparma.UParma(refresh_jsons=False, parameter_data=d["input"])
    default_params = up.get_default_params("omssa_style_1")
    assert default_params[("-tem", "-tom")] == "14N"
