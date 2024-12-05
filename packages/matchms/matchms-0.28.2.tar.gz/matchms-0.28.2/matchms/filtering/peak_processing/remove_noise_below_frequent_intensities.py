import logging
import numpy as np
from matchms.Fragments import Fragments
from matchms.Spectrum import Spectrum


logger = logging.getLogger("matchms")


def remove_noise_below_frequent_intensities(spectrum: Spectrum,
                                            min_count_of_frequent_intensities: int = 5,
                                            noise_level_multiplier: float = 2.0):
    """Removes noise if intensities exactly match frequently

    When no noise filtering has been applied to a spectrum, many spectra show repeating intensities.
    From all intensities that repeat more than min_count_of_frequent_intensities the highest is selected.
    The noise level is set to this intensity * noise_level_multiplier. All fragments with an intensity below the noise
    level are removed.

    This filter was suggested by Tytus Mak.

    Parameters
    ----------
    spectrum
        Input spectrum.
    min_count_of_frequent_intensities:
        Minimum number of repeating intensities.
    noise_level_multiplier:
        From all intensities that repeat more than min_count_of_frequent_intensities the highest is selected.
    The noise level is set to this intensity * noise_level_multiplier.
    """
    if spectrum is None:
        return None
    spectrum = spectrum.clone()

    highest_frequent_peak = _select_highest_frequent_peak(spectrum.intensities, min_count_of_frequent_intensities)
    if highest_frequent_peak != -1:
        noise_threshold = highest_frequent_peak * noise_level_multiplier
        peaks_to_keep = spectrum.intensities > noise_threshold
        new_mzs, new_intensities = spectrum.mz[peaks_to_keep], spectrum.intensities[peaks_to_keep]
        spectrum.peaks = Fragments(mz=new_mzs, intensities=new_intensities)
        logger.info("Fragments removed with intensity below %s", noise_threshold)
    return spectrum


def _select_highest_frequent_peak(intensities,
                                  min_count_of_frequent_intensities=5):
    unique_values, counts = np.unique(intensities, return_counts=True)
    mask = counts >= min_count_of_frequent_intensities
    filtered_values = unique_values[mask]

    # Return the highest value from the filtered values, or -1 if no values meet the criteria
    if filtered_values.size > 0:
        return filtered_values.max()
    return -1
