import numpy as np

def shear_to_probability(shear):

    shear_norm = (shear - np.mean(shear)) / np.std(shear)

    prob = 1 / (1 + np.exp(-shear_norm))

    return prob
