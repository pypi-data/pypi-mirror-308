# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv


class Disco(MorphoPlugin):
    """ This plugin can be used to split any object made up of several sub-objects that are not in contact with
    each other.

    This plugin is applied on whole segmented images.

    Parameters
    ----------
    time_points: string
        Current times : will only split  objects at the current time point.
        All times : will split objects for all the time points

    """
    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Disco.png")
        self.set_image_name("Disco.png")
        self.set_name("Disco : Split unconnected objects")
        self.add_dropdown("time points",["Current time","All times"])
        self.set_parent("Segmentation Correction")
    def split_unconnected_at(self, t, channel, dataset):
        import numpy as np
        from skimage.measure import label
        data = dataset.get_seg(t,channel)  #Get segmentations at the time
        if data is None:
            printv(f"ERROR: could not get segmentation at {t}, {channel}. Aborting this step",1)
            return
        lastID = dataset.get_last_id(t) + 1
        cells_updated = []
        bbox_region = dataset.get_regionprop_at("bbox", t, channel, ordered=True)
        for o in bbox_region:
            bb = bbox_region[o]
            if bb is None:
                printv(f"ERROR: bbox property null for {t}, {channel}, object {o.id}",1)
                continue
            data_cell = data[bb[0]:bb[3], bb[1]:bb[4], bb[2]:bb[5]]
            labels = label(data_cell == o.id)
            ids, counts = np.unique(labels, return_counts=True)  # Get the differents  connected components
            w = ids!=0 #Remove background (ATTENTION it's not dataset.background !)
            counts = counts[w]
            ids = ids[w]
            if len(ids) > 1:  # If we have 2 connected components
                printv(f"Found Object to split {o.get_name()} at {t}, channel {channel}", 0)

                idx = np.where(counts == counts.max())  #from all the connected components to split, the biggest will get the previous cell ids
                id_cell = ids[idx][0]  # Keep this cell
                printv(f"Let's keep id : {id_cell}",2)
                cells_updated.append(o.id)
                for other_cell in ids: #for each other connected components
                    if other_cell != id_cell:
                        printv(f"We need to update cell with id : {other_cell}",2)  #Each component get a new id in the segmentation
                        data_cell[labels == other_cell] = lastID
                        printv(f"Create a new ID {lastID}",0)
                        #cell to refresh
                        cells_updated.append(lastID)
                        lastID += 1
                data[bb[0]:bb[3], bb[1]:bb[4], bb[2]:bb[5]]=data_cell

        #If we changed a cell , write segmentation
        if len(cells_updated) > 0:
            dataset.set_seg(t, data, channel, cells_updated=cells_updated)

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects,objects_require=False):
            return None
        #Start the split for the sequence of times or the single times depending of user choice
        if str(self.get_dropdown("time points")) == "All times":
            for c in self.dataset.segmented_channels:
                for i in range(self.dataset.begin, self.dataset.end + 1):
                    printv(f"Perform Disco at {t}, channel {c}", 0)
                    self.split_unconnected_at(i,c,dataset)
        else:
            for c in self.dataset.segmented_channels:
                self.split_unconnected_at(t,c,dataset)
        self.restart()
