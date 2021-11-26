#!/usr/bin/env python3
import uparma
import random
import pytest

# jsons = {
#     ("general", "parameters"): "parameters.json",
#     ("general", "styles"): "styles.json",
# }
up = uparma.UParma()

# filter parameters to ones that can be sensibly used as reverse lookups
param_w_value_trans = [
    x for x in up.parameters if len(up.parameters[x]["value_translations"]) > 0
]
param_wone = [
    x for x in up.parameters if len(up.parameters[x]["value_translations"]) == 1
]
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

# test_data_list = [146]


@pytest.mark.parametrize("test_id", test_data_list)
def test_simple_back_and_forward_mapping(test_id):
    param_dict = up.parameters[test_id]
    for original_style in param_dict["key_translations"]:
        if isinstance(param_dict["key_translations"][original_style], list):
            continue
        for translated_style in param_dict["key_translations"]:

            if original_style == translated_style:
                # skip translations of a style to itself
                continue
            if isinstance(param_dict["key_translations"][translated_style], list):
                continue
            print()
            print("Translating", original_style, "to", translated_style)

            translations = param_dict["value_translations"].get(original_style, None)

            if translations is None:
                values = [param_dict["default_value"]]
            else:
                values = [x[1] for x in translations]

            for value in values:
                original_dict = {param_dict["key_translations"][original_style]: value}

                print("original_dict", original_dict)
                forward_mapping = up.translate(
                    original_dict,
                    original_style=original_style,
                    translated_style=translated_style,
                )
                new_input = {}
                for k, v in forward_mapping.items():
                    if isinstance(v["translated_key"], list):
                        continue
                    if v["was_translated"] is True:
                        new_input[v["translated_key"]] = v["translated_value"]
                        print("Reformatted forward_mapping", new_input)

                        retour_mapping = up.translate(
                            new_input,
                            original_style=translated_style,
                            translated_style=original_style,
                        )
                        retour = {}
                        for k, v in retour_mapping.items():
                            retour[v["translated_key"]] = v["translated_value"]

                        print("Reformatted retour", retour)
                        assert retour == original_dict

                    elif v["was_translated"] is False:
                        break
