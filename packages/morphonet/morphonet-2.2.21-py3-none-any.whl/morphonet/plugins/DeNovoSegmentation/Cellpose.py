# -*- coding: latin-1 -*-
from os.path import isfile
from skimage.transform import resize
from morphonet.plugins import MorphoPlugin
import numpy as np
from ...tools import printv
from ..functions import get_torch_device, read_time_points


def denoise(denoise_model,rawdata,diameter,t):
    # Denoise rawdata with CellPose3 but not working yet.
    if denoise_model is not None:
        printv("denoise z planes  at " + str(t), 0)
        for z in range(rawdata.shape[2]):
            printv("denoise z planes  " + str(z) + "  at " + str(t), 1)
            rawdata[..., z] = denoise_model.eval(rawdata[..., z], channels=[0, 0], diameter=diameter)[..., 0]
    return rawdata

def predict_3D(model,rawdata,dataset,t,diameter,downsampling,Isotrope,denoise_model=None):
    printv("predict the 3D segmentation masks with diameter " + str(diameter), 0)
    voxel_size = dataset.get_voxel_size(t)
    anisotropy = voxel_size[2] / voxel_size[1] #1/0.2=5 -> 100,100,20 ->  100,100,20*5
    printv("found anisotropy of " + str(anisotropy), 1)

    if downsampling > 1: rawdata = rawdata[::downsampling, ::downsampling, ::downsampling]
    if denoise_model is not None: rawdata= denoise(denoise_model,rawdata,diameter,t)
    if Isotrope and anisotropy!=1:
        original_shape=rawdata.shape
        rawdata = resize(rawdata, [rawdata.shape[0], rawdata.shape[1],int(anisotropy*rawdata.shape[2])], preserve_range=True).astype(rawdata.dtype)
        model_anisotropy=1
    else:
        model_anisotropy=anisotropy
    rawdata=np.swapaxes(np.swapaxes(rawdata, 0, 2), 1, 2) #Cell pose is Z,X,Y
    masks = model.eval(rawdata, diameter=int(diameter / downsampling), anisotropy=model_anisotropy, do_3D=True)
    masks = np.swapaxes(np.swapaxes(masks[0], 0, 2), 0, 1)  # Cell pose is Z,X,Y
    if Isotrope and anisotropy != 1: #Put Mask back
        masks = resize(masks, [original_shape[0], original_shape[1], original_shape[2]], preserve_range=True,order=0).astype(masks.dtype)
    return masks


class Cellpose(MorphoPlugin):
    """ This plugin uses an intensity image of the membranes from a local dataset at a specific time point, to compute
    a segmentation of the membranes, using the 3D CellPose deep learning algorithm.  Users can apply CellPose on a
    3D selected Mask to apply it to a part of a segmentation.\n

    This plugin can be used:

    * on a whole image by not selecting any object.

    * on a sub-part of the image by selecting objects. The algorithm will then be applied only on the mask of these \
    segmented objects

    \n
    This plugin can use the base models provided by cellpose (default_model parameter), or a custom-made model
    (pretrained_model parameter), that can be created for instance by using the Cellpose-Train plugin.

    Parameters
    ----------
    intensity_channel: int, default: 0
        in case of multiples channel, this corresponds to the intensity images channel

    dimension : string
        to applied CellPose in 2D or 3D

    time_points: string
        on which time point to train (current, begin:end, time1;time2;...)

    downsampling : int, default: 2
        The resolution reduction applied to each axis of the input image before performing segmentation, 1 meaning that
        no reduction is applied. Increasing the reduction factor may reduce segmentation quality

    default_model : string
        The model used to compute segmentations. A detailed documentation on models can be found https://cellpose.readthedocs.io/en/latest/models.html

    pretrained_model: string
        the full filename path to for pretrained model

    diameter: int, default: 30
        the average cell size diameter (in voxels)

    isotrope: bool, default: True
        resize (or not) the image to be isotropic before making prediction


    Reference
    ---------
        Stringer, C., Wang, T., Michaelos, M. et al. Cellpose: a generalist algorithm for cellular segmentation.
        Nat Methods 18, 100?106 (2021). https://doi.org/10.1038/s41592-020-01018-x
        https://www.cellpose.org
    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("Cellpose.png")
        self.set_image_name("Cellpose.png")
        self.set_name("CellPose : Perform cell segmentation on intensity images")
        self.add_inputfield("Intensity Channel", default=0)
        self.add_inputfield("Downsampling", default=1)
        self.add_inputfield("Diameter", default=30)
        self.add_dropdown("Default model",['cyto', 'cyto2', 'cyto3', 'nuclei','tissuenet','livecell',
                                           'general', 'CP', 'CPx', 'TN1', 'TN2', 'TN3', 'LC1', 'LC2', 'LC3', 'LC4'])
        self.add_filepicker("Pretrained model",default=None,Optional=True)
        self.add_toggle("Isotrope", default=True)
        self.add_inputfield("time points", default="current")
        #self.add_dropdown("denoise model type",['no-denoising', 'denoise-cyto3', 'deblur-cyto3', 'upsample-cyto3', 'denoise-nuclei','deblur-nuclei', 'upsample-nuclei'])
        self.set_parent("De Novo Segmentation")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None
        #import scipy.special._cdflib
        from cellpose import models
        from skimage.transform import resize
        import logging
        logging.basicConfig(level=logging.INFO) #To have cellpose log feedback on the terminalk

        which, device = get_torch_device()
        printv("CellPose  will run on " + which, 1)

        downsampling = int(self.get_inputfield("Downsampling"))
        intensity_channel= int(self.get_inputfield("Intensity Channel"))
        diameter = int(self.get_inputfield("Diameter"))
        model_type = self.get_dropdown("Default model")
        Isotrope = self.get_toggle("Isotrope")

        denoise_model = None
        '''For Cellpose 3 which not working yet ...
        denoise_model_type = self.get_dropdown("denoise model type")
        if denoise_model_type != "no-denoising":
            from cellpose.denoise import DenoiseModel
            denoise_model = DenoiseModel(model_type=denoise_model_type.replace("-", "_"), gpu=True)
        '''
        pretrained_model=self.get_filepicker("Pretrained model")
        if pretrained_model!="" and isfile(pretrained_model):
            printv("load the pretrained model " + pretrained_model, 0)
            model = models.CellposeModel(gpu=which == "GPU", device=device, pretrained_model=pretrained_model)
        else:
            printv("load the model " + model_type, 0)
            model = models.CellposeModel(gpu=which == "GPU", device=device, model_type=model_type)

        cancel = True
        #If objects are selected, we run cellpose on the global bounding box of the object
        if len(objects)>=1 and objects[0]!="":
            for t in dataset.get_times(objects):  # Get all times in the labeled objects list
                rawdata = dataset.get_raw(t, intensity_channel)
                data = dataset.get_seg(t, intensity_channel)
                if rawdata is not None and data is not None:

                    bbox = None  # Get the bounding box around the selected cells
                    for o in dataset.get_objects_at(objects, t):
                        printv("add object " + str(o.id) + " at " + str(o.t),1)
                        bb = dataset.get_regionprop("bbox", o)
                        if bbox is None:
                            bbox = bb
                        else:
                            bbox = [min(bb[0], bbox[0]), min(bb[1], bbox[1]),
                                  min(bb[2], bbox[2]), max(bb[3], bbox[3]),
                                  max(bb[4], bbox[4]), max(bb[5], bbox[5])]

                    rawdata_box = rawdata[bbox[0]:bbox[3]+1, bbox[1]:bbox[4]+1, bbox[2]:bbox[5]+1]
                    data_box = predict_3D(model,rawdata_box,dataset,t,diameter,1,Isotrope,denoise_model=denoise_model) #We do not apply downsampling for selected objectss

                    cells=np.unique(data_box)
                    nb_cells = len(cells)-1
                    if nb_cells == 1:  # Only background...
                        printv("did not find any cells ", 0)
                    else:
                        cells_updated = []

                        printv(f"found {nb_cells} cells  at {t}", 0)

                        #Now We have to merge this new segmentation inside the selected masks
                        data_mask=np.zeros(rawdata_box.shape,dtype=np.uint16)
                        for o in dataset.get_objects_at(objects, t):
                            cells_updated.append(o.id)
                            coords = dataset.np_where(o)
                            data_mask[coords[0] -bbox[0], coords[1] -bbox[1],coords[2] -bbox[2]] = True
                        data_box[data_mask==False] = 0 #Cut everything out of this masks

                        #Now we have to give the new cells ids
                        last_id = dataset.get_last_id(t)
                        data_box[data_box>0]+=last_id
                        data[bbox[0]:bbox[3]+1, bbox[1]:bbox[4]+1, bbox[2]:bbox[5]+1][data_mask==True]=data_box[data_mask==True]
                        for c in cells:
                            if c>0:
                                cells_updated.append(c+last_id)
                        print(" --> cells_updated="+str(cells_updated))
                        dataset.set_seg(t, data, channel=intensity_channel, cells_updated=cells_updated)  # ALL
                        cancel = False

        else: #Predict on the full images
            times = read_time_points(self.get_inputfield("time points"), t)
            if len(times) == 0:
                printv("No time points", 0)
            else:
                for t in  times:
                    rawdata = dataset.get_raw(t,intensity_channel)
                    if rawdata is None:
                        print(" --> miss raw data at "+str(t))
                    else:
                        init_shape = rawdata.shape
                        data = predict_3D(model,rawdata,dataset,t,diameter,downsampling,Isotrope,denoise_model=denoise_model)
                        if dataset.background != 0:
                            data[data==0] = dataset.background
                        cells = np.unique(data)
                        nb_cells = len(cells)-1
                        if nb_cells == 1:  # Only background...
                            printv("did not find any cells", 0)
                        else:
                            printv(f"found {nb_cells} cells  at {t}", 0)
                            if downsampling > 1: data = resize(data, init_shape, preserve_range=True, order=0)
                            dataset.set_seg(t, data, channel=intensity_channel, cells_updated=None)  # ALL
                            cancel = False



        logging.basicConfig(level=logging.WARNING)
        self.restart(cancel=cancel)
