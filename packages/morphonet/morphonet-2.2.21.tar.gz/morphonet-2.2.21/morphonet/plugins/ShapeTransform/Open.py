# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv
import numpy as np


class Open(MorphoPlugin):
    """This plugin perform the opening morphological operator on each individual selected object.

    Parameters
    ----------
    objects:
        The selected or labeled objects on MorphoNet
    kernel_size:
        the amount of pixels opened
    """

    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Open.png")
        self.set_image_name("Open.png")
        self.set_name("Open : Open the selected objects")
        self.add_inputfield("kernel size",default=3)
        self.set_parent("Shape Transform")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None

        from skimage.morphology import binary_opening

        kernel_size = int(self.get_inputfield("kernel size"))
        for channel in dataset.get_channels(objects):#For each channels in selected object
            for t in dataset.get_times(objects):#For each time points in selected object
                data=dataset.get_seg(t,channel)
                if data is not None:
                    voxel_size = dataset.get_voxel_size(t)
                    anisotropy = voxel_size[2] / voxel_size[1]
                    printv("found anisotropy at " + str(anisotropy), 1)
                    cells_updated=[]
                    for o in dataset.get_objects_at(objects,t):
                        printv('Open the object ' + str(o.get_name()), 0)
                        bbox = self.dataset.get_regionprop("bbox", o)
                        databox = data[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
                        open_box = np.uint8(binary_opening(databox==o.id,np.ones([kernel_size,kernel_size,round(anisotropy*kernel_size)])))
                        databox[databox==o.id] = dataset.background
                        databox[open_box == 1] = o.id
                        cells_updated.append(o.id)

                    if len(cells_updated)>0: #Update the segmentation
                        dataset.set_seg(t,data,channel=channel,cells_updated=cells_updated)

        self.restart() #Send data to morphonet
