# -*- coding: latin-1 -*-
from .MorphoPlugin import MorphoPlugin
__all__ = [
    'MorphoPlugin'
]

#from functions import  get_borders

defaultPlugins=[]


from .DeNovoSegmentation import defaultPlugins as DP
defaultPlugins+=DP

from .DeNovoSeed import defaultPlugins as DP
defaultPlugins+=DP

from .SegmentationFromSeeds import defaultPlugins as DP
defaultPlugins+=DP

from .SegmentationCorrection import defaultPlugins as DP
defaultPlugins+=DP

from .ShapeTransform import defaultPlugins as DP
defaultPlugins+=DP

from .EditTemporalLinks import defaultPlugins as DP
defaultPlugins+=DP

from .PropagateSegmentation import defaultPlugins as DM
defaultPlugins+=DM

