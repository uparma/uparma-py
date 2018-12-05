#!/usr/bin/env python3
import requests
import os
import json
import uparma

URLS = {
    ('general', 'parameters') : 'https://raw.githubusercontent.com/uparma/uparma-lib/master/general_parameters.json',
    ('spectrum', 'parameters') : 'https://raw.githubusercontent.com/uparma/uparma-lib/master/spectrum_parameters.json',
    ('modifications', 'parameters') : 'https://raw.githubusercontent.com/uparma/uparma-lib/master/modification_parameters.json',
    ('general', 'styles') : 'https://raw.githubusercontent.com/uparma/uparma-lib/master/styles.json'
}


class UParma(object):
    """
    Universal Parameter Mapper Class

    Keyword Arguments:
        refresh_jsons (bool): indicates if uparma jsons should be pulled from
            central repo (https://github.com/uparma/uparma-lib) or not.
            Note that if jsons are not available in uparma folder, option is
            overridden and set to True.

        source_style (str): Convenience when mapper is used to map from the
            same source style every time, in which case self.convert can be used
            instead of self.translate

    """
    def __init__(self, refresh_jsons=False, source_style="ursgal_style_1"):
        self.source_style = source_style
        self.jsons = {}
        self.parameter2id = {}
        self.available_styles = []
        self.parameters = {}

        for url_id, url in URLS.items():
            json_file_name = os.path.basename(url)
            full_path = os.path.join(
                os.path.dirname(uparma.uparma.__file__), json_file_name
            )
            if os.path.exists(full_path) is False:
                refresh_jsons = True
                # we will have to pull

            if refresh_jsons is True:
                with requests.get(url) as req:
                    with open(full_path, 'w') as j:
                        print(
                            json.dumps(
                                req.json(),
                                indent=2,
                                sort_keys=True
                            ), file=j
                        )
                    self.jsons[url_id] = req.json()
            else:
                for url_id, url in URLS.items():
                    with open(full_path) as j:
                        self.jsons[url_id] = json.load(j)

        self._parse_jsons()

    def _parse_jsons(self):
        """
        Parse and prepare jsons into internal structure in the form of::
            self.parameter2id = {
                'xtandem_style_1' : {
                    'spectrum, parent monoisotopic mass error units' : 42
                }
            }

        """
        for url_id in self.jsons.keys():
            json_tag, json_type = url_id
            if json_type != 'parameters':
                continue
            for uparma_entry in self.jsons[url_id]:
                print(uparma_entry)
                _id = uparma_entry['_id']
                self.parameters[_id] = uparma_entry

                for key, value in uparma_entry.items():
                    if "style" in key:
                        if isinstance(value, list):
                            value = ", ".join(value)
                        try:
                            self.parameter2id[key][value] = _id
                        except:
                            self.parameter2id[key] = {value: _id}
                            self.available_styles.append(key)

                assert _id in self.parameters.keys(), """
                ID {0} is not unique in parameters.json
                """.format(_id)

    def convert(self, param_dict, target_style=None):
        """
        Convenient wrapper to translate params with the source style defined
        during init.

        Calls self.translate with source_style = self.source_style
        """
        return self.translate(
            param_dict,
            source_style=self.source_style,
            target_style=target_style
        )

    def translate(self, param_dict, source_style=None, target_style=None):
        """
        Translate param_dict from source style into target style.


        Keyword Arguments:
            param_dict (dict): dict containing parameter and value in a given
                style

            source_style (str): style of the input format

            target_style (str): style to which the parameters should be
                translated to.

        Returns:
            translated_params (dict-like): dict with the translated key and
                values for the input dict with additional information in
                self.details (see above).

        For example an input in ursgal style::

            {
                "precursor_mass_tolerance_unit": "ppm",
                "min_pep_length" : 8
            }

        can be converted to msgfplus style, yielding::

            {
                '-minLength' : 8.
                '-t' : 'ppm'
            }

        the return object is a dict-like structure which holds additional
        detailed information accessible via self.details.
        For the example above, self.details looks like::

            {
                'min_pep_length': {
                    'source_key': 'min_pep_length',
                    'source_style': 'ursgal_style_1',
                    'source_value': 8,
                    'target_key': '-minLength',
                    'target_style': 'msgfplus_style_1',
                    'target_value': 8
                },
                'precursor_mass_tolerance_unit': {
                    'source_key': 'precursor_mass_tolerance_unit',
                   'source_style': 'ursgal_style_1',
                   'source_value': 'ppm',
                   'target_key': '-t',
                   'target_style': 'msgfplus_style_1',
                   'target_value': 'ppm'
                }
            }




        """
        cannot_be_translated = "{0} for {1} cannot be translated into {2}"

        translated_params = UParmaDict()
        for param_name, param_value in param_dict.items():

            _id = self.parameter2id[source_style].get(param_name, None)

            translated_key = cannot_be_translated.format(
                "Key", param_name, target_style
            )
            if _id is not None:
                translated_key = self.parameters[_id][target_style]

            _value_translations = self.parameter2id[source_style].get("value_translations", None)

            translated_value = param_value
            if _value_translations is not None:
                if target_style in _value_translations.keys():
                    if param_value in _value_translations[target_style].keys():
                        translated_value = _value_translations[target_style][param_value]

            translated_params.details[param_name] = {
                "source_value" : param_value,
                "source_key" : param_name,
                "source_style": source_style,
                "target_key": translated_key,
                "target_value": translated_value,
                "target_style": target_style
            }

            translated_params[translated_key] = translated_value

        return translated_params



class UParmaDict(dict):
    """
    UParma Dict

    Offers original key and values that have been translated by
    the UParMa in self.details.
    """
    def __init__(self,*args, **kwargs):
        self.details = {}
        super().__init__(*args, **kwargs)



if __name__ == '__main__':
    UParma(refresh_jsons=True)

