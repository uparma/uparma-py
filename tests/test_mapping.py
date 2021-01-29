import uparma
import pytest

param = [
    {
        "_id": 1,
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

jsons = {
    ("general", "parameters"): "parameters.json",
    ("general", "styles"): "styles.json",
}
up = uparma.UParma(refresh_jsons=False, parameter_data=jsons)
up.jsons[("general", "parameters")] = param
up._parse_jsons()

test_data_list = [
    {
        "source_style": "msgfplus_style_1",
        "target_style": "msfragger_style_3",
        "input_dict": {"-t": "Da"},
        "results": {"precursor_mass_units": 0},
    },
    {
        "source_style": "msfragger_style_3",
        "target_style": "xtandem_style_1",
        "input_dict": {"precursor_mass_units": 0},
        "results": {"spectrum, parent monoisotopic mass error units": "Daltons"},
    },
    {
        "source_style": "ursgal_style_1",
        "target_style": "moda_style_1",
        "input_dict": {"precursor_mass_tolerance_unit": "ppm"},
        "results": {"PPMTolerance": "ppm"},
    },
]


@pytest.mark.parametrize("test_dict", test_data_list)
def test_mapping(test_dict):
    up.source_style = test_dict["source_style"]
    msgf_params = up.translate(
        test_dict["input_dict"],
        source_style=test_dict["source_style"],
        target_style=test_dict["target_style"],
    )

    assert msgf_params == test_dict["results"]

