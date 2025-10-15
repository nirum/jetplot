import numpy as np
import pytest
from matplotlib import pyplot as plt

from jetplot import images


def test_img_corr_mode():
    data = np.eye(3)
    fig, ax = plt.subplots()
    im = images.img(data, mode="corr", fig=fig, ax=ax)

    # Check defaults for correlation mode
    assert im.get_cmap().name == "seismic"
    assert im.get_clim() == (-1, 1)

    # Colorbar should have been added
    assert len(fig.axes) == 2
    plt.close(fig)


def test_cmat_labels_and_colorbar():
    data = np.array([[0.0, 1.0], [1.0, 0.0]])
    fig, ax = plt.subplots()
    cb, returned_ax = images.cmat(data, labels=["a", "b"], cbar=True, fig=fig, ax=ax)

    assert returned_ax is ax
    assert [tick.get_text() for tick in ax.get_xticklabels()] == ["a", "b"]
    assert [tick.get_text() for tick in ax.get_yticklabels()] == ["a", "b"]
    assert len(fig.axes) == 2
    plt.close(fig)


def test_cmat_without_annotations():
    data = np.array([[0.2, 0.8], [0.1, 0.9]])
    fig, ax = plt.subplots()

    images.cmat(data, annot=False, fig=fig, ax=ax)

    assert len(ax.texts) == 0
    plt.close(fig)


def test_cmat_label_mismatch_raises():
    data = np.eye(2)
    fig, ax = plt.subplots()

    with pytest.raises(ValueError):
        images.cmat(data, labels=["short"], fig=fig, ax=ax)

    plt.close(fig)
