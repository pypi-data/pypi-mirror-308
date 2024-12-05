import logging
from typing import Union
from matchms.typing import SpectrumType


logger = logging.getLogger("matchms")

def require_retention_index(spectrum_in: SpectrumType) -> Union[SpectrumType, None]:
    """
    This function checks if the input spectrum has a 'retention_index' in its metadata.
    If the input spectrum is None or doesn't have a 'retention_index', the function returns None.
    Otherwise, it returns a clone of the input spectrum.

    Parameters:
    spectrum_in (SpectrumType): The input spectrum to check.

    Returns:
    SpectrumType: A clone of the input spectrum if it has a 'retention_index', None otherwise.
    """
    if spectrum_in is None:
        return None

    spectrum = spectrum_in.clone()

    retention_index = spectrum.get("retention_index", None)
    if retention_index is None:
        return None
    return spectrum
