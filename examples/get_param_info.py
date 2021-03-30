#!/usr/bin/env python3
import uparma
import pprint
import sys


def main(parameter):
    '''
    Get uparma information for a specific parameter name. Description, value
    transltion and uparma id is extracted.

    usage:

        ./get_param_info.py <parameter_name>

    E.g.:

        ./get_param_info.py 'spectrum, parent monoisotopic mass error units'

    The example provides the name of the monoisotopic mass error units of the
    X!Tandem engines. This name is mapped back to translation styles matching
    this name.
    '''

    up = uparma.UParma()
    original_style_matching_parameter_name = {}
    for original_style in up.parameter2id.keys():
        _id = up.parameter2id[original_style].get(parameter, None)
        # print(_id)
        if _id is not None:
            if parameter in up.parameter2id[original_style].keys():
                original_style_matching_parameter_name[original_style] = {
                    '_id': _id
                }
            parameter_entry = up.parameters[_id]
            original_style_matching_parameter_name[original_style]['description'] = parameter_entry['description']
            original_style_matching_parameter_name[original_style]['value_translations'] = parameter_entry['value_translations'].get(
                original_style,
                {}
            )
    if len(original_style_matching_parameter_name) == 0:
        print(
            'Parameter "{0}" can not be found! Spelling correct?'.format(
                parameter
            )
        )
    else:
        print(
            'Parameter "{0}" is found for the following translation styles:'.format(
                parameter
            )
        )
    for original_style, original_style_info in original_style_matching_parameter_name.items():
        print(
            '\t{0}; description: {1}; value_translations: {2}; uparma id: {3}'.format(
                original_style,
                original_style_info['description'],
                original_style_info['value_translations'],
                original_style_info['_id'],
            )
        )

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(main.__doc__)
        exit()
    main(sys.argv[1])
