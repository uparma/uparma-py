#!/usr/bin/env python3
import uparma
import pprint

def main():
    up = uparma.UParma()
    msgf_params = up.convert(
        {
            "precursor_mass_tolerance_unit": "ppm",
            "min_pep_length" : 8
        },
        target_style = 'msgfplus_style_1'
    )
    pprint.pprint(msgf_params)
    """
    {
        'min_pep_length': {
            'translated_key': '-minLength',
            'translated_to': 'msgfplus_style_1',
            'translated_value': 8,
            'value': 8
        },
        'precursor_mass_tolerance_unit': {
            'translated_key': '-t',
            'translated_to': 'msgfplus_style_1',
            'translated_value': 'ppm',
            'value': 'ppm'
        }
    }
    """

if __name__ == '__main__':
    main()
