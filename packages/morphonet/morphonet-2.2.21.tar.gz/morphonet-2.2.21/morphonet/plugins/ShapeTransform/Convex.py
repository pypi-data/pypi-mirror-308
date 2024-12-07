# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv
import numpy as np


def add_border(bbox,border,shape):
    delta=[np.uint8((bbox[3]-bbox[0])*border), np.uint8((bbox[4] - bbox[1]) * border ),np.uint8((bbox[5] - bbox[2]) * border )]
    new_bbox=np.zeros([6,],dtype=np.int16)
    for i in range(3):
        new_bbox[i]=bbox[i]-delta[i]
        if new_bbox[i]<0:new_bbox[i]=0
    for i in range(3):
        new_bbox[i+3]=bbox[i+3]+delta[i]
        if new_bbox[i+3]>=shape[i]:new_bbox[i+3]=shape[i]-1
    return list(new_bbox)


class Convex(MorphoPlugin):
    """This plugin computes the convex voxel hull of each individual selected object.

    Parameters
    ----------
    objects:
        The selected or labeled objects on MorphoNet
    background_only:
        if False the new shape of the object can overwrite the other objects in the segmentation
    """

    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Convex.png")
        self.set_image_name("Convex.png")
        self.set_name("Convex : Make selected objects convex")
        self.add_toggle("background only", default=True)
        self.set_parent("Shape Transform")


    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None

        from skimage.morphology import convex_hull_image

        background_only=self.get_toggle("background only")
        cancel=True
        for channel in dataset.get_channels(objects):#For each channels in selected object
            for t in dataset.get_times(objects):#For each time points in selected object
                data=dataset.get_seg(t,channel)
                if data is not None:
                    cells_updated=[]
                    for o in dataset.get_objects_at(objects,t):
                        printv('Convex the object ' + str(o.get_name()), 0)
                        bbox = self.dataset.get_regionprop("bbox", o)
                        bbox=add_border(bbox,border=0.4,shape=data.shape) #Increase of 40%
                        databox = data[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
                        convexbox = np.uint8(convex_hull_image(np.uint8(databox==o.id)))
                        if background_only:
                            where = databox==dataset.background  #WE ONLY FILL IN THE BACKGROUND
                        else:
                            where = convexbox==1

                        #Update previous id
                        if o.id not in cells_updated: cells_updated.append(o.id)
                        previous_id=np.unique(databox[where])
                        for p in previous_id:
                            if p!=0 and p not in cells_updated:
                                printv('overlap with ' + str(p), 0)
                                cells_updated.append(p)

                        #Update the shape
                        databox[where]=convexbox[where]*o.id

                    if len(cells_updated)>0: #Update the segmentation
                        dataset.set_seg(t,data,channel=channel,cells_updated=cells_updated)
                        cancel=False

        self.restart(cancel=cancel) #Send data to morphonet
