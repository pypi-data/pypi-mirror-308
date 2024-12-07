# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from ..functions import  read_time_points
from morphonet.tools import printv
import numpy as np

def match_label(nb_cells,new_data,data):  #  FOR EACH LABEL in the new data WE FIND THE CORRESPONDING ORIGINAL LABEL
    for c in range(1, nb_cells + 1):
        mask = new_data == c
        original_cells, nb = np.unique(data[mask], return_counts=True)  #
        best=0
        corresponding_cell = None
        for i in range(len(original_cells)):
            if original_cells[i] > 0 and nb[i]>best:
                corresponding_cell = original_cells[i]
                best= nb[i]
        if corresponding_cell is not None:
            data[mask] = corresponding_cell
        else:
            printv(f"Error correspoding cell is none for label {c}", 1)

class Fusoc(MorphoPlugin):
    """ This plugin performs the fusion of the object which are in contact.
    It uses apply the connected components method in 3D.
    \n
    This plugin can be used:

    * on a whole image by not selecting any object. You have in this case to specify the channel

    * only on selected objects. With the parameter bounding_box, you can choose to also automatically include in the fusion the objects that are inside the bounding box of each selected objects.


    Parameters
    ----------
    objects:
        The selected or labeled objects on MorphoNet
    channel:
        The segmented channel when no object is selected
    bounding box:
        True will automatically include any objects in the bounding box of the selected ones.

    """

    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Fusoc.png")
        self.set_image_name("Fusoc.png")
        self.set_name("Fusoc : Fuse the connected components")
        self.add_inputfield("time points", default="current")
        self.add_inputfield("channel", default=0)
        self.add_toggle("bounding box", default=True)
        self.set_parent("Segmentation Correction")


    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects, objects_require=False):
            return None
        from skimage.measure import label
        # If objects are selected, we run cellpose on the global bounding box of the object
        cancel=True
        if len(objects) >= 1 and objects[0] != "":
            bounding_box = self.get_toggle("bounding box")
            for channel in dataset.get_channels(objects):  # For each channels in selected object
                for t in dataset.get_times(objects):
                    data = dataset.get_seg(t, channel)  # Get segmentations at the time
                    if data is None:
                        printv(f"ERROR: could not get segmentation at {t},{channel} ", 1)
                    else:

                        objects_to_fused=[]
                        if bounding_box: #We add objects that are in the boudning box of each selected object
                            for o in dataset.get_objects_at(objects, t):
                                bbox = dataset.get_regionprop("bbox", o)
                                data_box = data[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
                                objects_in_bb = np.unique(data_box)
                                objects_in_bb = objects_in_bb[objects_in_bb != dataset.background]
                                for new_o in objects_in_bb:
                                    ob=dataset.get_object(t,new_o,channel)
                                    if new_o not in  objects_to_fused:
                                        printv("add close object " + str(new_o) + " at " + str(t), 1)
                                        objects_to_fused.append(ob)
                        else:
                            for o in dataset.get_objects_at(objects, t):
                                printv("add object " + str(o.id) + " at " + str(o.t), 1)
                                objects_to_fused.append(o)

                        if len(objects_to_fused)>1:
                            #Compute the global bounding box
                            bbox = None
                            for o in objects_to_fused:
                                bb = dataset.get_regionprop("bbox", o)
                                if bbox is None:bbox=bb
                                else:  bbox = [min(bb[0], bbox[0]), min(bb[1], bbox[1]), min(bb[2], bbox[2]), max(bb[3], bbox[3]),
                                        max(bb[4], bbox[4]), max(bb[5], bbox[5])]

                            #Create the binary mask
                            mask = np.zeros([bbox[3]-bbox[0],bbox[4]-bbox[1],bbox[5]-bbox[2]],dtype=data.dtype)
                            cell_updated=[]
                            for o in objects_to_fused:
                                bb = dataset.get_regionprop("bbox", o)
                                cell_updated.append(o.id)
                                data_box = data[bb[0]:bb[3], bb[1]:bb[4], bb[2]:bb[5]]
                                mask[bb[0]-bbox[0]:bb[3]-bbox[0], bb[1]-bbox[1]:bb[4]-bbox[1], bb[2]-bbox[2]:bb[5]-bbox[2]][data_box==o.id]=1

                            #Labelize the data
                            new_data, nb_cells = label(mask, return_num=True,background=0)
                            new_data=np.uint16(new_data)

                            #Reatribute the labels
                            match_label(nb_cells,new_data,data[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]])
                            printv(f"fuse {len(objects_to_fused) } in {nb_cells} objects  at {t} channel {channel}", 0)
                            dataset.set_seg(t, data, channel=channel, cells_updated=cell_updated)
                            cancel=False
        else: #ENTIRE IMAGES
            channel = int(self.get_inputfield("channel"))
            times = read_time_points(self.get_inputfield("time points"), t)
            if len(times) == 0:
                printv("No time points", 0)
            else:
                for t in times:
                    data = dataset.get_seg(t,channel)  # Get segmentations at the time
                    if data is None:
                        printv(f"ERROR: could not get segmentation at {t},{channel} ", 1)
                    else:
                        new_data,nb_cells=label(data>dataset.background,return_num=True,background=0)
                        printv(f"found {nb_cells} objects  at {t} channel {channel}", 0)
                        data = match_label(nb_cells, new_data, data)
                        dataset.set_seg(t, data, channel=channel, cells_updated=None) #Update all cells
                        cancel=False
        self.restart(cancel=cancel)
