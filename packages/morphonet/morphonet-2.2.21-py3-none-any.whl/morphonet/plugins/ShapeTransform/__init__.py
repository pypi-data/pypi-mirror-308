
# -*- coding: latin-1 -*-
defaultPlugins=[]

from .Convex import Convex
defaultPlugins.append(Convex())

from .Erode import Erode
defaultPlugins.append(Erode())

from .Dilate import Dilate
defaultPlugins.append(Dilate())

from .Close import Close
defaultPlugins.append(Close())

from .Open import Open
defaultPlugins.append(Open())

from .Deform import Deform
defaultPlugins.append(Deform())







