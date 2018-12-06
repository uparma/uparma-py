#!/usr/bin/env python3
import uparma
import random

up = uparma.UParma(refresh_jsons=True)

def turn_into_hashable(entry):
   if isinstance(entry, list):
       entry = ', '.join(entry)
   return entry

def test_simple_back_and_forward_mapping():
    skey = random.choice(list(up.parameters.keys()))

    param_dict = up.parameters[skey]

    while True:
        # must be sure to have both keys in param_dict
        try:
            source_style, target_style = random.choices(up.available_styles, k=2)
            # python 3.7
        except:
            source_style, target_style = random.sample(up.available_styles, 2)
            # python <3.7
        if source_style in param_dict.keys() and target_style in param_dict.keys():
            if isinstance(param_dict[source_style], str) and \
                isinstance(param_dict[target_style], str):
                    break

    print(source_style, target_style)
    forward_dict = {
        param_dict[source_style] : 42
     }
    print('forward_dict', forward_dict)
    forward_mapping = up.translate(
        forward_dict,
        source_style=source_style,
        target_style=target_style
    )
    print('forward_mapping', forward_mapping)
    forward_key = forward_mapping[param_dict[source_style]]['translated_key']
    forward_value = forward_mapping[param_dict[source_style]]['translated_value']
    backward_dict = {
        forward_key : forward_value
    }
    print('backward_dict', backward_dict)
    backwards_mapping = up.translate(
        backward_dict,
        source_style=target_style,
        target_style=source_style
    )
    print('backwards_mapping', backwards_mapping)
    final_dict = {
        backwards_mapping[param_dict[target_style]]['translated_key'] : \
            backwards_mapping[param_dict[target_style]]['translated_value']
    }
    print('final_dict', final_dict)
    assert forward_dict == final_dict
