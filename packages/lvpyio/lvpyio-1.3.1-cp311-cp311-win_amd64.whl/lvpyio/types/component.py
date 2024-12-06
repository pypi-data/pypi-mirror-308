#############################################################################
#                                                                           #
#           Copyright (C) LaVision GmbH.  All Rights Reserved.              #
#                                                                           #
#############################################################################

from dataclasses import dataclass
import numpy as np
from .scale import Scale


@dataclass
class Component:
    scale: Scale
    planes: list[np.ndarray]

    @property
    def dtype(self):
        return self[0].dtype

    @property
    def shape(self):
        return self[0].shape

    def __repr__(self):
        size = len(self.planes)
        prefix = "1 plane" if size == 1 else f"{size} planes"
        return f"<{prefix}, scale={self.scale}>"

    def __len__(self):
        return len(self.planes)

    def __getitem__(self, index):
        return self.planes[index]


class Components(dict[str, Component]):
    def __repr__(self):
        size = len(self)
        keys = ", ".join(self.keys())
        prefix = "1 component" if size == 1 else f"{size} components"
        return f"<{prefix}: {keys}>"
