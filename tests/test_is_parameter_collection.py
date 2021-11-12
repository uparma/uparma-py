import uparma
import pytest
import pprint

param = {
    ("general", "parameters"): [
        {
            "default_value": [],
            "description": "Experimental Setup list describing each sample",
            "is_parameter_collection": True,
            "key_translations": {
                "flash_lfq_style_org": 'experiment_setup\nFormat:\n{"1": {"FileName": <filename as in identfile>, "Condition":<str>, "Biorep": <int>, "Fraction": <int>, "Techrep": <int>},\n"2": ....\n}\n',
                "flash_lfq_style_1": 'experiment_setup\nFormat:\n{"1": {"FileName": <filename as in identfile>, "Condition":<str>, "Biorep": <int>, "Fraction": <int>, "Techrep": <int>},\n"2": ....\n}\n',
                "ursgal_style_1": "experiment_setup",
            },
            "name": "experiment_setup",
            "tag": ["experiment_setup"],
            "triggers_rerun": True,
            "value_translations": {},
            "value_type": "list",
        },
        {
            "default_value": "",
            "description": "Experiment - file name (many more to come)",
            "key_translations": {
                "flash_lfq_style_1": "FileName",
                "ursgal_style_1": "experiment_file_name",
            },
            "name": "experiment_file_name",
            "tag": ["experiment_setup"],
            "triggers_rerun": True,
            "value_translations": {},
            "value_type": "str",
        },
        {
            "default_value": "",
            "description": "Experiment - Condition (many more to come)",
            "key_translations": {
                "flash_lfq_style_1": "Condition",
                "ursgal_style_1": "experiment_condition",
            },
            "name": "experiment_condition",
            "tag": ["experiment_setup"],
            "triggers_rerun": True,
            "value_translations": {},
            "value_type": "str",
        },
    ]
}


test_data_list = [
    {
        "original_style": "ursgal_style_1",
        "translated_style": "flash_lfq_style_1",
        "input_dict": {
            "experiment_setup": [
                {"experiment_file_name": "First", "experiment_condition": "control"},
                {
                    "experiment_file_name": "Second",
                    "experiment_condition": "treatment1",
                },
            ]
        },
        "results": {
            "experiment_setup": [
                {"FileName": "First", "Condition": "control"},
                {"FileName": "Second", "Condition": "treatment1"},
            ]
        },
    }
]


@pytest.mark.parametrize("test_dict", test_data_list)
def test_shows_meta_tag(test_dict):
    up = uparma.UParma(parameter_data=param)
    up.original_style = test_dict["original_style"]
    translated_params = up.translate(
        test_dict["input_dict"],
        original_style=test_dict["original_style"],
        translated_style=test_dict["translated_style"],
    )
    pprint.pprint(translated_params)
    assert "is_parameter_collection" in translated_params["experiment_setup"].keys()


@pytest.mark.parametrize("test_dict", test_data_list)
def test_mapping(test_dict):
    up = uparma.UParma(parameter_data=param)
    up.original_style = test_dict["original_style"]
    translated_params = up.translate(
        test_dict["input_dict"],
        original_style=test_dict["original_style"],
        translated_style=test_dict["translated_style"],
    )
    pprint.pprint(translated_params)
    for uparma_key in translated_params.keys():
        for t_value in translated_params[uparma_key]["translated_value"]:
            translated_sub_dict = {}
            for sub_key, sub_dict in t_value.items():
                translated_sub_dict[sub_dict["translated_key"]] = sub_dict[
                    "translated_value"
                ]

            assert translated_sub_dict in test_dict["results"][uparma_key]
