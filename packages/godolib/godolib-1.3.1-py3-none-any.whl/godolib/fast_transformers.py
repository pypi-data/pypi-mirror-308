import numpy as np

def calculate_returns(array, period):
    """
    Calculate returns over a specified period for a 2D array of time series data.

    Parameters
    ----------
    array : np.ndarray
        A 2-dimensional NumPy array where each row represents a timestamp, and each column represents a separate time series.
    period : int
        The number of timestamps over which to calculate returns (e.g., 1 for daily returns, 7 for weekly returns).

    Returns
    -------
    np.ndarray
        A 2-dimensional NumPy array containing the calculated returns. The shape of the output array will be 
        (array.shape[0] - period, array.shape[1]).

    Raises
    ------
    ValueError
        - If `array` is not a NumPy ndarray.
        - If `array` is not 2-dimensional.
        - If `array` contains any NaN values.

    Notes
    -----
    The function calculates returns as the relative change in values between `current_values` and `previous_values` 
    (at `period` intervals) for each time series, computed as `(current_values / previous_values) - 1`.
    Returns are calculated for each timestamp from `period` onward, so the resulting array has fewer rows than 
    the input `array`.

    Example
    -------
    >>> import numpy as np
    >>> data = np.array([[100, 200], [110, 210], [115, 220], [120, 225]])
    >>> calculate_returns(data, period=1)
    array([[ 0.1       ,  0.05      ],
           [ 0.04545455,  0.04761905],
           [ 0.04347826,  0.02272727]])
    """
    if not isinstance(array, np.ndarray):
        raise ValueError('Input object must be an array')
    if array.ndim != 2:
        raise ValueError('Array must be bidimensional')
    if np.isnan(array).any():
        raise ValueError('Array contains NaNs')
    transformed_array = []
    for layer in range(period, array.shape[0]):
        previous_values = array[layer - period, :]
        current_values = array[layer, :]
        transformed_values = (current_values / previous_values) - 1
        transformed_array.append(transformed_values)
    return np.array(transformed_array)



def calculate_inverse_returns(array, period, initial_values):
    """
    Calculate the inverse returns to reconstruct the original time series values 
    from returns data over a specified period.

    Parameters
    ----------
    array : np.ndarray
        A 2-dimensional NumPy array where each row represents a timestamp, and each column represents a separate time series.
        The values in the array represent returns calculated over the specified period.
    period : int
        The number of timestamps over which the original returns were calculated.
        This parameter does not directly impact the reconstruction process but provides context for the calculation.
    initial_values : np.ndarray
        A 1-dimensional NumPy array containing the initial values for each time series at the start of reconstruction.

    Returns
    -------
    np.ndarray
        A 2-dimensional NumPy array containing the reconstructed time series values. 
        The shape of the output array will be (array.shape[0] + 1, array.shape[1]), 
        as it includes the initial values and all reconstructed values based on inverse returns.

    Raises
    ------
    ValueError
        - If `array` is not a NumPy ndarray.
        - If `array` is not 2-dimensional.
        - If `array` contains any NaN values.

    Notes
    -----
    The function reconstructs time series values by iteratively applying the inverse of the returns calculation:
    `recovered_values = (1 + current_values) * previous_values`.
    This approach accumulates the recovered values, beginning with `initial_values` and progressing row by row 
    through `array`.

    Example
    -------
    >>> import numpy as np
    >>> returns = np.array([[0.1, 0.05], [0.04, 0.03], [0.02, 0.01]])
    >>> initial_values = np.array([100, 200])
    >>> calculate_inverse_returns(returns, period=1, initial_values=initial_values)
    array([[100.        , 200.        ],
           [110.        , 210.        ],
           [114.4       , 216.3       ],
           [116.688     , 218.463     ]])
    """
    if not isinstance(array, np.ndarray):
        raise ValueError('Input object must be an array')
    if array.ndim != 2:
        raise ValueError('Array must be bidimensional')
    if np.isnan(array).any():
        raise ValueError('Array contains NaNs')
    recovered_values = initial_values.copy()
    for layer in range(array.shape[0]):
        current_values = array[[layer], :]
        previous_values = recovered_values[[layer], :]
        recovered_values = np.concatenate([recovered_values, (1 + current_values) * previous_values], axis=0)
    return recovered_values



def calculate_log_returns(array, period):
    """
    Calculate the log returns over a specified period for a 2D array of time series data.

    Parameters
    ----------
    array : np.ndarray
        A 2-dimensional NumPy array where each row represents a timestamp, and each column represents a separate time series.
    period : int
        The number of timestamps over which to calculate log returns 
        (e.g., 1 for daily log returns, 7 for weekly log returns).

    Returns
    -------
    np.ndarray
        A 2-dimensional NumPy array containing the calculated log returns. 
        The shape of the output array will be (array.shape[0] - period, array.shape[1]).

    Raises
    ------
    ValueError
        - If `array` is not a NumPy ndarray.
        - If `array` is not 2-dimensional.
        - If `array` contains any NaN values.

    Notes
    -----
    The function calculates log returns as the natural logarithm of the ratio of 
    `current_values` to `previous_values` (at `period` intervals) for each time series.
    Log returns are calculated from the timestamp at `period` onward, so the resulting 
    array has fewer rows than the input `array`.

    Example
    -------
    >>> import numpy as np
    >>> data = np.array([[100, 200], [110, 210], [115, 220], [120, 225]])
    >>> calculate_log_returns(data, period=1)
    array([[0.09531018, 0.04879016],
           [0.04575749, 0.04652002],
           [0.0432423 , 0.02247329]])
    """
    if not isinstance(array, np.ndarray):
        raise ValueError('Input object must be an array')
    if array.ndim != 2:
        raise ValueError('Array must be bidimensional')
    if np.isnan(array).any():
        raise ValueError('Array contains NaNs')
    transformed_array = []
    for layer in range(period, array.shape[0]):
        current_values = array[layer, :]
        previous_values = array[layer - period, :]
        transformed_array.append(np.log(current_values / previous_values))
    return np.array(transformed_array)



def calculate_inverse_log_returns(array, period, initial_values):
    """
    Calculate the inverse of log returns to reconstruct the original time series values 
    from log returns data over a specified period.

    Parameters
    ----------
    array : np.ndarray
        A 2-dimensional NumPy array where each row represents a timestamp, and each column represents a separate time series.
        The values in the array represent log returns calculated over the specified period.
    period : int
        The number of timestamps over which the original log returns were calculated.
        This parameter provides context but does not directly impact the reconstruction process.
    initial_values : np.ndarray
        A 1-dimensional NumPy array containing the initial values for each time series at the start of reconstruction.

    Returns
    -------
    np.ndarray
        A 2-dimensional NumPy array containing the reconstructed time series values. 
        The shape of the output array will be (array.shape[0] + 1, array.shape[1]), 
        as it includes the initial values and all reconstructed values based on the inverse log returns.

    Raises
    ------
    ValueError
        - If `array` is not a NumPy ndarray.
        - If `array` is not 2-dimensional.
        - If `array` contains any NaN values.

    Notes
    -----
    The function reconstructs time series values by iteratively applying the inverse of the log returns calculation:
    `recovered_values = np.exp(current_values) * previous_values`.
    This approach accumulates the recovered values, beginning with `initial_values` and progressing row by row 
    through `array`.

    Example
    -------
    >>> import numpy as np
    >>> log_returns = np.array([[0.09531018, 0.04879016], [0.04575749, 0.04652002], [0.0432423, 0.02247329]])
    >>> initial_values = np.array([100, 200])
    >>> calculate_inverse_log_returns(log_returns, period=1, initial_values=initial_values)
    array([[100.        , 200.        ],
           [110.        , 210.        ],
           [114.5       , 220.        ],
           [119.        , 225.        ]])
    """
    if not isinstance(array, np.ndarray):
        raise ValueError('Input object must be an array')
    if array.ndim != 2:
        raise ValueError('Array must be bidimensional')
    if np.isnan(array).any():
        raise ValueError('Array contains NaNs')
    recovered_values = initial_values.copy()
    for layer in range(array.shape[0]):
        current_values = array[[layer], :]
        previous_values = recovered_values[[layer], :]
        recovered_values = np.concatenate([recovered_values, np.exp(current_values) * previous_values])
    return recovered_values


def calculate_volatility_on_returns(array, window_size, min_periods=2, ddof=0):
    """
    Calculate rolling volatility (standard deviation) on returns for a 2D array of time series data over a specified window.

    Parameters
    ----------
    array : np.ndarray
        A 2-dimensional NumPy array where each row represents a timestamp, and each column represents a separate time series.
    window_size : int
        The size of the rolling window over which to calculate volatility.
    min_periods : int, optional
        Minimum number of observations in the window required to calculate volatility. 
        Default is 2.
    ddof : int, optional
        Delta degrees of freedom for the standard deviation calculation. 
        Default is 0, providing an unbiased estimate.

    Returns
    -------
    np.ndarray
        A 2-dimensional NumPy array containing the rolling volatility values, where each row corresponds to the 
        volatility at a given timestamp (starting from `min_periods`). The shape of the output array will be 
        (array.shape[0] - min_periods, array.shape[1]).

    Raises
    ------
    ValueError
        - If `array` is not a NumPy ndarray.
        - If `array` is not 2-dimensional.
        - If `array` contains any NaN values.

    Notes
    -----
    The function calculates volatility by computing the standard deviation of returns over a rolling window.
    For each timestamp (starting from `min_periods`), it takes a window of values of size `window_size` (or fewer if
    the beginning of the series is reached), then calculates the standard deviation across the window.
    This is repeated for each time series.

    Example
    -------
    >>> import numpy as np
    >>> returns = np.array([[0.01, 0.02], [0.015, 0.018], [0.012, 0.021], [0.014, 0.019], [0.013, 0.022]])
    >>> calculate_volatility_on_returns(returns, window_size=3)
    array([[0.00316228, 0.00141421],
           [0.00152753, 0.00152753],
           [0.00094281, 0.00152753]])
    """
    if not isinstance(array, np.ndarray):
        raise ValueError('Input object must be an array')
    if array.ndim != 2:
        raise ValueError('Array must be bidimensional')
    if np.isnan(array).any():
        raise ValueError('Array contains NaNs')
    transformed_values = []
    for layer in range(min_periods, array.shape[0]):
        rolling_window = array[:layer, :][-window_size:]
        transformed_values.append(np.std(rolling_window, axis=0, ddof=ddof))
    return np.array(transformed_values)



def calculate_volatility_on_prices(array, returns_period, window_size, returns_method='percentage', min_periods=2, ddof=0):
    """
    Calculate rolling volatility on price data over a specified window by first converting prices to returns.

    Parameters
    ----------
    array : np.ndarray
        A 2-dimensional NumPy array where each row represents a timestamp, and each column represents a separate time series.
    returns_period : int
        The period over which to calculate returns (e.g., 1 for daily returns, 7 for weekly returns).
    window_size : int
        The size of the rolling window over which to calculate volatility.
    returns_method : str, optional
        The method for calculating returns, either 'percentage' or 'logarithmic'. Default is 'percentage'.
    min_periods : int, optional
        Minimum number of observations in the window required to calculate volatility. Default is 2.
    ddof : int, optional
        Delta degrees of freedom for the standard deviation calculation. Default is 0, providing an unbiased estimate.

    Returns
    -------
    np.ndarray
        A 2-dimensional NumPy array containing the rolling volatility values. 
        The shape of the output array will be (returns_array.shape[0] - min_periods, array.shape[1]).

    Raises
    ------
    ValueError
        - If `array` is not a NumPy ndarray.
        - If `array` is not 2-dimensional.
        - If `array` contains any NaN values.
        - If `returns_method` is not 'percentage' or 'logarithmic'.

    Notes
    -----
    The function first converts price data into returns, then calculates volatility (standard deviation) over a rolling 
    window for each time series. Returns can be calculated using either percentage or logarithmic methods:
    - 'percentage' calculates returns as `(current_values / previous_values) - 1`.
    - 'logarithmic' calculates returns as `log(current_values / previous_values)`.
    
    The function then calculates volatility by taking the standard deviation of returns within the rolling window for 
    each timestamp (starting from `min_periods`).

    Example
    -------
    >>> import numpy as np
    >>> prices = np.array([[100, 200], [110, 210], [115, 220], [120, 225], [125, 230]])
    >>> calculate_volatility_on_prices(prices, returns_period=1, window_size=3, returns_method='percentage')
    array([[0.09534626, 0.04714045],
           [0.04082483, 0.04692723],
           [0.03902275, 0.02236068]])
    """
    if not isinstance(array, np.ndarray):
        raise ValueError('Input object must be an array')
    if array.ndim != 2:
        raise ValueError('Array must be bidimensional')
    if np.isnan(array).any():
        raise ValueError('Array contains NaNs')
    if returns_method == 'percentage':
        returns_array = calculate_returns(array=array, period=returns_period)
    elif returns_method == 'logarithmic':
        returns_array = calculate_log_returns(array=array, period=returns_period)
    else:
        raise ValueError("returns_method must be either 'percentage' or 'logarithmic'.")
    transformed_values = []
    for layer in range(min_periods, returns_array.shape[0]):
        rolling_window = returns_array[:layer, :][-window_size:, :]
        transformed_values.append(np.std(rolling_window, axis=0, ddof=ddof))
    return np.array(transformed_values)



def standardize(array, mean, std):
    """
    Standardize a 2D array by subtracting the mean and dividing by the standard deviation.

    Parameters
    ----------
    array : np.ndarray
        A 2-dimensional NumPy array where each row represents a timestamp, and each column represents a separate time series.
    mean : np.ndarray or float
        The mean value(s) used for standardization. This can be either:
        - A single float, in which case the same mean is applied to all elements of `array`.
        - A 1-dimensional array of shape (array.shape[1],), in which case each column is standardized using its respective mean.
    std : np.ndarray or float
        The standard deviation value(s) used for standardization. This can be either:
        - A single float, in which case the same standard deviation is applied to all elements of `array`.
        - A 1-dimensional array of shape (array.shape[1],), in which case each column is standardized using its respective standard deviation.

    Returns
    -------
    np.ndarray
        A 2-dimensional NumPy array containing the standardized values of the input `array`, 
        with the same shape as `array`.

    Raises
    ------
    ValueError
        - If `array` is not a NumPy ndarray.
        - If `array` is not 2-dimensional.
        - If `array` contains any NaN values.

    Notes
    -----
    Standardization is performed by applying the formula `(array - mean) / std` element-wise. 
    Each column is standardized independently if `mean` and `std` are 1-dimensional arrays with 
    a shape matching the number of columns in `array`.

    Example
    -------
    >>> import numpy as np
    >>> data = np.array([[100, 200], [110, 210], [115, 220]])
    >>> mean = np.array([105, 205])
    >>> std = np.array([5, 10])
    >>> standardize(data, mean, std)
    array([[-1., -0.5],
           [ 1.,  0.5],
           [ 2.,  1.]])
    """
    if not isinstance(array, np.ndarray):
        raise ValueError('Input object must be an array')
    if array.ndim != 2:
        raise ValueError('Array must be bidimensional')
    if np.isnan(array).any():
        raise ValueError('Array contains NaNs')
    standardized_array = (array - mean) / std
    return standardized_array




def inverse_standardize(array, std, mean):
    """
    Reverse the standardization process on a 2D array by multiplying by the standard deviation 
    and adding the mean to recover the original values.

    Parameters
    ----------
    array : np.ndarray
        A 2-dimensional NumPy array representing standardized data, where each row represents 
        a timestamp, and each column represents a separate time series.
    std : np.ndarray or float
        The standard deviation(s) used in the original standardization. This can be either:
        - A single float, in which case the same standard deviation is applied to all elements of `array`.
        - A 1-dimensional array of shape (array.shape[1],), in which case each column is rescaled using its respective standard deviation.
    mean : np.ndarray or float
        The mean value(s) used in the original standardization. This can be either:
        - A single float, in which case the same mean is applied to all elements of `array`.
        - A 1-dimensional array of shape (array.shape[1],), in which case each column is shifted using its respective mean.

    Returns
    -------
    np.ndarray
        A 2-dimensional NumPy array containing the recovered values with the same shape as `array`.

    Raises
    ------
    ValueError
        - If `array` is not a NumPy ndarray.
        - If `array` is not 2-dimensional.
        - If `array` contains any NaN values.

    Notes
    -----
    This function reverses the standardization transformation applied using `(array - mean) / std`, 
    by using the formula `array * std + mean`. Each column is transformed independently if `mean` 
    and `std` are arrays with shapes matching the number of columns in `array`.

    Example
    -------
    >>> import numpy as np
    >>> standardized_data = np.array([[-1., -0.5], [1., 0.5], [2., 1.]])
    >>> mean = np.array([105, 205])
    >>> std = np.array([5, 10])
    >>> inverse_standardize(standardized_data, std, mean)
    array([[100., 200.],
           [110., 210.],
           [115., 220.]])
    """
    if not isinstance(array, np.ndarray):
        raise ValueError('Input object must be an array')
    if array.ndim != 2:
        raise ValueError('Array must be bidimensional')
    if np.isnan(array).any():
        raise ValueError('Array contains NaNs')
    transformed_values = array * std + mean
    return transformed_values


def window(array, n_past, n_future):
    """
    Generate sliding windows of past and future values from a 2D time series array.

    Parameters
    ----------
    array : np.ndarray
        A 2-dimensional NumPy array where each row represents a timestamp, and each column represents a separate time series.
    n_past : int
        The number of past timestamps to include in each window.
    n_future : int
        The number of future timestamps to predict for each window.

    Returns
    -------
    tuple of np.ndarray
        - X: A 3-dimensional array of shape (num_samples, n_past, num_features), containing the past values for each window.
        - Y: A 3-dimensional array of shape (num_samples, n_future, num_features), containing the future values to predict for each window.
        `num_samples` is calculated as `array.shape[0] - n_past`, and `num_features` is the number of columns in `array`.

    Raises
    ------
    ValueError
        - If `array` is not a NumPy ndarray.
        - If `array` is not 2-dimensional.
        - If `array` contains any NaN values.
        - If `n_past` or `n_future` is too large relative to the number of rows in `array`.

    Notes
    -----
    This function creates a sliding window over the time series data, where:
    - `X` contains `n_past` consecutive past values for each feature.
    - `Y` contains the values at the next `n_future` timestamps for each feature.
    
    This structure is useful for training models on time series data where each input sample consists 
    of a sequence of past values and each target output consists of a sequence of future values.

    Example
    -------
    >>> import numpy as np
    >>> data = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
    >>> X, Y = window(data, n_past=2, n_future=1)
    >>> X
    array([[[1., 2.],
            [3., 4.]],
           [[3., 4.],
            [5., 6.]],
           [[5., 6.],
            [7., 8.]]])
    >>> Y
    array([[[5., 6.]],
           [[7., 8.]],
           [[9., 10.]]])
    """
    if not isinstance(array, np.ndarray):
        raise ValueError('Input object must be an array')
    if array.ndim != 2:
        raise ValueError('Array must be bidimensional')
    if np.isnan(array).any():
        raise ValueError('Array contains NaNs')
    if array.shape[0] <= n_past:
        raise ValueError('Input shape not big enough for given n_past')
    if array.shape[0] <= n_future:
        raise ValueError('Input shape not big enough for given n_future')
    X = np.zeros((array.shape[0] - n_past, n_past, array.shape[1]))
    Y = np.zeros((array.shape[0] - n_past, n_future, array.shape[1]))
    for layer in range(array.shape[1]):
        layer_array = array[:, layer]
        for step in range(array.shape[0] - n_past):
            X[step, :, layer] = layer_array[step:step + n_past]
            Y[step, :, layer] = layer_array[step + n_past:step + n_past + n_future]
    return X, Y

def inverse_window(X, Y):
    """
    Reconstruct the original time series from sliding window inputs and outputs.

    Parameters
    ----------
    X : np.ndarray
        A 3-dimensional array of shape (num_samples, n_past, num_features), where each slice along the first axis 
        represents a sequence of past values for a time series.
    Y : np.ndarray
        A 3-dimensional array of shape (num_samples, n_future, num_features), where each slice along the first axis 
        represents the corresponding future values to predict for each sequence in `X`.

    Returns
    -------
    np.ndarray
        A 2-dimensional NumPy array of shape (num_samples + n_past, num_features), 
        which approximates the original time series before windowing.

    Raises
    ------
    ValueError
        - If the first dimension of `X` does not match that of `Y`.
        - If the third dimension of `X` does not match that of `Y`.

    Notes
    -----
    This function reconstructs the original time series from windowed input (X) and output (Y) arrays, by taking 
    the initial sequence from `X` and appending values from `Y`. It concatenates overlapping windows to 
    recompose the original data. This reconstruction assumes that the initial values are stored in `X` and 
    subsequent target values are stored in `Y`, where each sequence in `Y` overlaps with the next.

    Example
    -------
    >>> import numpy as np
    >>> X = np.array([[[1, 2], [3, 4]], [[3, 4], [5, 6]], [[5, 6], [7, 8]]])
    >>> Y = np.array([[[5, 6]], [[7, 8]], [[9, 10]]])
    >>> inverse_window(X, Y)
    array([[1., 2.],
           [3., 4.],
           [5., 6.],
           [7., 8.],
           [9., 10.]])
    """
    if X.shape[0] != Y.shape[0]:
        raise ValueError('Shapes at index 0 are incongruous')
    if X.shape[2] != Y.shape[2]:
        raise ValueError('Shapes at index 2 are incongruous')
    reconstructed_array = np.zeros((X.shape[0] + X.shape[1], X.shape[2]))
    for layer in range(X.shape[2]):
        current_array = np.concatenate(
            [X[0, :, layer].reshape(-1, 1), 
             np.concatenate([Y[0, :, layer].reshape(-1, 1), Y[1:, -1, layer].reshape(-1, 1)], axis=0)], axis=0
        )
        reconstructed_array[:, layer] = current_array.reshape(-1,)
    return reconstructed_array
