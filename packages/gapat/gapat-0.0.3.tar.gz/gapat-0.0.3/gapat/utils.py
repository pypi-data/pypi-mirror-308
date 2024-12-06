import scipy.io as sio


def load_mat(filename):
    """
    Load .mat file and return a dictionary with variable names as keys, and loaded matrices as values.

    Parameters
    ----------
    filename : str
        The path to the .mat file.

    Returns
    -------
    data : dict
        A dictionary with variable names as keys, and loaded matrices as values.
    """
    return sio.loadmat(filename)


def save_mat(filename, varname, data):
    """
    Save data to .mat file with the given variable name.

    Parameters
    ----------
    filename : str
        The path to the .mat file.
    varname : str
        The variable name to save the data to.
    data : np.ndarray
        The data to save.
    """
    sio.savemat(filename, {varname: data})
