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
    ): "https://raw.githubusercontent.com/uparma/uparma-lib/master/jsons/parameters.json",
    (
        "general",
        "styles",
    ): "https://raw.githubusercontent.com/uparma/uparma-lib/master/jsons/styles.json",
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

        source_style (str): Convenience when mapper is used to map from the
            same source style every time, in which case self.convert can be used
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
                ): [{"-id": ... }]
                (
                    "general",
                    "styles",
                ): [{"_id": ... }]


    """

    def __init__(
        self,
        refresh_jsons=False,
        source_style="ursgal_style_1",
        parameter_data=None,
    ):
        self.source_style = source_style
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

            if refresh_jsons is True:
                with requests.get(url) as req:
                    with open(full_path, "w") as j:
                        print(json.dumps(req.json(), indent=2, sort_keys=True), file=j)
                    self.jsons[url_id] = req.json()
            else:
                with open(full_path) as j:
                    self.jsons[url_id] = json.load(j)

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

    # def load_data(self, identifier=None, data_source=None):
    #     """

    #     Args:
    #         identifier: (tuple) for indexing the data_source
    #         data_source:  can be a url to json file or file path or json string

    #     Returns:

    #     """
    #     loaded = True
    #     # action depends on the type of data
    #     if isinstance(data_source, list):
    #         # this is a preformatted dictionary
    #         self.jsons[identifier] = data_source
    #     elif isinstance(data_source, Path):
    #         # path object pointing to a json file
    #         if data_source.exists():
    #             # this is a path string to a valid file
    #             with open(str(data_source)) as j:
    #                 self.jsons[identifier] = json.load(j)
    #         else:
    #             # this is a url
    #             pass
    #     elif isinstance(data_source, str):
    #         # data_source could be many things

    #         # url or file path
    #         fp = Path(data_source)

    #         try:
    #             if fp.exists():
    #                 # path as given exists
    #                 file_exists = True
    #             else:
    #                 # try using uparma location as parent
    #                 fp = base_path.parent.joinpath(fp.name)
    #                 if fp.exists():
    #                     # local file exists
    #                     file_exists = True
    #                 else:
    #                     file_exists = False
    #         except OSError:
    #             file_exists = False

    #         try:
    #             # if jason string parser will not fail
    #             parsed = json.loads(data_source)
    #         except json.JSONDecodeError:
    #             # not json string
    #             parsed = None

    #         if file_exists is True:
    #             # string is a filepath
    #             with open(str(fp)) as j:
    #                 self.jsons[identifier] = json.load(j)
    #         elif parsed is not None:
    #             # string translated as json
    #             self.jsons[identifier] = parsed
    #         else:
    #             # could be url
    #             try:
    #                 with requests.get(data_source) as req:
    #                     self.jsons[identifier] = req.json()
    #             except:
    #                 self.jsons[identifier] = None
    #                 loaded = False
    #     else:
    #         self.jsons[identifier] = None
    #         loaded = False

    #     return loaded

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
            for uparma_entry in self.jsons[url_id]:
                _id = uparma_entry["_id"]
                self.parameters[_id] = uparma_entry
                for key, value in uparma_entry["key_translations"].items():

                    if isinstance(value, list):
                        value = ", ".join(value)

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

    def convert(self, param_dict, target_style=None):
        """
        Convenient wrapper to translate params with the source style defined
        during init.

        Calls self.translate with source_style = self.source_style
        """
        return self.translate(
            param_dict, source_style=self.source_style, target_style=target_style
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
                   'source_value': 'da',
                   'target_key': '-t',
                   'target_style': 'msgfplus_style_1',
                   'target_value': 'Da'
                }
            }

        """
        cannot_be_translated = "{0} for {1} cannot be translated into {2}"

        translated_params = UParmaDict()
        for param_name, param_value in param_dict.items():
            source_key = param_name
            source_value = param_value
            template_dict = {
                "source_style": source_style,
                "source_key": source_key,
                "source_value": source_value,
                # ========================
                "target_style": target_style,
                "target_key": source_key,  # not translated
                "target_value": source_value,  # not translated
            }

            _id = self.parameter2id[source_style].get(source_key, None)

            if _id is None:
                translated_params[source_key] = source_value
                template_dict.update(
                    {
                        "was_translated": False,
                        "reason": "Parameter {source_key} does not exist in {source_style}".format(
                            source_key=source_key, source_style=source_style
                        ),
                    }
                )
                translated_params.details[source_key] = template_dict

            else:
                translated_key = self.parameters[_id]["key_translations"].get(
                    target_style,
                    None,
                )
                if translated_key is None:
                    translated_params[source_key] = source_value
                    template_dict.update(
                        {
                            "was_translated": False,
                            "reason": "Parameter {source_key} does not exist in {target_style}".format(
                                source_key=source_key,
                                target_style=target_style,
                            ),
                        }
                    )
                    translated_params.details[source_key] = template_dict
                else:

                    parameter_data = self.parameters[_id]
                    source_translations = parameter_data["value_translations"].get(
                        source_style, None
                    )
                    target_translations = parameter_data["value_translations"].get(
                        target_style, None
                    )

                    # convert param_value with source value_translations
                    source_value = None
                    if source_translations is None:
                        # no translator so keep value
                        source_value = param_value
                    else:
                        for key, value in source_translations:
                            if value == param_value:
                                source_value = key
                                break
                        if source_value is None:
                            source_value = param_value

                    target_value = None
                    if target_translations is None:
                        # no translator so keep value
                        target_value = source_value
                    else:
                        mapped = False
                        for key, value in target_translations:
                            if key == source_value:
                                target_value = value
                                mapped = True
                                break

                        if mapped is False and target_value is None:
                            target_value = source_value

                    template_dict.update(
                        {
                            "target_key": translated_key,
                            "target_value": target_value,
                            "target_style": target_style,
                            "was_translated": True,
                        }
                    )
                    translated_params.details[source_key] = template_dict
                    translated_params[translated_key] = target_value

        return translated_params

    def identify_parameters_triggering_rerun(self, params, style=None):
        if style is None:
            style = self.source_style
        params_that_trigger_rerun = []
        for param_name in params.keys():
            if style not in self.parameter2id.keys():
                continue
            _id = self.parameter2id[style].get(param_name, None)
            if _id is not None:
                if self.parameters[_id].get("triggers_rerun", False) is True:
                    params_that_trigger_rerun.append(param_name)

        return params_that_trigger_rerun

    def get_default_params(self, style=None):
        """Fetch translated default params for a given style1.

        Args:
            style (str): Translation style, e.g. msfragger_style_3.

        Returns:
            dict: Dict with translated key and translated default value for the given style.

        """
        params = {}
        for key, value in self.parameters.items():
            translated_key = value["key_translations"].get(style, None)
            if translated_key is not None:
                untranslated_default = value["default_value"]
                if (
                    "value_translations" in value
                    and len(value["value_translations"]) > 0
                ):
                    if style in value["value_translations"]:
                        translated_default = dict(
                            value["value_translations"][style]
                        ).get(
                            untranslated_default,
                            dict(value["value_translations"][style]),
                        )
                    else:
                        translated_default = untranslated_default
                else:
                    translated_default = untranslated_default
                params[translated_key] = translated_default
            else:
                continue
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
