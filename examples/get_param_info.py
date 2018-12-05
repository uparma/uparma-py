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
    source_style_matching_parameter_name = {}
    for source_style in up.parameter2id.keys():
        _id = up.parameter2id[source_style].get(parameter, None)
        if _id is not None:
            if parameter in up.parameter2id[source_style].keys():
                source_style_matching_parameter_name[source_style] = {
                    '_id': _id
                }
            parameter_entry = up.parameters[_id]
            source_style_matching_parameter_name[source_style]['description'] = parameter_entry['description']
            source_style_matching_parameter_name[source_style]['value_translations'] = parameter_entry['value_translations'].get(
                source_style,
                {}
            )
    if len(source_style_matching_parameter_name) == 0:
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
    for source_style, source_style_info in source_style_matching_parameter_name.items():
        print(
            '\t{0}; description: {1}; value_translations: {2}; uparma id: {3}'.format(
                source_style,
                source_style_info['description'],
                source_style_info['value_translations'],
                source_style_info['_id'],
            )
        )

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(main.__doc__)
        exit()
    main(sys.argv[1])
