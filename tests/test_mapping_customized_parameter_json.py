import uparma
import pytest
import pprint

param = {
    ("general", "parameters"): [
        {
            "name": "precursor_mass_tolerance_unit",
            "description": "Precursor mass tolerance unit: available in ppm (parts-per-millon), da (Dalton) or mmu (Milli mass unit)",
            "default_value": "ppm",
            "value_type": "select",
            "tag": ["accuracy", "precursor"],
            "value_translations": {
                "msamanda_style_1": [["da", "Da"]],
                "msgfplus_style_1": [["da", "Da"]],
                "omssa_style_1": [["da", ""], ["ppm", "-teppm"]],
                "xtandem_style_1": [["da", "Daltons"]],
                "msfragger_style_3": [["ppm", 1], ["da", 0]],
            },
            "key_translations": {
                "ursgal_style_1": "precursor_mass_tolerance_unit",
                "moda_style_1": "PPMTolerance",
                "msamanda_style_1": "ms1_tol unit",
                "msgfplus_style_1": "-t",
                "omssa_style_1": "-teppm",
                "xtandem_style_1": "spectrum, parent monoisotopic mass error units",
                "msfragger_style_3": "precursor_mass_units",
            },
        }
    ]
}


test_data_list = [
    {
        "original_style": "msgfplus_style_1",
        "translated_style": "msfragger_style_3",
        "input_dict": {"-t": "Da"},
        "results": {
            "precursor_mass_tolerance_unit": {
                "translated_key": "precursor_mass_units",
                "translated_value": 0,
            }
        },
    },
    {
        "original_style": "msfragger_style_3",
        "translated_style": "xtandem_style_1",
        "input_dict": {"precursor_mass_units": 0},
        "results": {
            "precursor_mass_tolerance_unit": {
                "translated_key": "spectrum, parent monoisotopic mass error units",
                "translated_value": "Daltons",
            }
        },
    },
    {
        "original_style": "ursgal_style_1",
        "translated_style": "moda_style_1",
        "input_dict": {"precursor_mass_tolerance_unit": "ppm"},
        "results": {
            "precursor_mass_tolerance_unit": {
                "translated_key": "PPMTolerance",
                "translated_value": "ppm",
            }
        },
    },
    {
        "original_style": "ursgal_style_1",
        "translated_style": "moda_style_1",
        "input_dict": {
            "precursor_mass_tolerance_unit": "ppm",
            "precursor_mass_units": 0,
        },
        "results": {
            "precursor_mass_tolerance_unit": {
                "translated_key": "PPMTolerance",
                "translated_value": "ppm",
            },
            "precursor_mass_units": {
                "translated_key": "precursor_mass_units",
                "translated_value": 0,
            },
        },
    },
]


@pytest.mark.parametrize("test_dict", test_data_list)
def test_mapping(test_dict):
    up = uparma.UParma(parameter_data=param)
    up.original_style = test_dict["original_style"]
    translated_params = up.translate(
        test_dict["input_dict"],
        original_style=test_dict["original_style"],
        translated_style=test_dict["translated_style"],
    )
    pprint.pprint(translated_params)
    for uparma_key in translated_params.keys():
        assert all(
            r_items in translated_params[uparma_key].items()
            for r_items in test_dict["results"][uparma_key].items()
        )
