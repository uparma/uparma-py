import uparma
import pytest
import pprint


up = uparma.UParma()

test_data_list = [
    {
        "source_style": "ursgal_style_1",
        "target_style": "terminat0r_style_1",
        "input_dict": {
            "really?": "yes!",
            "really, really?": "YEEEESS!",
        },
        "results": {
            "really?": "yes!",
            "really, really?": "YEEEESS!",
        },
    },
    {
        "source_style": "ursgal_style_1",
        "target_style": "omssa_style_1",
        "input_dict": {
            "max_output_e_value": 2.3,
        },
        "results": {
            "-he": 2.3,
        },
    },
    {
        "source_style": "ursgal_style_1",
        "target_style": "omssa_style_1",
        "input_dict": {
            "max_num_of_ions_per_series_to_search": 0,
        },
        "results": {
            "-sp": "all",
        },
    },
    {
        "target_style": "ursgal_style_1",
        "source_style": "omssa_style_1",
        "input_dict": {
            "-sp": "all",
        },
        "results": {
            "max_num_of_ions_per_series_to_search": 0,
        },
    },
]


@pytest.mark.parametrize("test_dict", test_data_list)
def test_mapping(test_dict):
    up.source_style = test_dict["source_style"]
    pprint.pprint(test_dict)
    translated_params = up.translate(
        test_dict["input_dict"],
        source_style=test_dict["source_style"],
        target_style=test_dict["target_style"],
    )

    assert sorted(translated_params.items()) == sorted(test_dict["results"].items())
