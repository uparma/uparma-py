import uparma
import pytest


test_data_list = [
    {
        "input": {
            ("general", "parameters"): [
                {
                    "name": "to_key_or_not_to_key",
                    "key_translations": {
                        "ursgal_style_1": "to_key_or_not_to_key",
                        "some_other_style": "to_key_or_not_to_key_<DROP_KEY>",
                    },
                    "value_translations": {
                        "ursgal_style_1": [[True, True], [False, False]],
                        "some_other_style": [[True, "i_lived"], [False, "i_died"]],
                    },
                },
                {
                    "name": "to_key_or_not_to_key_list",
                    "key_translations": {
                        "ursgal_style_1": "to_key_or_not_to_key_list",
                        "some_other_style": [
                            "keyp_no_pun_intended",
                            "to_key_or_not_to_key_<DROP_KEY>",
                        ],
                    },
                    "value_translations": {
                        "ursgal_style_1": [[True, True], [False, False]],
                        "some_other_style": [[True, "i_lived"], [False, "i_died"]],
                    },
                },
                {
                    "name": "to_key_or_not_to_key_rip_delim",
                    "key_translations": {
                        "ursgal_style_1": "to_key_or_not_to_key_rip_delim",
                        "some_other_style": "to_key_or_not_to_key_DROP_KEY",
                    },
                    "value_translations": {
                        "ursgal_style_1": [[True, True], [False, False]],
                        "some_other_style": [[True, "i_lived"], [False, "i_died"]],
                    },
                },
            ]
        },
    }
]


@pytest.mark.parametrize("test_dict", test_data_list)
def test_load_data(test_dict):
    up = uparma.UParma(refresh_jsons=False, parameter_data=test_dict["input"])
    translation = up.convert(
        {
            "to_key_or_not_to_key": True,
            "to_key_or_not_to_key_list": False,
            "to_key_or_not_to_key_rip_delim": False,
        },
        "some_other_style",
    )
    assert translation["to_key_or_not_to_key"]["translated_key"] is None
    assert translation["to_key_or_not_to_key"]["translated_value"] == "i_lived"
    assert translation["to_key_or_not_to_key_list"]["translated_key"] == [
        "keyp_no_pun_intended",
        None,
    ]
    assert translation["to_key_or_not_to_key_list"]["translated_value"] == "i_died"
    assert (
        translation["to_key_or_not_to_key_rip_delim"]["translated_key"]
        == "to_key_or_not_to_key_DROP_KEY"
    )
    assert translation["to_key_or_not_to_key_rip_delim"]["translated_value"] == "i_died"
