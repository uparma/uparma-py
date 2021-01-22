import uparma
import pytest
import json
import os
from pathlib import Path

test_data_list = [
    # {
    #     "input": {
    #         (
    #             "general",
    #             "parameters",
    #         ): "https://raw.githubusercontent.com/uparma/uparma-lib/master/jsons/parameters.json",
    #         (
    #             "general",
    #             "styles",
    #         ): "https://raw.githubusercontent.com/uparma/uparma-lib/master/jsons/styles.json",
    #     },
    #     "results": None,
    # },
    {
        "input": {
            ("general", "parameters"): "parameters.json",
            ("general", "styles"): "styles.json",
        },
        "results": None,
    },
    {"input": None, "results": None},
]


@pytest.mark.parametrize("test_dict", test_data_list)
def test_initialise(test_dict):

    param = test_dict["input"]
    results = test_dict["results"]

    if param is None:
        up = uparma.UParma(refresh_jsons=False)
    else:
        up = uparma.UParma(refresh_jsons=False, parameter_data=param)

    # param = test_dict["input"]
    # loaded = up.load_data(identifier=param["identifier"], data_source=param["data_source"])
    #
    # results = test_dict["results"]
    # if results is None:
    #     assert loaded is False
    #     assert up.jsons[param["identifier"]] is None
    # else:
    #     assert loaded is True
    #     assert len(up.jsons[param["identifier"]]) == results["size"]
    #
    #     for idx, name in enumerate(results["names"]):
    #         assert up.jsons[param["identifier"]][idx]["name"] == name
