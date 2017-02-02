import numpy as np
import matplotlib.pyplot as plt
from jetpack import plotmatrix

def test_plotmatrix():
    X = np.random.randn(5, 100)
    fig, axes = plotmatrix(X, labels=('a','b','c','d','e'), categories=np.random.randint(0,5,100))
    plt.show()

if __name__ == '__main__':
    test_plotmatrix()
