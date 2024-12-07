import numpy as np
from scipy.spatial.distance import cdist
from .information import kl_divergence


def expected_distortion(
    px: np.ndarray, qxhat_x: np.ndarray, dist_mat: np.ndarray
) -> float:
    """Compute the expected distortion $E[D[X, \\hat{X}]]$ of a joint distribution defind by $P(X)$ and $P(\\hat{X}|X)$, where

    $D[X, \hat{X}] = \sum_x p(x) \sum_{\\hat{x}} p(\\hat{x}|x) \\cdot d(x, \\hat{x})$

    Args:
        px: array of shape `|X|` the prior probability of an input symbol (i.e., the source)

        qxhat_x: array of shape `(|X|, |X_hat|)` the probability of an output symbol given the input

        dist_mat: array of shape `(|X|, |X_hat|)` representing the distoriton matrix between the input alphabet and the reconstruction alphabet.
    """
    return np.sum(px * (qxhat_x * dist_mat))


# Pairwise distortion measures


def hamming(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Get a hamming distortion matrix for between two arrays of n-dimensional points."""
    return cdist(x, y, "hamming")


def quadratic(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Compute the L2 distance between two arrays of n-dimensional points."""
    return cdist(x, y)


def ib_kl(py_x: np.ndarray, qy_xhat: np.ndarray) -> np.ndarray:
    """Compute the IB distortion matrix, the KL divergence between p(y|x) and q(y|xhat), in nats."""
    # D[p(y|x) || q(y|xhat)],
    # input shape `(x, xhat, y)`, output shape `(x, xhat)`
    return kl_divergence(py_x[:, None, :], qy_xhat[None, :, :], axis=2)


def ib_bin_se(py_x: np.ndarray, qy_xhat: np.ndarray) -> np.ndarray:
    # [ p(y=1|x) - q(y=1|xhat) ]^2
    result = np.array([[(py[1] - qy[1]) ** 2 for qy in qy_xhat] for py in py_x])
    return result


def feature_loss(
    fx: np.ndarray, fxhat: np.ndarray, weights: np.ndarray = None
) -> np.ndarray:
    # 1/|f| sum_{i}^{|f|} w_i [ f(x)_i - f(\hat{x})_i ]^2
    # if fx.shape != fxhat.shape:
    # raise ValueError

    num_features = fx.shape[1]
    if weights is None:
        weights = np.ones(num_features)

    result = (
        np.sum(
            # `(x,xhat,f)`
            weights * (fx[:, None, :] - fxhat[None, :, :]) ** 2,
            axis=2,
        )
        / num_features
    )

    return result


def ib_mse(
    py_x: np.ndarray,
    qy_xhat: np.ndarray,
    fx: np.ndarray,
    fxhat: np.ndarray,
    alpha: float,
    weights: np.ndarray,
):
    # breakpoint()
    return (
        alpha * ib_kl(py_x, qy_xhat)
        # alpha * ib_bin_se(py_x, qy_xhat)
        + (1 - alpha) * feature_loss(fx, fxhat, weights)
    )
