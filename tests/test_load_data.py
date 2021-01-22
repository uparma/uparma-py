import uparma
import pytest
import json
import os
from pathlib import Path

up = uparma.UParma(refresh_jsons=False)

test_data = [
    {
        "_id": 1,
        "name": "experiment_setup",
        "description": " ",
        "default_value": [],
        "value_type": "list",
        "tag": ["quantification"],
        "value_translations": {},
        "key_translations": {
            "ursgal_style_1": "experiment_setup",
            "flash_lfq_style_1": "experiment_setup",
        },
    }
]
test_data_list = [
    {
        "input": {
            "data_source": f"https://{Path(__file__).parent.joinpath('parameters.json').as_posix()}",
            # "data_source": "https://raw.githubusercontent.com/uparma/uparma-lib/master/jsons/parameters.json",
            "identifier": ("general", "parameters"),
        },
        "results": {
            "size": 7,
            "names": [
                "max_num_mods",
                "min_pep_length",
                "precursor_mass_tolerance_unit",
                "precursor_mass_tolerance_minus",
                "precursor_mass_tolerance_plus",
                "max_mod_alternatives",
                "score_ion_list",
            ],
        },
    },
    {
        "input": {"data_source": test_data, "identifier": ("general", "parameters")},
        "results": {"size": 1, "names": ["experiment_setup"]},
    },
    {
        "input": {
            "data_source": json.dumps(test_data),
            "identifier": ("general", "parameters"),
        },
        "results": {"size": 1, "names": ["experiment_setup"]},
    },
    {
        "input": {
            "data_source": Path("tests/parameters.json"),
            "identifier": ("general", "parameters"),
        },
        "results": {
            "size": 2,
            "names": ["experiment_setup", "isotopic_distribution_tolerance"],
        },
    },
    {
        "input": {
            "data_source": "tests/parameters.json",
            "identifier": ("general", "parameters"),
        },
        "results": {
            "size": 2,
            "names": ["experiment_setup", "isotopic_distribution_tolerance"],
        },
    },
]


@pytest.mark.parametrize("test_dict", test_data_list)
def test_load_data(test_dict):
    param = test_dict["input"]
    up.load_data(identifier=param["identifier"], data_source=param["data_source"])

    results = test_dict["results"]
    assert len(up.jsons[param["identifier"]]) == results["size"]

    for idx, name in enumerate(results["names"]):
        assert up.jsons[param["identifier"]][idx]["name"] == name
    xx = 1
