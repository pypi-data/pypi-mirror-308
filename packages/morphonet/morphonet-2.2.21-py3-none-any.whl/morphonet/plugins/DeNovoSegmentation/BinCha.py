# -*- coding: latin-1 -*-
import logging
from os.path import join, isfile

from morphonet.plugins import MorphoPlugin
import numpy as np
from ...tools import printv
from ..functions import fit_bbox_in_shape, _centerInShape


class BinCha(MorphoPlugin):
    """This plugin creates a new segmentation from each mask of the selected objects using a binary threshold on
    intensity image in the desired channel. Alternatively, you can also do the thresholding on the centroid of each
    object, with a bounding box of input radius.

    Parameters
    ----------
    intensity_Channel : int, default: 0
        The desired channel to apply the binary threshold
    threshold : int, default: 30
        The threshold value using in the intensity image
    radius : int, default: 15
        The radius value of the bounding box around the center of each selected objects (only applies is bbox_on_centroid is True)
    intensity_channel : int, default: 0
        The desired channel to apply the binary threshold
    bbox_on_centroid : bool, default: False
        Toggle on to compute on the centroid of selected objects, with a bounding box of radius
    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("BinCha.png")
        self.set_image_name("BinCha.png")
        self.set_name("BinCha : apply a binary threshold on the other channel from selected objects")
        self.add_inputfield("threshold", default=30)
        self.add_inputfield("Intensity Channel", default=0)
        self.add_toggle("bbox on centroid", default=False)
        self.add_inputfield("radius", default=15)
        self.set_parent("De Novo Segmentation")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects):
            return None

        from skimage.measure import label
        threshold = float(self.get_inputfield("threshold"))
        intensity_channel = int(self.get_inputfield("Intensity Channel"))
        radius = int(self.get_inputfield("radius"))
        bbox_mode = bool(self.get_toggle("bbox on centroid"))

        cancel = True

        for t in dataset.get_times(objects):  # For each time points in selected object
            cell_updated = []
            rawdata = dataset.get_raw(t, intensity_channel)
            if rawdata is None:
                printv("miss raw data at "+str(t), 0)
            else:
                data = dataset.get_seg(t, intensity_channel)
                if data is None:
                    printv(f"Create a complete new segmentation data at {t} for channel {intensity_channel}", 1)
                    data = np.zeros_like(rawdata).astype(np.uint16)#Create an empty matrix

                last_id = dataset.get_last_id(t) + 1
                for o in dataset.get_objects_at(objects, t): #For each objects

                    if bbox_mode:
                        coords = dataset.np_where(o)
                        centroid = [int(np.mean(coords[0])), int(np.mean(coords[1])), int(np.mean(coords[2]))]
                        printv("centroid of " + str(o.id) + " at " + str(o.t) + " in channel " + str(o.channel) +
                               " is "+str(centroid), 2)

                        bbox = [centroid[0]-radius, centroid[1]-radius, centroid[2]-radius,centroid[0]+radius, centroid[1]+radius, centroid[2]+radius] # Get the bounding box with this diameter
                        bbox = fit_bbox_in_shape(bbox,data.shape)#Trunk the box if it gets out of the image shape
                    else:
                        bbox = self.dataset.get_regionprop("bbox", o)

                    #CREATE A MASK WITH EXISTING OBJECTS IN THE CHANNEL
                    data_box = data[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
                    raw_box = rawdata[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
                    raw_box[data_box > 0] = 0 #Put at 0 where cells already exist

                    new_data_box = np.uint16(label(np.uint8(raw_box > threshold)))  # Label by connected component

                    if bbox_mode:  # bbox mode ("old" BinCha)
                        new_label = new_data_box[radius,radius,radius]
                        if new_label == 0:  # Only background...
                            printv(f"did not find any new object for label {o.id}", 0)
                            printv("the distribution of intensity in this bounding box is " + str(
                                np.unique(rawdata[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]])), 1)
                        else:
                            last_id += 1
                            printv(f"For object {o.id} at {t} in channel {o.channel}, create a new object "
                                   f"{last_id} in channel {intensity_channel}", 0)
                            data_box[new_data_box == new_label] = last_id
                            cell_updated.append(last_id)
                    else:  # BinCha on mask
                        source_seg = dataset.get_seg(t,o.channel)
                        source_box = source_seg[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
                        new_data_box[source_box != o.id] = 0  # remove all new seg not in original mask
                        labels = np.unique(new_data_box)
                        for lab in labels:
                            if lab != 0:
                                last_id += 1
                                printv(f"For object {o.id} at {t} in channel {o.channel}, create a new object "
                                       f"{last_id} in channel {intensity_channel}", 0)
                                data_box[new_data_box == lab] = last_id
                                cell_updated.append(last_id)





            if len(cell_updated)>0:
                dataset.set_seg(t, data, channel=intensity_channel, cells_updated=cell_updated)  # New ID
                cancel = False

        self.restart(cancel=cancel)




