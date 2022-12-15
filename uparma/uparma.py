#!/usr/bin/env python3
import requests
import os
import json
from pathlib import Path

import logging

log = logging.getLogger(__name__)

import uparma

URLS = {
    (
        "general",
        "parameters",
    ): f"https://raw.githubusercontent.com/uparma/uparma-lib/master/jsons/parameters.json",
    # f"https://raw.githubusercontent.com/uparma/uparma-lib/v{uparma.__lib_version__}/jsons/parameters.json",
    (
        "general",
        "styles",
    ): f"https://raw.githubusercontent.com/uparma/uparma-lib/master/jsons/styles.json",
    # f"https://raw.githubusercontent.com/uparma/uparma-lib/v{uparma.__lib_version__}/jsons/styles.json",
}

base_path = Path(__file__)


class UParma(object):
    """
    Universal Parameter Mapper Class

    Keyword Arguments:
        refresh_jsons (bool): indicates if uparma jsons should be pulled from
            central repo (https://github.com/uparma/uparma-lib) or not.
            Note that if jsons are not available in uparma folder, option is
            overridden and set to True.

        original_style (str): Convenience when mapper is used to map from the
            same original style every time, in which case self.convert can be used
            instead of self.translate

        parameter_data (dict): overwrite json loading with customized object
            Should look like:
                (
                    "general",
                    "parameters",
                ): "https://raw.githubusercontent.com/uparma/uparma-lib/master/jsons/parameters.json",
                (
                    "general",
                    "styles",
                ): "https://raw.githubusercontent.com/uparma/uparma-lib/master/jsons/styles.json",

            or alternatively, already in dict format:
                (
                    "general",
                    "parameters",
                ): [{"name": ... }]
                (
                    "general",
                    "styles",
                ): [{"name": ... }]


    """

    def __init__(
        self,
        refresh_jsons=False,
        original_style="ursgal_style_1",
        parameter_data=None,
    ):
        self.original_style = original_style
        self.jsons = {}
        self.parameter2id = {}
        self.parameter2id_list = {}
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

            if refresh_jsons is False:
                with open(full_path) as j:
                    try:
                        self.jsons[url_id] = json.load(j)
                    except json.decoder.JSONDecodeError:
                        refresh_jsons = True

            if refresh_jsons is True:
                with requests.get(url) as req:
                    with open(full_path, "w") as j:
                        if req.text == "404: Not Found":
                            raise FileNotFoundError(
                                "No uparma-lib release is compatible with this version of uparma-py.\n"
                                f"{url} not available."
                            )
                        print(json.dumps(req.json(), indent=2, sort_keys=True), file=j)
                    self.jsons[url_id] = req.json()

        # Let's overwrite with custom
        if parameter_data is not None:
            if isinstance(parameter_data, dict) is False:
                logging.warning("Parameter_Data needs is in wrong format")
            else:
                for key, value in parameter_data.items():
                    if isinstance(value, list) is False:
                        logging.warning("Require list of dicts for key {0}".format(key))
                    else:
                        self.jsons[key] = value

        self._parse_jsons()

    def _parse_jsons(self):
        """
        Parse and prepare jsons into internal structure in the form of::
            self.parameter2id = {
                'xtandem_style_1' : {
                    'spectrum, parent monoisotopic mass error units' : 42,
                    ...
                }
            }

        """
        # print(self.jsons[('general', 'parameters')])
        # exit()
        self.parameter2id = {}
        for url_id in self.jsons.keys():
            json_tag, json_type = url_id
            if json_type != "parameters":
                continue

            # print(url_id)
            for _id, uparma_entry in enumerate(self.jsons[url_id]):
                # _id = uparma_entry["_id"]
                self.parameters[_id] = uparma_entry
                for key, value in uparma_entry["key_translations"].items():

                    if isinstance(value, list):
                        value = tuple(value)

                    if key in self.parameter2id.keys():

                        # found key does value also exist
                        if value in self.parameter2id[key]:
                            # parameter already found
                            raise ValueError(
                                "Duplicate parameter found: {key} - {value}".format(
                                    key=key, value=value
                                )
                            )
                        else:
                            # add value = _id
                            self.parameter2id[key][value] = _id
                    else:
                        self.parameter2id[key] = {value: _id}
                        self.available_styles.append(key)

        return

    def convert(self, param_dict, translated_style=None):
        """
        Convenient wrapper to translate params with the original style defined
        during init.

        Calls self.translate with original_style = self.original_style
        """
        return self.translate(
            param_dict,
            original_style=self.original_style,
            translated_style=translated_style,
        )

    def translate(self, param_dict, original_style=None, translated_style=None):
        """
        Translate param_dict from original style into translated style.


        Keyword Arguments:
            param_dict (dict): dict containing parameter and value in a given
                style

            original_style (str): style of the input format

            translated_style (str): style to which the parameters should be
                translated to.

        Returns:
            translated_params (dict-like): dict with the translated key and
                values for the input dict with additional information in
                self.details (see below).

        For example an input in ursgal style::

            {
                "precursor_mass_tolerance_unit": "da",
                "min_pep_length" : 8
            }

        can be converted to msgfplus style, yielding::

            {
                '-minLength' : 8,
                '-t' : 'Da'
            }

        the return object is a dict-like structure which holds additional
        detailed information accessible via self.details.
        For the example above, self.details looks like::

            {
                'min_pep_length': {
                    'original_key': 'min_pep_length',
                    'original_style': 'ursgal_style_1',
                    'original_value': 8,
                    'translated_key': '-minLength',
                    'translated_style': 'msgfplus_style_1',
                    'translated_value': 8
                },
                'precursor_mass_tolerance_unit': {
                    'original_key': 'precursor_mass_tolerance_unit',
                   'original_style': 'ursgal_style_1',
                   'original_value': 'da',
                   'translated_key': '-t',
                   'translated_style': 'msgfplus_style_1',
                   'translated_value': 'Da'
                }
            }

        """
        cannot_be_translated = "{0} for {1} cannot be translated into {2}"
        translated_params = UParmaDict()

        for original_key, original_value in param_dict.items():
            template_dict = {
                "original_style": original_style,
                "original_key": original_key,
                "original_value": original_value,
                # ========================
                "translated_style": translated_style,
                "translated_key": original_key,  # not translated
                "translated_value": original_value,  # not translated
            }

            _id = self.parameter2id[original_style].get(original_key, None)
            if _id is None:
                template_dict.update(
                    {
                        "was_translated": False,
                        "reason": f"Parameter {original_key} does not exist in {original_style}",
                    }
                )
                _name = original_key
            else:
                _name = self.parameters[_id].get("name", None)
                if _name is None:
                    raise TypeError(f"id {_id} has no name! Contact uparma team!")

                # ---
                translated_key = self.parameters[_id]["key_translations"].get(
                    translated_style,
                    None,
                )
                if translated_key is None:
                    _name = None  # will not be translated
                else:
                    if isinstance(translated_key, list) is True:
                        translated_key = tuple(translated_key)

                    parameter_data = self.parameters[_id]
                    org_value_translations = parameter_data["value_translations"].get(
                        original_style, []
                    )

                    trans_value_translations = parameter_data["value_translations"].get(
                        translated_style, []
                    )

                    is_parameter_collection = parameter_data.get(
                        "is_parameter_collection", False
                    )

                    """
                    {'original_key': '-t',
                    'original_style': 'msgfplus_style_1',
                    'original_value': 'Da',
                    'translated_key': '-t',
                    'translated_style': 'msfragger_style_3',
                    'translated_value': 'Da'}
                    [['da', 'Da']]
                    [['ppm', 1], ['da', 0]]

                    Starting from "Da".. finding 'da' .. looking up ['da', 0]
                    """
                    if is_parameter_collection:
                        translated_value = []
                        for local_p_dict in original_value:
                            _translated_sub_collection = self.translate(
                                local_p_dict,
                                original_style=original_style,
                                translated_style=translated_style,
                            )
                            translated_value.append(_translated_sub_collection)
                        was_translated = None

                    else:
                        translated_value = original_value
                        was_translated = False
                        for _uparma_v, _orgstyle_v in org_value_translations:
                            if _orgstyle_v == original_value:
                                for (
                                    _uparma_vt,
                                    _transtyle_v,
                                ) in trans_value_translations:
                                    if _uparma_v == _uparma_vt:
                                        translated_value = _transtyle_v
                                        was_translated = True

                    template_dict.update(
                        {
                            "translated_key": translated_key,
                            "translated_value": translated_value,
                            "translated_style": translated_style,
                            "was_translated": was_translated,
                            "is_parameter_collection": is_parameter_collection,
                        }
                    )
                if _name is not None:
                    translated_params[_name] = template_dict
        return translated_params

    def identify_parameters_triggering_rerun(self, params_list, style=None):
        """Identify from a list of params which one will trigger rerun


        Args:
            params_list (list of str) list with parameter names
            style (str)

        """
        if style is None:
            style = self.original_style
        params_that_trigger_rerun = []
        for param_name in params_list:
            if style not in self.parameter2id.keys():
                continue
            if isinstance(param_name, list) is False:
                listified_param_name = [param_name]

            for _pname in listified_param_name:
                _id = self.parameter2id[style].get(_pname, None)
                if _id is not None:
                    if self.parameters[_id].get("triggers_rerun", False) is True:
                        params_that_trigger_rerun.append(param_name)
                        break
        return params_that_trigger_rerun

    def get_default_params(self, style=None):
        """Fetch translated default params for a given style1.

        Args:
            style (str): Translation style, e.g. msfragger_style_3.

        Returns:
            dict: Dict with translated key and translated default value for
                the given style.

        """
        params = {}
        for key, value in self.parameters.items():
            translated_key = value["key_translations"].get(style, None)
            name = value["name"]
            if isinstance(translated_key, tuple) is True:
                translated_key = list(translated_key)
            if translated_key is None:
                continue
            else:
                if (
                    "value_translations" in value
                    and len(value["value_translations"]) > 0
                ):
                    if style in value["value_translations"]:
                        if value["default_value"] is not None:
                            translated_default = dict(
                                value["value_translations"][style]
                            ).get(
                                value["default_value"],
                                value["default_value"],
                            )
                        else:
                            translated_default = dict(
                                value["value_translations"][style]
                            )
                    else:
                        translated_default = value["default_value"]
                else:
                    translated_default = value["default_value"]
                params[name] = {
                    "original_key": value["name"],
                    "original_value": value["default_value"],
                    "translated_key": translated_key,
                    "translated_value": translated_default,
                }
        return params


class UParmaDict(dict):
    """
    UParma Dict

    Regular dict, yet offers original key and values that have been translated by
    the UParma translate function in self.details.
    """

    def __init__(self, *args, **kwargs):
        self.details = {}
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    UParma(refresh_jsons=True)
