import numpy as np

from lost_spc.constants import get_c4, get_d
from lost_spc.utils import get_sample_size

from .spc_values import calculate_means, calculate_ranges, calculate_standard_deviations


def calculate_control_limits(data: np.ndarray, chart_type: str = "X_R", z: int = 3) -> dict:
    """Calculates the control limits for different SPC charts (X̄, R, S, etc.).

    Args:
        data (np.ndarray): The data for which the control limits are to be calculated.
        chart_type (str): Type of chart ('X_R', 'R', 'S' or 'X_S'). Determines
                          the control limits' calculations.
        z (int): The number of standard deviations for control limits. Default is 3.

    Returns:
        dict: A dictionary containing the center line (CL), upper control limit (UCL),
              and lower control limit (LCL).

    Examples:
        >>> data = np.array([[10, 12, 14], [15, 16, 17]])
        >>> calculate_control_limits(data, chart_type='X_R')
        {'CL': 14.0, 'UCL': 17.069198123276216, 'LCL': 10.930801876723784}
    """
    # Bestimme m und n automatisch für NumPy-Arrays
    sample_size = get_sample_size(data)
    m = sample_size.m  # Stichprobengröße

    # Berechne die Kontrollgrenzen basierend auf dem Kartentyp
    if chart_type == "X_R":
        # X̄-R Karte: Mittelwert und Spannweite
        means = calculate_means(data)
        ranges = calculate_ranges(data)
        d = get_d(m)
        d2 = d.d2
        cl = np.mean(means)
        R_mean = np.mean(ranges)
        factor = z * (R_mean / d2) / np.sqrt(m)
        ucl = cl + factor
        lcl = cl - factor
    elif chart_type == "R":
        # R-Karte: Spannweite
        ranges = calculate_ranges(data)
        d = get_d(m)
        d2 = d.d2
        d3 = d.d3
        range_mean = np.mean(ranges)
        cl = range_mean
        factor = cl * z * d3 / d2
        ucl = cl + factor
        lcl = cl - factor
    elif chart_type == "S":
        # S-Karte: Standardabweichung
        std_devs = calculate_standard_deviations(data)
        c4 = get_c4(m)
        cl = np.mean(std_devs)
        factor = cl * z * np.sqrt(1 - c4**2) / c4
        ucl = cl + factor
        lcl = cl - factor
    elif chart_type == "X_S":
        # X̄-S Karte: Mittelwert und Standardabweichung
        means = calculate_means(data)
        std_devs = calculate_standard_deviations(data)
        X_mean = np.mean(means)
        s_i = std_devs
        s_mean = np.mean(s_i)
        c4 = get_c4(m)
        cl = X_mean
        factor = z * (s_mean / c4) / np.sqrt(m)
        ucl = cl + factor
        lcl = cl - factor
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")

    return {"CL": float(cl), "UCL": float(ucl), "LCL": float(lcl)}
