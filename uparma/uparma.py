import requests
import os
import json
from collections import defaultdict as ddict

URLS = {
    'parameter_url' : 'https://raw.githubusercontent.com/uparma/uparma-lib/master/parameters.json',
    'styles_url' : 'https://raw.githubusercontent.com/uparma/uparma-lib/master/styles.json'
}


class UParma(object):
    """
    Universal Parameter Mapper Class
    """
    def __init__(self, refresh_jsons=False, source_style="ursgal_style_1"):
        self.source_style = source_style
        self.jsons = {}
        self.parameter2id = {}
        self.available_styles = []
        self.parameters = {}

        for url_id, url in URLS.items():
            json_file_name = os.path.basename(url)
            if refresh_jsons is True:
                with requests.get(url) as req:
                    with open(json_file_name, 'w') as j:
                        print(req.json(), file=j)
                    self.jsons[json_file_name] = req.json()
            else:
                for url_id, url in URLS.items():
                    full_path = os.path.join(
                        os.path.dirname(__file__), json_file_name
                    )
                    with open(full_path) as j:
                        self.jsons[json_file_name] = json.load(j)

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
        for uparma_entry in self.jsons['parameters.json']:

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
        """
        return self.translate(
            param_dict,
            source_style=self.source_style,
            target_style=target_style
        )

    def translate(self, param_dict, source_style=None, target_style=None):
        """
        Translate param_dict from source style into target style.

        e.g.:

            {
                "precursor_mass_tolerance_unit": "ppm",
                "min_pep_length" : 8
            }

        to msgfplus::

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
        cannot_be_translated = "{0} for {1} cannot be translated into {2}"

        translated_params = {}
        for param_name, param_value in param_dict.items():
            translated_params[param_name] = {}

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

            translated_params[param_name] = {
                "value" : param_value,
                "translated_key": translated_key,
                "translated_value": translated_value,
                "translated_to": target_style
            }
        return translated_params




