import numpy as np

PRECISION = 1e-24

# Small gaussian noise
get_gaussian_noise = lambda shape: np.random.normal(loc=0, scale=1e-15, size=shape)

def add_noise_to_stochastic_matrix(q: np.ndarray, weight: float = 1e-2) -> np.ndarray:
    """Given an input stochastic matrix `q`, sample a stochastic matrix `p` and then mix it with the input with a small weight `weight`, i.e. return q + weight * p."""
    p = np.random.dirichlet(np.ones(q.shape[1]), size=q.shape[0])
    noisy_matrix = q + weight * p
    noisy_matrix /= noisy_matrix.sum(axis=1, keepdims=True)
    return noisy_matrix