# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from ..functions import gaussian, get_barycenter
from ...tools import printv

def get_overlap_bbox(bboxs):
    bboxs = [list(bbox) for bbox in bboxs]
    init_bbox=bboxs[0]
    for bbox in bboxs:
        if bbox[0] < init_bbox[0]: init_bbox[0] = bbox[0]
        if bbox[1] < init_bbox[1]: init_bbox[1] = bbox[1]
        if bbox[2] < init_bbox[2]: init_bbox[2] = bbox[2]
        if bbox[3] > init_bbox[3]: init_bbox[3] = bbox[3]
        if bbox[4] > init_bbox[4]: init_bbox[4] = bbox[4]
        if bbox[5] > init_bbox[5]: init_bbox[5] = bbox[5]
    return init_bbox


class Prope(MorphoPlugin):
    """
    This plugin propagates labeled objects at the current time point through time, filling empty space.\n

    It requires a segmentation, an intensity image, and selected objects.

    The selected object(s) (named the source objects) will be propagated Forward in time or Backward in time by
    choosing the appropriate time_direction parameter. The source objects are then copied to the segmentation of the
    next/previous time (the intersection with the rest of the segmentation is removed), and finally a watershed
    algorithm is applied, using the corresponding intensity image. New objects are created in the background of the
    segmentation.


    Parameters
    ----------
    objects:
        The selected or labeled objects on MorphoNet
    time_direction : string
        Forward : The first time point to be propagated is the lowest one.
        Backward : THe first time point to be propagated is the latest, and the propagation happens in backwards direction
    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Prope.png")
        self.set_image_name("Prope.png")
        self.set_name("Prope : Propagate selected eroded objects through time on the next empty area with intensity images)")
        self.add_dropdown("time direction", ["Forward", "Backward"])
        self.add_inputfield("membrane channel", default=0)
        self.add_inputfield("sigma", default=2)
        self.set_parent("Propagate Segmentation")


    # For time t , and a list of object that will be used as seeds, do a watershed in objects to split
    def process_at(self, t, channel, next_t, objects, dataset,s_sigma,membrane_channel):
        import numpy as np
        from skimage.segmentation import watershed

        from skimage.transform import rescale, resize

        printv("Processing Shape Propagation of " + str(len(objects)) + " objects from time " + str(t) , 0)
        data_t = dataset.get_seg(t, channel) # Load current time point segmentation
        data_next_t = dataset.get_seg(next_t, channel)# Load next time point segmentation
        raw_next_t = dataset.get_raw(next_t, membrane_channel)
        if data_next_t is None:
            raise ValueError(f"Error, no segmented image found at time {t}")

        if raw_next_t is None:
            raise ValueError(f"Error, no intensity image found at time {t}")

        if s_sigma > 0.0:
            printv("Perform gaussian with sigma=" + str(s_sigma) + " at " + str(t), 0)
            raw_next_t = gaussian(raw_next_t, sigma=s_sigma, preserve_range=True)


        #Compute the overlap Bouding Box for the selected objects
        bb=None
        for o in objects:
            bbox_c = dataset.get_regionprop("bbox", o)
            if bb is None: bb = bbox_c
            else: bb = get_overlap_bbox([bb,bbox_c])
        printv("The largest bounding box is "+str(bb),3)

        #making bbox bigger : since we have no bounding box for "next time", we need to go a little larger
        bb = list(bb)
        border_size = 10
        for i in range(3):
            bb[i] = bb[i] - border_size
            if bb[i] < 0:
                bb[i] = 0
        for i in range(3, 6):
            bb[i] = bb[i] + border_size
            if bb[i] > data_next_t.shape[i-3]:
                bb[i] = data_next_t.shape[i-3]

        raw_box = raw_next_t[bb[0]:bb[3], bb[1]:bb[4], bb[2]:bb[5]]

        #Calculate Final Mask
        sm = data_next_t[bb[0]:bb[3], bb[1]:bb[4], bb[2]:bb[5]]
        mask_next_t = sm == dataset.background  # Create a mask with only the background at true

        #Get only the corresponding  mask in the bouding box
        printv("Create markers by overlaping at " + str(t), 1)
        markers = np.zeros_like(mask_next_t).astype(np.uint8)
        smt = data_t[bb[0]:bb[3], bb[1]:bb[4], bb[2]:bb[5]]
        i = 1
        correspondences = {}
        for o in objects:
            sm_id = smt == o.id  # Binarize
            sm_id[mask_next_t==False]=False #Remove the outsides voxel with no overlapping with the next mask
            if True in sm_id:
                markers[sm_id] = i
                correspondences[i] = o
                i += 1

        if i < 2:  # need at least one label to propagate
            raise ValueError("Error, Objects do not overlap with empty space. aborting plugin...")

        #add seeds to all corners of the image to avoid watershed spill
        markers[0, 0, 0] = i+1
        markers[0, 0, markers.shape[2]-1] = i + 2
        markers[0, markers.shape[1]-1, 0] = i + 3
        markers[markers.shape[0]-1, 0, 0] = i + 4
        markers[0, markers.shape[1]-1, markers.shape[2]-1] = i + 5
        markers[markers.shape[0]-1, 0, markers.shape[2]-1] = i + 6
        markers[markers.shape[0]-1, markers.shape[1]-1, 0] = i + 7
        markers[markers.shape[0]-1, markers.shape[1]-1, markers.shape[2]-1] = i + 8


        # Now we expand the data in z if necessary
        vsize = dataset.get_voxel_size(t)  # Get the voxelsize
        ratioz = vsize[2] / vsize[0]
        mask_w = np.uint8(mask_next_t)
        if ratioz>1:
            mask_w = resize(mask_w,[mask_w.shape[0],mask_w.shape[1],int(mask_w.shape[2] * ratioz)],preserve_range=True,order=0)
            markers = resize(markers, [markers.shape[0], markers.shape[1], int(markers.shape[2] * ratioz)], preserve_range=True, order=0)
            raw_box = resize(raw_box, [raw_box.shape[0], raw_box.shape[1], int(raw_box.shape[2] * ratioz)], preserve_range=True)

        printv(f"Compute watershed with {i-1} objects at {str(next_t)}", 1)

        labelw = watershed(raw_box, markers, mask=mask_w)

        if ratioz > 1:
            labelw = resize(labelw, mask_next_t.shape, preserve_range=True, order=0)

        labels, counts = np.unique(labelw, return_counts=True)
        labels = labels[labels != 0] #Remove background
        labels = labels[labels < i] #remove labels added to the corers
        printv("Found " + str(len(labels)) + " objects ", 1)

        cells_updated = []
        lastID = int(data_next_t.max()) + 1

        correspondences_real= {}

        for new_l in labels:
            new_coords = np.where(labelw == new_l)
            data_next_t[new_coords[0] + bb[0], new_coords[1] + bb[1], new_coords[2] + bb[2]] = lastID
            printv('Create a new object ' + str(lastID) + " with " + str(len(new_coords[0])) + " voxels",1)
            cells_updated.append(lastID)
            correspondences_real[lastID] = correspondences[new_l]
            lastID += 1

        # set the new segmentation
        printv(f"The cells {str(cells_updated)} were updated at {str(next_t)}" , 1)
        dataset.set_seg(next_t, data_next_t, channel, cells_updated=cells_updated)

        for o in objects:

            corr_id = list(correspondences_real.keys())[list(correspondences_real.values()).index(o)]
            m = dataset.get_object(next_t,corr_id, channel)
            dataset.add_link(o, m)

        next_cells=[dataset.get_object(next_t,id, channel) for id in cells_updated]
        return next_cells, data_next_t # Return the list of cells updated, and the new segmentation

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects):
            return None

        printv("Shape Propagation of " + str(len(objects)) + " objects", 0)
        selections = {} # List Objects by selections , to work on each selection one by one
        for cid in objects:
            o = dataset.get_object(cid)
            if o is not None:
                if o.s not in selections:
                    selections[o.s] = []
                selections[o.s].append(o)

        if len(selections) > 1:
            printv(" --> Found  " + str(len(selections)) + " selections ", 0)

        forward = (str(self.get_dropdown("time direction")) == "Forward")  # Get user direction chosen
        s_sigma = int(self.get_inputfield("sigma"))
        membrane_channel = int(self.get_inputfield("membrane channel"))

        new_labels = None

        # For each selection found
        for s in selections:
            # Find the min, max and list of times
            time_lists = sorted([o.t for o in selections[s]])
            channel_lists = sorted([o.channel for o in selections[s]])
            channel_lists = list(dict.fromkeys(channel_lists))
            if not forward:
                time_lists = reversed(time_lists)

            object_times = {}

            time_lists = list(dict.fromkeys(time_lists))
            for t in time_lists:
                object_times[t]=[o for o in selections[s] if o.t==t]


            for channel in channel_lists:
                for t in object_times: # For each time point of this Selection
                    next_t = t + 1 if forward else t - 1 # Detect the time point to modify using direction chosen
                    prev_t = t - 1 if forward else t + 1 # Detect the time point to modify using direction chosen
                    # Propagate the seeds and get the new cells created as source for the next propagation
                    new_objects = {}
                    new_objects[next_t], data = self.process_at(t, channel, next_t, object_times[t], dataset,
                                                                s_sigma, membrane_channel)
                    # Add the updated cells to the list of cells to update
                    for cell in new_objects[next_t]:
                        if new_labels is None:  new_labels = ""
                        new_labels += str(next_t) + "," + str(cell) + "," + str(s) + ";"
        # Send back data to MorphoNet
        self.restart(label=new_labels)
