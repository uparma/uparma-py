#!/usr/bin/env python3
import uparma
import random
import pytest

jsons = {
    ("general", "parameters"): "parameters.json",
    ("general", "styles"): "styles.json",
}
up = uparma.UParma(refresh_jsons=False, parameter_data=jsons)

# filter parameters to ones that can be sensibly used as reverse lookups
param_w_value_trans = [x for x in up.parameters if len(up.parameters[x]["value_translations"]) > 0]
param_wone = [x for x in up.parameters if len(up.parameters[x]["value_translations"]) == 1]
test_data_list = []
for test_id in param_w_value_trans:
    use_to_test = True
    for styles, values in up.parameters[test_id]["value_translations"].items():
        key_set = set()
        value_set = set()
        for key, value in values:
            key_set.add(key)
            value_set.add(value)

        if len(key_set) != len(value_set):
            use_to_test = False
            break
    if use_to_test is True:
        test_data_list.append(test_id)

test_data_list = [146]

@pytest.mark.parametrize("test_id", test_data_list)
def test_simple_back_and_forward_mapping(test_id):
    param_dict = up.parameters[test_id]
    for source_style in param_dict["key_translations"]:
        if isinstance(param_dict["key_translations"][source_style], list):
            continue
        for target_style in param_dict["key_translations"]:
            if isinstance(param_dict["key_translations"][target_style], list):
                continue

            if source_style == target_style:
                # skip tranlations of a style to itself
                continue

            print()
            print(source_style, target_style)

            if source_style == "pepnovo_style_1" and target_style == "ursgal_style_1":
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
                if retour_mapping != original_dict:
                    xx = 1
                assert retour_mapping == original_dict
