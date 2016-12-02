import numpy as np
import matplotlib.pyplot as plt
from jetpack import plotmatrix

def test_plotmatrix():
    X = np.random.randn(5, 100)
    fig, axes = plotmatrix(X, labels=('a','b','c','d','e'))
    plt.show()

if __name__ == '__main__':
    test_plotmatrix()
