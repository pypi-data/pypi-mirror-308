import numpy as np


def calculate_means(data: np.ndarray) -> np.ndarray:
    """Calculates the mean (average) of each row (sample) in a dataset.

    Args:
        data (np.ndarray): Array of numerical values.

    Returns:
        np.ndarray: Array of means for each row.

    Examples:
        >>> calculate_means(np.array([[10, 12, 14], [15, 16, 17]]))
        array([12., 16.])
    """
    return np.mean(data, axis=1)


def calculate_ranges(data: np.ndarray) -> np.ndarray:
    """Calculates the range (max - min) of each row (sample) in a dataset.

    Args:
        data (np.ndarray): Array of numerical values.

    Returns:
        np.ndarray: Array of ranges for each row.

    Examples:
        >>> calculate_ranges(np.array([[10, 12, 14], [15, 16, 17]]))
        array([4., 2.])
    """
    return np.ptp(data, axis=1).astype(float)


def calculate_standard_deviations(data: np.ndarray) -> np.ndarray:
    """Calculates the sample standard deviation for each row (sample) in the dataset.

    Args:
        data (np.ndarray): Array of numerical values, where each row is a sample.

    Returns:
        np.ndarray: Array of sample standard deviations for each row.

    Examples:
        >>> calculate_standard_deviations(np.array([[10, 12, 14], [15, 16, 17]]))
        array([2., 1.])
    """
    return np.std(data, axis=1, ddof=1)
