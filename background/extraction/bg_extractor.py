import numpy as np
from nptyping import Array

from background.extraction.abstact_bg_extractor import AbstractBGExtractor


class BGExtractor(AbstractBGExtractor):
    def extract_background(self, frame: Array[np.int]) -> Array[np.int]:
        pass
