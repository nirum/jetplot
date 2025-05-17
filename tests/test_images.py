import numpy as np
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
