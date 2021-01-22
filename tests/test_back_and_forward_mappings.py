#!/usr/bin/env python3
import uparma
import random
import pytest

jsons = {
    ("general", "parameters"): "parameters.json",
    ("general", "styles"): "styles.json",
}
up = uparma.UParma(refresh_jsons=False, parameter_data=jsons)

test_data_list = [x for x in up.parameters if len(up.parameters[x]["value_translations"]) > 0]
# test_data_list = [83]

@pytest.mark.parametrize("test_id", test_data_list)
def test_simple_back_and_forward_mapping(test_id):
    param_dict = up.parameters[test_id]

    for source_style in param_dict["key_translations"]:
        for target_style in param_dict["key_translations"]:
            if source_style == target_style:
                # skip tranlations of a style to itself
                continue

            print(source_style, target_style)

            if source_style == "ursgal_style_1" and target_style == "pyqms_style_1":
                xx = 1
            translations = param_dict["value_translations"].get(source_style, None)

            if translations is None:
                values = [param_dict["default_value"]]
            else:
                values = [x[1] for x in translations]

            for value in values:
                original_dict = {
                    param_dict["key_translations"][source_style]: value
                }

                print('original_dict', original_dict)
                forward_mapping = up.translate(
                    original_dict,
                    source_style=source_style,
                    target_style=target_style
                )
                print('forward_mapping', forward_mapping)
                retour_mapping = up.translate(
                    forward_mapping,
                    source_style=target_style,
                    target_style=source_style
                )
                print('retour_mapping', retour_mapping)
                assert retour_mapping == original_dict
