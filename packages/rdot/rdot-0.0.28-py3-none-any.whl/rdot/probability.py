import numpy as np
from scipy.special import softmax, logsumexp
from .noise import PRECISION

##############################################################################
# Helper functions for encoding discrete probability distributions. Code credit belongs to N. Zaslavsky: https://github.com/nogazs/ib-color-naming/blob/master/src/tools.py
##############################################################################



def marginal(pXY, axis=1):
    """Compute $p(y) = \sum_x p(x,y)$

    Args:
        pXY: a numpy array of shape `(|X|, |Y|)`

    Returns:
        pY: (axis = 0) or pX (default, axis = 1)
    """
    return pXY.sum(axis)


def conditional(pXY):
    """Compute $p(y|x) = \frac{p(x,y)}{p(x)}$

    Args:
        pXY: a numpy array of shape `(|X|, |Y|)`

    Returns:
        pY_X: a numpy array of shape `(|X|, |Y|)`
    """
    pX = pXY.sum(axis=1, keepdims=True)
    return np.where(pX > PRECISION, pXY / pX, 1 / pXY.shape[1])


def joint(pY_X, pX):
    """Compute $p(x,y) = p(y|x) \cdot p(x) $

    Args:
        pY_X: a numpy array of shape `(|X|, |Y|)`

        pX: a numpy array `|X|`
    Returns:
        pXY: a numpy array of the shape `(|X|, |Y|)`
    """
    return pY_X * pX[:, None]


def marginalize(pY_X, pX):
    """Compute $p(y) = \sum_x p(y|x) \cdot p(x)$

    Args:
        pY_X: a numpy array of shape `(|X|, |Y|)`

        pX: a numpy array of shape `|X|`

    Returns:
        pY: a numpy array of shape `|Y|`
    """
    return pY_X.T @ pX


def bayes(pY_X, pX):
    """Compute $p(x|y) = \frac{p(y|x) \cdot p(x)}{p(y)}$
    Args:
        pY_X: a numpy array of shape `(|X|, |Y|)`
    """
    pXY = joint(pY_X, pX)
    pY = marginalize(pY_X, pX)
    return np.where(pY > PRECISION, pXY / pY, 1 / pXY.shape[0]).T

def log_bayes(pY_X, pX):
    """Compute bayes rule, but perform the operation in logspace to prevent underflow."""
    ln_py_x = np.log(pY_X)
    ln_px = np.log(pX)

    ln_pxy = ln_px[:, None] + ln_py_x
    ln_py = logsumexp(ln_pxy, axis=0)
    ln_px_y = ln_pxy.T - ln_py[:, None]
    px_y = np.exp(ln_px_y)

    return px_y


def random_stochastic_matrix(shape: tuple[int], gamma=1e-10) -> np.ndarray:
    """Initialize a stochastic matrix (2D array) that sums to 1. along the rows."""
    energies = gamma * np.random.normal(size=shape)
    return softmax(energies, axis=1)
