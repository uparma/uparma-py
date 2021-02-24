import uparma
import pytest
import json
import os
from pathlib import Path

jsons = {
    ("general", "parameters"): "parameters.json",
    ("general", "styles"): "styles.json",
}
up = uparma.UParma(refresh_jsons=False, parameter_data=jsons)


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
            "data_source": Path("tests/parameters_duplicate.json"),
            "identifier": ("general", "parameters"),
        },
        "results": "Duplicate parameter found: ursgal_style_1 - experiment_setup",
    }
]


@pytest.mark.parametrize("test_dict", test_data_list)
def test_load_data(test_dict):
    param = test_dict["input"]
    loaded = up.load_data(
        identifier=param["identifier"], data_source=param["data_source"]
    )
    with pytest.raises(ValueError) as err:
        up._parse_jsons()

    assert str(err.value) == test_dict["results"]
