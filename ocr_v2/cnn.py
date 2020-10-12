import tensorflow as tf

class CNN:
    def __init__(self, height, width, maxpool, h_maxpool, last):
        # Extraction window height
        self._wnd_height = height

        # Extraction window width
        self._wnd_width = width

        # Window shift
        self._wnd_shift = width - 2

        # Number of all maxpool layers
        self._all_maxpool_layers = maxpool

        # Number of maxpool in horizontal dimension
        self._h_maxpool_layers = h_maxpool

        # Number of feature maps at the last conv layer
        self._last_filters = last

        # tbh idk what this is
        self._fv = int(WND_HEIGHT / (2 ** maxpool))

        # the number of features? idk
        self._n_features = self._fv * self._last_filters

    def start(self):
        pass
