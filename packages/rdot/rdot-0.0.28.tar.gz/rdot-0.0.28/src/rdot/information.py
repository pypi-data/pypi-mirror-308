import warnings
import numpy as np
from .probability import joint
from scipy.stats import entropy


def entropy_bits(p: np.ndarray, axis=None) -> float:
    """Compute entropy of p, $H(X) = - \sum_x p(x) \log p(x)$, in bits."""
    return entropy(p, base=2, axis=axis)


def mutual_info(pxy: np.ndarray) -> float:
    """Compute mutual information, $I(X;Y)$ in bits.

    Args:
        pxy: 2D numpy array of shape `(x, y)`
    """
    return (
        entropy_bits(pxy.sum(axis=0))
        + entropy_bits(pxy.sum(axis=1))
        - entropy_bits(pxy)
    )


def kl_divergence(p: np.ndarray, q: np.ndarray, axis=None, base=np.e) -> float:
    """Compute KL divergence (in nats by defaut) between p and q, $D_{KL}[p \| q]$.

    Args:
        p: np.ndarray, lhs of KL divergence

        q: np.ndarray, rhs of KL divergence
    """
    return entropy(
        p,
        q,
        axis=axis,
        base=base,
    )


# Common pattern for rate-distortion optimizations
def information_cond(pA: np.ndarray, pB_A: np.ndarray) -> float:
    """Compute the mutual information $I(A;B)$ from a joint distribution defind by $P(A)$ and $P(B|A)$

    Args:
        pA: array of shape `|A|` the prior probability of an input symbol (i.e., the source)

        pB_A: array of shape `(|A|, |B|)` the probability of an output symbol given the input
    """
    pab = joint(pY_X=pB_A, pX=pA)
    mi = mutual_info(pxy=pab)
    if mi < 0.0 and not np.isclose(mi, 0.0, atol=1e-5):
        raise Exception
    return mi


def NID(pW_X: np.ndarray, pV_X: np.ndarray, pX: np.ndarray):
    """Compute Normalized Informational Distance (NID)."""
    if len(pX.shape) == 1:
        pX = pX[:, None]
    elif pX.shape[0] == 1 and pX.shape[1] > 1:
        pX = pX.T
    pXW = pW_X * pX
    pXV = pV_X * pX
    pWV = pXW.T @ (pV_X)
    pW = pXW.sum(axis=0)
    pV = pXV.sum(axis=0)    
    score = 1 - mutual_info(pWV) / (np.max([entropy_bits(pW), entropy_bits(pV)]))
    if score < 0 or score > 1 and not (np.isclose(score, 0) or np.isclose(score, 1)):
        # NID is bounded to [0,1].
        warnings.warn(f"NID falls outside of [0,1]: {score}.")
    return score

def gNID(pW_X: np.ndarray, pV_X: np.ndarray, pX: np.ndarray):
    """Compute Generalized Normalized Informational Distance (gNID, in Zaslavsky et al. 2018, SI, Section 3.2) between two encoders. Code credit: https://github.com/nogazs/ib-color-naming/blob/master/src/tools.py#L94

    Args:
        pW_X: first encoder of shape `(|meanings|, |words|)`

        pV_X: second encoder of shape `(|meanings|, |words|)`

        pX: prior over source variables of shape `(|meanings|,)`
    """
    if len(pX.shape) == 1:
        pX = pX[:, None]
    elif pX.shape[0] == 1 and pX.shape[1] > 1:
        pX = pX.T
    pXW = pW_X * pX
    pWV = pXW.T @ (pV_X)
    pWW = pXW.T @ (pW_X)
    pVV = (pV_X * pX).T @ (pV_X)
    score = 1 - mutual_info(pWV) / (np.max([mutual_info(pWW), mutual_info(pVV)]))
    if score < 0:
        # N.B.: gNID is not necessarily non-negative (See SI, Section 3.2, paragraph 2.)
        warnings.warn(f"Negative gNID: {score}.")    
    return score
