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
    up = uparma.UParma(parameter_data=test_dict["input"])
    default_params = up.get_default_params(style="msfragger_style_3")
    assert (
        default_params["precursor_mass_tolerance_unit"]["translated_key"]
        == "precursor_mass_units"
    )
    assert default_params["precursor_mass_tolerance_unit"]["translated_value"] == 1
    assert (
        default_params["precursor_mass_tolerance"]["translated_key"]
        == "precursor_mass_lower"
    )
    assert default_params["precursor_mass_tolerance"]["translated_value"] == 5
    assert default_params["database"]["translated_value"] is None


def test_get_default_params_with_list_of_keys():
    d = {
        "input": {
            ("general", "parameters"): [
                {
                    "default_value": "14N",
                    "description": "15N if the corresponding amino acid labeling was applied",
                    "key_translations": {
                        "myrimatch_style_1": "label",
                        "omssa_style_1": ["-tem", "-tom"],
                        "pipi_style_1": "15N",
                        "ursgal_style_1": "label",
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
    assert default_params["label"]["translated_key"] == ["-tem", "-tom"]
    assert default_params["label"]["translated_value"] == "14N"


def test_get_default_params_with_no_value_trans_for_default():
    d = {
        "input": {
            ("general", "parameters"): [
                {
                    "default_value": "ppm",
                    "description": "Fragment mass tolerance unit: available in ppm (parts-per-millon), da (Dalton) or mmu (Milli mass unit)",
                    "key_translations": {
                        "xtandem_style_1": "spectrum, fragment monoisotopic mass error units",
                        "ursgal_style_1": "frag_mass_tolerance_unit",
                    },
                    "name": "frag_mass_tolerance_unit",
                    "tag": ["accuracy", "fragment"],
                    "triggers_rerun": True,
                    "value_translations": {"xtandem_style_1": [["da", "Daltons"]]},
                    "value_type": "select",
                },
            ]
        }
    }
    up = uparma.UParma(refresh_jsons=False, parameter_data=d["input"])
    default_params = up.get_default_params("xtandem_style_1")
    assert (
        default_params["frag_mass_tolerance_unit"]["translated_key"]
        == "spectrum, fragment monoisotopic mass error units"
    )
    assert default_params["frag_mass_tolerance_unit"]["translated_value"] == "ppm"


def test_get_default_msfragger_3():
    up = uparma.UParma()
    default_params = up.get_default_params("msfragger_style_3")
    import pprint

    pprint.pprint(default_params)
    assert default_params["enzyme_specificity"]["translated_value"] == 2
