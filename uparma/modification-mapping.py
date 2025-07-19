# Function for mapping modifications list from ursgal_style_1 to msfragger style
from pyteomics import mass

def format_MSFragger_Mods(Mods) -> str:
	"""Format mods into proper style, which can be printed into the params file for msfragger search.

        Args:
            Mods: List of Dicts, each representing 1 modification

        Returns:
           String with mods formatted for msfragger detailed_mass_offset param
    """
	umod = pyteomics.mass.unimod.Unimod()
	n_opt_mods = 0
	params = []

	def GetMass(ModDict):
		if "composition" not in ModDict.keys():
			composition = umod.by_name(ModDict["name"]).composition
		else:
			composition = ModDict["composition"]
		return mass.calculate_mass(composition=composition)

	def detailed_list(Mods):
	    detailed_mass_offsets = "0(aa=*)"
	    for mod_dict in mapped_mods["opt"]:
	        if not mod_dict.get("labile"):
	            regular_mods(mod_dict)
	        aa_to_append = mod_dict["aa"]
	        if aa_to_append == "*":
	        	aa_to_append = ""
	        pos_modifier = None
	        if mod_dict["position"] == "Prot-N-term":
	            pos_modifier = "["
	        elif mod_dict["position"] == "Prot-C-term":
	            pos_modifier = "]"
	        elif mod_dict["position"] == "N-term":
	            pos_modifier = "n"
	        elif mod_dict["position"] == "C-term":
	            pos_modifier = "c"
	        elif mod_dict["position"] == "any":
	            pass
	        else:
	            raise ValueError(
	                """
	            Unknown positional argument for given modification:
	            {0}
	            MSFragger cannot deal with this, please use one of the follwing:
	            any, Prot-N-term, Prot-C-term, N-term, C-term
	            """.format(
	                    mod_dict["org"]
	                )
	            )
	        if pos_modifier is not None:
	            aa_to_append = "{0}^{1}".format(pos_modifier, aa_to_append)
	        else:
	            aa_to_append = "{0}".format(aa_to_append)
	        
	        diag_ions_str = ""
	        if mod_dict["labile"]["diagnostic_ions"]:
	            diag_ions_str = "_d=" + ",".join(map(str, mod_dict["labile"]["diagnostic_ions"]))

	        pep_ions_str = ""
	        if mod_dict["labile"]["peptide_remainder_ions"]:
	            pep_ions_str = "_p=" + ",".join(map(str, mod_dict["labile"]["peptide_remainder_ions"]))

	        frag_ions_str = ""
	        if mod_dict["labile"]["fragment_remainder_ions"]:
	            pep_ions_str = "_f=" + ",".join(map(str, mod_dict["labile"]["fragment_remainder_ions"]))

	        detailed_mass_offsets = detailed_mass_offsets + f";{mod_dict["mass"]}(aa={aa_to_append}{diag_ions_str}{pep_ions_str}{frag_ions_str})"
		return detailed_mass_offsets

	def regular_mods(ModDict):
		FixedModParam = {
			"G": "add_G_glycine",
			"A": "add_A_alanine",
			"S": "add_S_serine",
			"P": "add_P_proline",
			"V": "add_V_valine",
			"T": "add_T_threonine",
			"C": "add_C_cystein",
			"L": "add_L_leucine",
			"I": "add_I_isoleucine",
			"N": "add_N_asparagine",
			"D": "add_D_aspartic_acid",
			"Q": "add_Q_glutamine",
			"K": "add_K_lysine",
			"E": "add_E_glutamic_acid",
			"M": "add_M_methionine",
			"H": "add_H_histidine",
			"F": "add_F_phenylalanine",
			"R": "add_R_arginine",
			"Y": "add_Y_tyrosine",
			"W": "add_W_tryptophan",
		}
		if ModDict["type"] == "fix":
			params.append(f"{FixedModParam[ModDict["aa"]]} = {GetMass(ModDict)}")
		elif ModDict["type"] == "opt":
			n_opt_mods += 1
			params.append(f"variable_mod_{n_opt_mods:02d} = {GetMass(ModDict)}")


	params.append(f"detailed_mass_offsets = {detailed_list(Mods)}")
	params.append("use_detailed_offsets = 1")
	return params