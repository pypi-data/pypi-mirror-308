import logging
from rdkit import Chem
from rdkit.Chem.rdMolDescriptors import CalcMolFormula


logger = logging.getLogger("matchms")


def derive_formula_from_smiles(spectrum_in, overwrite=True):
    if spectrum_in is None:
        return None
    spectrum = spectrum_in.clone()
    if spectrum.get("formula") is not None:
        if overwrite is False:
            return spectrum

    formula = _get_formula_from_smiles(spectrum.get("smiles"))

    if formula is not None:
        if spectrum.get("formula") is not None:
            if spectrum.get("formula") != formula:
                logger.info("Overwriting formula. Original formula: %s New formula: %s",
                            spectrum.get('formula'), formula)
                spectrum.set("formula", formula)
        else:
            logger.info("Added formula from SMILES. New Formula: %s", formula)
            spectrum.set("formula", formula)
    else:
        logger.warning("SMILES: %s could not be interpreted by rdkit, so no formula was set")
    return spectrum


def _get_formula_from_smiles(smiles):
    if smiles is None:
        return None
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return CalcMolFormula(mol)
