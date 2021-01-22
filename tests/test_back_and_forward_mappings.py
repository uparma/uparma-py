#!/usr/bin/env python3
import uparma
import random

jsons = {
    ("general", "parameters"): "parameters.json",
    ("general", "styles"): "styles.json",
}
up = uparma.UParma(refresh_jsons=False, parameter_data=jsons)


def test_simple_back_and_forward_mapping():
    while True:
        skey = random.choice(list(up.parameters.keys()))
        # skey = 54

        param_dict = up.parameters[skey]
        available_styles = param_dict["key_translations"].keys()
        if len(available_styles) >= 2:
            break

    while True:
        # must be sure to have both keys in the random param_dict
        try:
            source_style, target_style = random.choices(available_styles, k=2)
            # python 3.7
        except:
            source_style, target_style = random.sample(available_styles, 2)
            # python <3.7
        if source_style in available_styles and target_style in available_styles:
            break

    print(skey, source_style, target_style)
    # generate appropriate value
    if source_style in param_dict["value_translations"]:
        idx = random.randrange(len(param_dict["value_translations"][source_style]))
        value = param_dict["value_translations"][source_style][idx][1]
    else:
        value = param_dict["default_value"]
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
