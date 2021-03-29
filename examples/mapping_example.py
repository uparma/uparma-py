#!/usr/bin/env python3
import uparma
import pprint


def main():
    up = uparma.UParma(refresh_jsons=False)
    print('Original input:')
    input_dict = {
        "precursor_mass_tolerance_unit": "da",
        "min_pep_length" : 8,
        "max_num_mods"  : 3,
    }
    pprint.pprint(input_dict)

    msgf_params = up.convert(
        input_dict,
        translated_style='msgfplus_style_1'
    )
    print('\nMapped to msgf+:')
    pprint.pprint(msgf_params)

    print('\nDetails:')
    pprint.pprint(msgf_params.details)


if __name__ == '__main__':
    main()
