# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv
import numpy as np

def add_border(bbox,border,shape):
    delta=[np.uint8((bbox[3]-bbox[0])+border[0]), np.uint8((bbox[4] - bbox[1]) +border[1] ),np.uint8((bbox[5] - bbox[2]) +border[2] )]
    new_bbox=np.zeros([6,],dtype=np.int16)
    for i in range(3):
        new_bbox[i]=bbox[i]-delta[i]
        if new_bbox[i]<0:new_bbox[i]=0
    for i in range(3):
        new_bbox[i+3]=bbox[i+3]+delta[i]
        if new_bbox[i+3]>=shape[i]:new_bbox[i+3]=shape[i]-1
    return list(new_bbox)

class Close(MorphoPlugin):
    """This plugin performs the closing morphological operator on each individual selected object.

    Parameters
    ----------
    objects:
        The selected or labeled objects on MorphoNet
    kernel_size:
        the amount of pixels closed
    background_only:
        if False the new shape of the object can overwrite the other objects in the segmentation
    """

    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Close.png")
        self.set_image_name("Close.png")
        self.set_name("Close : Close the selected objects")
        self.add_inputfield("kernel size",default=3)
        self.add_toggle("background only", default=True)
        self.set_parent("Shape Transform")


    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None

        from skimage.morphology import binary_closing

        kernel_size=int(self.get_inputfield("kernel size"))
        background_only = self.get_toggle("background only")

        for channel in dataset.get_channels(objects):#For each channels in selected object
            for t in dataset.get_times(objects):#For each time points in selected object
                data=dataset.get_seg(t,channel)
                if data is not None:
                    voxel_size = dataset.get_voxel_size(t)
                    anisotropy = voxel_size[2] / voxel_size[1]
                    printv("found anisotropy at " + str(anisotropy), 1)
                    cells_updated=[]
                    for o in dataset.get_objects_at(objects,t):
                        printv('Close the object ' + str(o.get_name()), 0)
                        bbox = self.dataset.get_regionprop("bbox", o)
                        kernel=[kernel_size,kernel_size,round(anisotropy*kernel_size)]
                        bbox=add_border(bbox,kernel,data.shape)
                        databox = data[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
                        close_box = np.uint8(binary_closing(databox==o.id,np.ones(kernel)))
                        if background_only:
                            where = databox==dataset.background  #WE ONLY FILL IN THE BACKGROUND
                        else:
                            where = close_box==1

                        # Update previous id
                        if o.id not in cells_updated: cells_updated.append(o.id)
                        previous_id = np.unique(databox[where])
                        for p in previous_id:
                            if p != 0 and p not in cells_updated:
                                printv('overlap with ' + str(p), 0)
                                cells_updated.append(p)

                        databox[where] = close_box[where]*o.id

                    if len(cells_updated)>0: #Update the segmentation
                        dataset.set_seg(t,data,channel=channel,cells_updated=cells_updated)

        self.restart() #Send data to morphonet
