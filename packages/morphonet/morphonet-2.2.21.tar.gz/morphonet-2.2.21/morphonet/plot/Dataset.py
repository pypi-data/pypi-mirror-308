import pickle
from os import listdir
from os.path import join, dirname, basename, isfile, isdir, exists

import numpy as np
import psutil

from morphonet.plot.Object import Object
from morphonet.plot.Property import Property
from morphonet.plot.ScikitProperty import ScikitProperty
from pathlib import Path
from math import floor

from morphonet.plugins.functions import shift_bbox
from morphonet.tools import mkdir, printv, _add_line_in_file, _read_last_line_in_file, \
    _load_seg, imsave, rmrf, cp, _save_seg_thread, imread, \
    get_property_type, _set_dictionary_value, get_id_t, get_name, write_XML_properties, _get_type, \
    start_init_raw, get_image_at, set_image_at, compute_scikit_region, rm, axis_ratio, diameter, convexity, \
    get_tc_from_filename, write_csv_properties, export_regionproperties_csv, roughness, intensity_heterogeneity, \
    intensity_distance, compactness, smoothness, connected_neighbors


class Dataset():
    """Dataset class automatically created when you specify your dataset path in the seDataset function from Plot()

    Parameters
    ----------
    begin : int
        minimal time point
    end : int
        maximal time point
    raw : string
        path to raw data file where time digits are in standard format (ex: (:03d) for 3 digits  )(accept .gz)
    segment : string
        path to segmented data file  where time digits are in standard format  (accept .gz)
    log : bool
        keep the log
    background : int
        the pixel value of the background inside the segmented image
    xml_file : string
        path to the xml properties files (.xml)
    temp_path : string
        temporary path to store all termporary data (but also curration)

    """

    def __init__(self, parent, begin=0, end=0, raw=None, segment=None, raw_dict=None, seg_dict=None, log=True,
                 background=0, xml_file=None,  temp_path=".temp",  segname=None):
        assert begin <= end, 'Time boundaries are not coherent ... '
        assert segment is not None or raw is not None or raw_dict is not None or seg_dict is not None, 'Please specify either segmented or raw images'

        self.parent = parent #Plot Instance
        self.begin = begin
        self.end = end
        self.log = log
        self.temp_path = temp_path
        self.annotations_path = join(self.temp_path, "annotations")
        mkdir(self.annotations_path)
        self.cells = {} # List of Cells

        # Prepare Step Folder
        self.step = self.get_last_step()
        self.visualization_step = self.step
        self.step_folder = join(self.temp_path, str(self.step))
        if self.step == 0:
            mkdir(self.step_folder)  # Create the directory
        else:
            printv("Last step is " + str(self.step), 1)

        # RAW DATA
        self.raw = False  # Is there any loading raw ?
        self.raw_path = None #Original Patch Given by the user (used for plugins)
        self.temp_raw_path= None #Temporary path where data are converted in 8bits
        self.nb_raw_channels={} #Number of channels associated to the rawdata
        self.current_segmented_channel = 0
        self.raw_datas = {}  # list of each rawdata time point
        self.raw_files = None
        # single path mode:
        if raw is not None and raw !="":
            self.raw = True
            self.raw_path = dirname(raw) + "/"
            if dirname(raw) == "":
                self.raw_path = ""
            self.raw_files = basename(raw)
            self.temp_raw_path=join(self.temp_path,"raw")
            mkdir(self.temp_raw_path)
        # dictionary mode
        self.raw_dict = raw_dict  # dictionary containing all raw info
        if self.raw_dict is not None and len(self.raw_dict) > 0:
            self.raw = True
            # init properties as empty.
            self.raw_path = ""
            self.raw_files = ""

            self.temp_raw_path = join(self.temp_path, "raw")
            mkdir(self.temp_raw_path)

        # Segmentation
        self.seg_datas = {}  # list of each segmented time point and associated channels
        self.voxel_size_by_t = {}
        self.segment_path = ""
        self.segmented_channels = []  #List of segmented channels
        self.segment = segment
        self.segment_files = "curated_t{:03d}.inr.gz"
        self.center = None  # Center of the images (we consider that center is fix throuth time and it's the same for raw and seg..)
        if segment is not None:
            self.segment_path = dirname(segment) + "/"
            if dirname(segment) == "":
                self.segment_path = ""
            self.segment_files = basename(segment)
            mkdir(self.segment_path)  # To be able to perform a first segmentation
        self.seeds = None  # To Send Centers to Unity
        self.seg_dict = seg_dict #dictionary mode
        if self.seg_dict is not None and len(self.seg_dict) > 0:
            self.segment_path = ""
            self.segment_files = ""


        # Define temporary name for segmented file in compress numpy format
        if self.segment is not None and self.segment != "":
            f = basename(self.segment)
        elif self.raw_files is not None and self.raw_files != "":
            f = basename(self.raw_files)
        else:
            f = segname+".tiff"
        self.temp_segname = f[:f.index('.')] + "_ch{:01d}.npz" #To save each step of the curation
        if self.temp_segname.count("{")==1: self.temp_segname = f[:f.index('.')] + "_t{:01d}_ch{:01d}.npz" #We do not have the time in the name (Only one time point)
        #temp segname : if some seg .npz files exist, we just take the existing prefix
        npz_prefix = self.get_npz_prefix()
        if npz_prefix is not None:
            self.temp_segname = npz_prefix


        # LOG
        self.log_file = "morpho_log.txt"
        self.background = background  # Background Color

        # DATA Management
        self.lasT = []  # List of last time step
        self.times_updated = []  # List of modified time point

        # SCIKIT PROPERTIES (From regions scikit image)
        self.regionprops = {}  # List of Regions Properties (from scikit image)
        self.regionprops_name = ['volume', "bbox"]#, "centroid"]  # Minimum required properties
        # Additional region asked by the user
        self.additional_regionprops_name = ['volume_real', 'volume_bbox', 'volume_filled',
                                            'axis_major_length',  'axis_minor_length','axis_ratio', "diameter",
                                            'equivalent_diameter_area',
                                            'euler_number', 'extent', "connected_neighbors",
                                            'convexity', 'roughness', "compactness", "smoothness",
                                            'intensity_max', 'intensity_mean', 'intensity_min',
                                            'intensity_heterogeneity', "intensity_distance"]

        self.init_regionprops()

        # PROPERTIES
        self.xml_properties_type = {}  # Save All Avaiable Properties (fom XML )
        self.properties = {}  # Stored all Properties
        self.xml_file = xml_file  # Xml Properties
        self.read_properties_files()

        # Cell to update
        self.cells_updated = {} #[t][c] = None -> All Cells;  [t][c]=[] -> Nothing; [t][c]=[1] -> Cell 1 at t for channel c
        self.last_object_id={} # Last Object Id per time points



    def get_last_id(self,t):
        #Return the last ID (in all channels) at this time point
        if t not in self.last_object_id:
            self.compute_last_id(t)
        return self.last_object_id[t]

    def compute_last_id(self,t):
        last_id=0
        for channel in self.segmented_channels:
            data=self.get_seg(t,channel=channel)
            if data is not None:
                last_id=max(last_id,data.max())
        self.last_object_id[t]=last_id

    def set_last_id(self,t,last_id):
        if t not in self.last_object_id:
            self.last_object_id[t]=last_id
        elif self.last_object_id[t]<last_id:
            self.last_object_id[t] = last_id

    def init_channels(self):
        #First we look in the temporary files
        files=None
        t=self.begin
        while t<=self.end+1 and files is None:
            printv(" init channels with previous temporary data at "+str(t),3)
            globstr = self.temp_segname.format(t, 0)
            files = self.get_last_version_glob_channels(globstr.replace("_ch0", "_ch*"))
            if files is not None:
                for f in files:
                    try:
                        # get channel number
                        s_path = str(f.resolve())
                        channel = int(s_path.split("_ch")[len(s_path.split("_ch")) - 1].replace(".npz", ""))
                        if channel not in self.segmented_channels:
                            self.segmented_channels.append(channel)
                    except Exception as e:
                        printv("WARNING: init_channels could not parse channel for {}, cause : {}".format(f.resolve(),
                                                                                                          e), 1)
            t+=1

        if files is None: #First Time we create the channel , we have to read the segmented data
            printv(" init channels for the first time ",3)
            if self.segment_files is not None and isfile(join(self.segment_path, self.segment_files.format(self.begin))):
                 self._read_seg(self.begin)
            elif self.seg_dict is not None and len(self.seg_dict) > 0:
                #don't just take begin, take the first available!
                begin = int(list(self.seg_dict.keys())[0])
                self._read_seg(begin)
            else:
                if self.segment_files is not None : printv("this file does not exist "+join(self.segment_path, self.segment_files.format(self.begin)),1)
        self.parent.check_exit()

    def restart(self, plug, label=None):  # Apply and Restart a Curation
        """Restart the curation mode after execution of a specific plugin

        Parameters
        ----------
        plug : MorphoPlug
            the plugin just executed

        Examples
        --------
        dataset.restart(fuse)
        """
        self.parent.restart(self.times_updated, label=label)
        self.times_updated = []
        if plug is not None:
            printv("End Of " + str(plug.name), 1)

    ##### ##### ##### #####  SAVE ALL STEPS OF CURATION

    def get_last_version(self, filename, step_only=False,before=None):
        '''
        Return the last file is exist in order of last steps first
        '''
        bc = self.step
        if before is not None:
            bc = before-1

        while bc >= 0:
            f = join(self.temp_path, str(bc), filename)
            if isfile(f):
                if step_only:
                    return bc
                return f
            bc -= 1
        if step_only:
            return 0

        return None

    def get_last_version_glob_channels(self, filename):
        '''
        Return the last file is exist in order of last steps first
        '''
        out = []
        bc = self.step
        while bc >= 0:
            p = Path(join(self.temp_path, str(bc)))
            res = list(p.glob(filename))
            if len(res)>0:
                out.extend(res)
            bc -= 1
        if len(out)>0:
            out.sort()
            return out
        return None

    def get_last_step(self):
        '''
        Return the last step version
        '''
        bc = 0
        while isdir(join(self.temp_path, str(bc))):
            bc += 1
        if bc == 0:
            return 0
        return bc - 1

    def get_first_step_with_seg(self,time):
        for index_step in range(0,self.step+1): #for all existing step
            if len(self.segmented_channels)>0:
                image_path = join(self.temp_path, str(index_step), self.temp_segname.format(
                    int(time), int(self.segmented_channels[0])))
                if isfile(image_path):
                    return index_step
        return -1

    def start_step(self, command, exec_time):
        '''
        Prepare the step folder and save the command to the log file system
        '''
        printv("Increase Step at " + str(self.step + 1), 1)
        self.step += 1  # Increase Step
        self.visualization_step = self.step
        self.step_folder = join(self.temp_path, str(self.step))
        mkdir(self.step_folder)  # Create the directory

        # SAVE ACTION
        if not isfile(join(self.step_folder, "action")):
            _add_line_in_file(join(self.step_folder, "action"), str(command))

            # Add the command to the log file
            _add_line_in_file(self.log_file,
                              str(self.step) + ":" + str(command) + str(exec_time.strftime("%Y-%m-%d-%H-%M-%S")) + "\n")

        # Initialisation times points
        self.times_updated = []

    def copy_previous_vtk(self,t,channel,cells_updated):
        '''
        Recopy the  vtk files from the previous step in order to avoid recomputing
        cells_updated=None #All Cells to update
        cells_updated=[] #No Cells to update
        cells_updated=[1,2] #Sepcifc cells to update
        '''
        bc = self.step
        while bc >= 0:
            f = join(self.temp_path, str(bc), str(t)+","+str(channel))
            if isdir(f):
                vtk_step_path=join(self.step_folder, str(t)+","+str(channel))
                mkdir(vtk_step_path)
                for vtk_filename in listdir(f):
                    if vtk_filename.endswith(".vtk"):
                        if cells_updated is not None:
                                cell_id=int(vtk_filename.replace(".vtk","").split("-")[1])
                                if cell_id not in cells_updated:
                                    cp(join(f,vtk_filename), vtk_step_path)
                return True
            bc -= 1
        return False


    def end_step(self):
        '''
        Save the lineage after performing an action
        '''
        printv("Finalise Step " + str(self.step),1)
        #EXPORT SOME PROPERTIES
        properties_to_save=["temporal"]
        #TODO: REMOVE THIS WITH NEW SYSTEM ???
        for property_name in properties_to_save:
            if property_name in self.properties:
                self.properties[property_name].export(filename=join(self.step_folder, property_name + ".txt"))

    def cancel_to_visualization_step(self):
        printv("Cancel to Visualization Step " + str(self.step),1)
        backup_current_step = self.visualization_step #check if worked
        while self.step > 0 and self.step >= backup_current_step: #Cancel steps one by one
            self.cancel(skip_restart=True) # Only restart at the end
        if backup_current_step != self.step: # If we did cancel at least 1 step
            self.parent.restart(self.times_updated) # restart now !

    def cancel(self,skip_restart=False):
        '''
        Cancel the last action (by put the STEP back)
        '''
        if self.step <= 0:
            printv("Nothing to cancel", 0)
            return None
        printv("Cancel Step " + str(self.step), 1)
        del_step_folder = self.step_folder  # We have to delete the current step folder
        self.step -= 1  # Decreate Step
        self.visualization_step = self.step
        self.step_folder = join(self.temp_path, str(self.step))

        # READ COMMAND
        label = ""
        if isfile(join(del_step_folder, "action")):
            action = _read_last_line_in_file(join(del_step_folder, "action"))
            printv("Cancel " + action.replace(":", " ").replace(";", " "), 0)

            # Retrieve the list of cells
            for a in action.split(";"):
                if a.strip().startswith("ID:"):
                    objts = a[a.find('[') + 1:a.find(']')].split("',")
                    for o in a[a.find('[') + 1:a.find(']')].split("',"):
                        label += o.replace("'", "") + ";"

        # RESTORE LINEAGE
        self.clear_lineage()
        for property_name in ["temporal"]:
            if property_name in self.properties:
                filename = join(self.step_folder, property_name + ".txt")
                if isfile(filename):
                    self.properties[property_name].read(filename)
                else:  # We have to remove completly the lienage
                    self.properties[property_name].todelete = True

        # RESTORE Images and regions properties
        self.times_updated = []
        for f in listdir(del_step_folder):
            last_file=None
            if f.endswith(".npz") or f.endswith("regions.pickle"):
                last_file = self.get_last_version(f, before=self.step+1)
                if last_file is None:   printv("ERROR , we should have something somewhere for " + str(last_file), 2)
            if last_file is not None:
                if f.endswith(".npz"):
                    t, channel = get_tc_from_filename(f,".npz")
                    data, vsize = _load_seg(last_file)  # Read Image
                    self._set_seg(t, channel,data)
                    self.times_updated.append(t)  # Meshes are automatically reload from compute_meshes

                if f.endswith("regions.pickle"):
                    t, channel = get_tc_from_filename(f,".regions.pickle")
                    self.delete_regionprops_at(t, channel)  # Clear previous regions properties
                    self.read_regionprops_at(t, channel, filename=last_file)
                    #update cells once property has been loaded
                    self.update_cells_at(t, channel)

        # TODO IF A REGIONS PROP IS ASKED AFTER THE CANCEL BUT WERE NEVER COMPUTED BEFORE, it leaves the old value...

        # REMOVE STEP FOLDER
        rmrf(del_step_folder)
        if not skip_restart:
            self.parent.restart(self.times_updated, label=label)


    def get_npz_prefix(self):
        for i in range(self.get_last_step()+1):#for all steps
            path = Path(join(self.temp_path),str(i))
            if path.exists():
                globstr = path.glob("*.npz") # check if we find npz files already
                for result in sorted(globstr, key=lambda item: len(str(item))):
                    tokens = str(result.stem).split("_t")
                    if len(tokens) > 1:
                        prefix = "_t".join(tokens[:-1])
                        suffix = tokens[-1] # then add the proper amount of digits to time
                        digits = "".join([c for c in suffix[:suffix.index("_ch")] if c.isdigit()])
                        length = len(digits)
                        return prefix + "_t{:0"+str(length)+"d}"+suffix[length:suffix.index("_ch")]+"_ch{:01d}.npz"
                    elif str(result.stem).count("t") == 1: #specific case where npz string has one t. cut here #TODO In the name contain the letter t , what happen ??
                        tokens = str(result.stem).split("t")
                        if len(tokens) > 1:
                            prefix = "t".join(tokens[:-1])
                            suffix = tokens[-1]  # then add the proper amount of digits to time
                            digits = "".join([c for c in suffix[:suffix.index("_ch")] if c.isdigit()])
                            length = len(digits)
                            return prefix + "t{:0" + str(length) + "d}" + suffix[length:suffix.index("_ch")] + "_ch{:01d}.npz"
                    elif  str(result.stem).count("_ch") == 1: #specific case where npz string has no t
                        tokens = str(result.stem).split("_ch")[0]   #Nothing was wound, we just look for the first time point
                        first_time_point="{:01d}".format(self.begin)
                        if tokens.endswith(first_time_point):
                            prefix=tokens[0:tokens.find(first_time_point)]
                            return prefix + "{:01d}_ch{:01d}.npz"
                    else:
                        printv("ERROR File do not recognize",-1)
                        quit()

        return None

    def get_actions(self):
        '''
        Return all actions in order

        '''
        actions = []
        for s in range(1, self.step + 1):
            action_file = join(self.temp_path, str(s), "action")
            if not isfile(action_file):
                printv("ERROR miss action file " + action_file, 0)
                actions.append("MISS ACTION FILE")
            else:
                action = _read_last_line_in_file(action_file)
                # cleanup actions string : remove "plugin:" intro
                action = action[7:]
                #remove input types
                action = (action.replace("IF:", "").replace("DD:", "").replace("MI:", "").replace("CB:", "")
                          .replace("DF:", ""))
                tokens = action[:-1].split("; ")
                tokens[0] = tokens[0].split(" : ")[0]#remove the long name of the plugin
                tokens[2] = tokens[2].replace("[","").replace("]","").replace("\',","/")
                objects = tokens[2].split("/")
                if(len(objects)>2):#if more than 2 objects, put an ellipsis
                    tokens[2] = ",".join(objects[:2])+" ... "
                else:
                    tokens[2] = ",".join(objects[:2])

                action = "-".join(tokens)
                actions.append(action.replace(" ", "_").replace(",", ".").replace(";", ":"))

        return actions

    def export(self, export_path, image_file_type="nii.gz", export_temp=False, export_prop=None, export_skprop=None):
        '''
        Export all the dataset with the last version of each file
        '''
        self.init_channels()
        mkdir(export_path)
        import shutil
        last_step = self.get_last_step()
        # EXPORT IMAGES

        for t in range(self.begin, self.end + 1):  # List images to restore HERE EXPORT AS ONE IMAGE IF MULTI CHANNEL
            printv("Exporting time point " + str(t), 1)
            seg_step = last_step
            while seg_step > 0 and not isfile(join(self.temp_path, str(seg_step),
                                                   self.temp_segname.format(int(t), int(self.segmented_channels[0])))):
                seg_step -= 1
            if seg_step == -1:
                printv("Unable to find a segmentation image at time : " + str(t) + " , skipping this time point.", 1)
                continue
            dataTemplate, vsize = _load_seg(join(self.temp_path, str(seg_step), self.temp_segname.format(int(t), int(
                self.segmented_channels[0]))))
            data = np.zeros(dataTemplate.shape+(len(self.segmented_channels),),dtype=dataTemplate.dtype) #add channel dims
            #in every case take template as channel 0
            data[:, :, :, int(0)] = dataTemplate  # aggregates channels into image output
            self.set_voxel_size(t, vsize, 0)
            # take from seg data if available
            if self.seg_dict is not None and str(t) in self.seg_dict and str(0) in self.seg_dict[str(t)]:
                vsize = self.seg_dict[str(t)][str(0)]["VoxelSize"]
            # take try from raw data
            elif self.raw_dict is not None and str(t) in self.raw_dict and str(0) in self.raw_dict[str(t)]:
                vsize = self.raw_dict[str(t)][str(0)]["VoxelSize"]
            #then continue if needed
            if len(self.segmented_channels) > 1:
                for channel in self.segmented_channels[1:]:
                    printv(" adding channel : "+str(channel), 1)
                    s = last_step

                    while s > 0 and not isfile(join(self.temp_path, str(s), self.temp_segname.format(int(t),int(channel)))):
                        s -= 1
                    if not isfile(join(self.temp_path, str(s), self.temp_segname.format(int(t),int(channel)))):
                        printv("ERROR did not find any backup for "+self.temp_segname.format(int(t),int(channel)),1)
                    else:
                        datachannel, vsize = _load_seg(join(self.temp_path, str(s), self.temp_segname.format(int(t),int(channel))))
                        data[:,:,:,int(channel)] = datachannel # aggregates channels into image output
                        self.set_voxel_size(t, vsize, channel)

                    # take from seg data if available
                    if self.seg_dict is not None and str(t) in self.seg_dict and str(channel) in self.seg_dict[str(t)]:
                        vsize = self.seg_dict[str(t)][str(channel)]["VoxelSize"]
                    # take try from raw data
                    elif self.raw_dict is not None and str(t) in self.raw_dict and str(channel) in self.raw_dict[str(t)]:
                        vsize = self.raw_dict[str(t)][str(channel)]["VoxelSize"]
            filename = join(export_path,self.temp_segname.replace("_ch{:01d}","").format(int(t)).replace(".npz",image_file_type))
            printv("writing segmented image to "+filename,1)
            dim_order = "XYZ"
            if len(data.shape) > 3:
                dim_order += "C"
            if len(data.shape) > 4:
                dim_order += "T"
            imsave(filename,data,voxel_size=(vsize[0],vsize[1],vsize[2]),dimension_order=dim_order,dtype=data.dtype,shape=data.shape)


        # EXPORT PROPERTIES
        property_exported = []
        s = last_step
        if export_prop is not None:
            if export_prop == 2:  # XML
                self.export_xml(join(export_path,"properties.xml"))
            elif export_prop == 0:  # CSV
                self.export_properties_csv(join(export_path,"properties.csv"))
            else:
                while s >= 0:
                    for f in listdir(join(self.temp_path, str(s))):
                        if isfile(join(self.temp_path, str(s), f)) and f.endswith("txt"):
                            property_name = f.replace(".txt", "")
                            if property_name not in property_exported:
                                printv("export property to " + join(export_path, f), 1)
                                cp(join(self.temp_path, str(s), f), export_path)
                            property_exported.append(property_name)
                    s -= 1

        # export sk-properties. No XML for now
        if export_skprop is not None:
            #start off by reading currently loaded skproperties
            for t in range(self.begin, self.end + 1):
                for c in self.segmented_channels:
                    self.read_regionprops_at(t, c)
            if export_skprop == 0:  # CSV
                export_regionproperties_csv(self.regionprops,join(export_path,"region_properties.csv"))
            else:  # TXT
                for pname in self.regionprops:
                    if len(self.regionprops[pname].data) > 0:
                        filename = join(export_path,f"{pname}.txt")
                        txt = self.regionprops[pname].get_txt()

                        with open(filename,"w") as tp:
                            tp.write(txt)
        if export_temp:
            if isdir(self.temp_path):
                export_temp_path = join(export_path, "temp_data")
                printv("Exporting temporary data to : " + export_temp_path + ".zip", 1)
                shutil.make_archive(join(export_path, export_temp_path), 'zip', self.temp_path)

    ##### ##### ##### #####  OBJECT ACCESS

    def get_object(self, *args):
        """Get an MorphoObject from a list of arguments (times, id, ... )

        Parameters
        ----------
        *args : list of arugemnts
            the arguments which define the object, with at least 1 argument (object id with time =0 )

        Return
        ----------
        MorphoObject class

        Examples
        --------
        dataset.get_object(1,2)
        """
        t = 0
        id = None
        channel=0
        s = None  # label
        tab = args
        if len(args) == 1:
            tab = args[0].split(",")

        if len(tab) == 1:
            try:
                id = int(tab[0])
            except:
                id = int(float(tab[0]))
        if len(tab) == 2:
            try:
                t = int(tab[0])
            except:
                t = int(float(tab[0]))
            try:
                id = int(tab[1])
            except:
                id = int(float(tab[1]))
        if len(tab) >= 3: #TODO ? CHANGE IN UNTY OBJECT NEED TO CONTAINS CHANBEL t,id,ch,s
            try:
                t = int(tab[0])
            except:
                t = int(float(tab[0]))
            try:
                id = int(tab[1])
            except:
                id = int(float(tab[1]))
            try:
                channel = int(tab[2])
            except:
                channel = int(float(tab[2]))
        if len(tab) >= 4:
            try:
                s = int(tab[3])
            except:
                s = int(float(tab[3]))

        if id is None:
            printv(" Wrong parsing  " + str(args[0]), 1)
            return None

        if t not in self.cells:
            self.cells[t] = {}
        if channel not in self.cells[t]:
            self.cells[t][channel] = {}

        if id not in self.cells[t][channel]:  # CREATION
            self.cells[t][channel][id] = Object(t, id,channel)

        if s is not None:
            self.cells[t][channel][id].s = s

        return self.cells[t][channel][id]

    def get_times(self, objects):
        '''
        Return the order list of time points corresponding to the list of objects
        '''
        times = []
        for cid in objects:  # Listobjects
            o = self.get_object(cid)
            if o is not None and o.t not in times:
                times.append(o.t)
        times.sort()  # Order Times
        return times

    def get_channels(self, objects):
        '''
        Return the order list of channels corresponding to the list of objects
        '''
        channels = []
        for cid in objects:  # List all objects
            o = self.get_object(cid)
            if o is not None and o.channel not in channels:
                channels.append(o.channel)
        channels.sort()  # Order Channels
        return channels

    def get_objects(self, objects):
        '''
        Return the list of objects from string format
        '''
        all_objects = []
        for cid in objects:
            o = self.get_object(cid)
            if o is not None:
                all_objects.append(o)
        return all_objects

    def get_objects_at(self, objects, t):
        '''
        Return the list of objects at a specific time point
        '''
        time_objects = []
        for cid in objects:
            o = self.get_object(cid)
            if o is not None and o.t == t:
                time_objects.append(o)
        return time_objects

    ##### ##### ##### ##### DATA ACCESS

    def _set_last(self, t):
        if t in self.lasT:  self.lasT.remove(t)
        self.lasT.append(t)  # Put at the end
        if t not in self.seg_datas:
            data_size=self._get_data_size()
            # if we do not have the time to load another 4 time points, remove the first time in the stack
            # alternatively in any case, only save max 5 time points at a time
            printv(f"checking if we have to clear time points: {len(self.lasT)} times saved in memory. "
                   f"Space available is {psutil.virtual_memory().available}, data_size is {data_size}", 2)
            if psutil.virtual_memory().available < data_size * 4 or len(self.lasT) >= 5:
                remove_t = self.lasT.pop(0)
                if remove_t == t: #do not remove what we are just adding
                    self.lasT.append(t)  # Put at the end
                    return
                printv("Remove from memory time " + str(remove_t), 1)
                if remove_t in self.seg_datas:
                    del self.seg_datas[remove_t]
                if remove_t in self.raw_datas:
                    del self.raw_datas[remove_t]


    def _get_data_size(self):
        """
        Get the size in bytes of the first time step (seg and raw).

        Returns
        -------
        size in bytes of the first time step (seg and raw).
        """
        sif = 0
        for t in self.seg_datas:
            if self.seg_datas[t] is not None:
                for channel in self.seg_datas[t]:
                    if self.seg_datas[t][channel] is not None:
                        sif += self.seg_datas[t][channel].nbytes
                if sif >0:
                    break

        # also count raw datas
        for t in self.raw_datas:
            if self.raw_datas[t] is not None:
                sif += self.raw_datas[t].nbytes
                break
        return sif

    def update_cells_at(self,t,channel):
        '''

        We update the list of cells based on the last region version

        '''
        printv("update_cells for channel  "+str(channel)+ " at "+str(t),2)
        if "bbox" in self.regionprops:  #use bbox by default: it is always loaded
            if t in self.regionprops["bbox"].data :
                data=self.regionprops["bbox"].get_at(t,channel)
                if data is not None:
                    existing_cells = []
                    for c in data:
                        if c not in self.cells[t][channel]:  # if somehow we don't have an id in the cells list, add it
                            self.get_object(t,c.id,channel) #This directly create the object
                        existing_cells.append(c.id)

                    todelete = [cell for cell in self.cells[t][channel].keys() if cell not in existing_cells]
                    for d in todelete:
                        del self.cells[t][channel][d]
        else:
            printv(" INTERNAL ERROR : bbox should be in the region props... ",2)


    ##### ##### ##### #####  SCIKIT IMAGE PROPERTY (Volume, bouding box, etc ...)

    def _regionprops_filename(self, filename):
        return filename.replace(".npz", ".regions.pickle")

    def init_regionprops(self):
        '''
        Initialize region properties object
        '''
        for name in self.regionprops_name: #Initalize
            self.init_regionprop(name,required=True)  #This propery are required by the system
        for name in self.additional_regionprops_name:
            self.init_regionprop(name)

    def init_regionprop(self,name,required=False):
        '''
        Create an object of property
        '''
        printv(" Create region "+name,2)
        self.regionprops[name] = ScikitProperty(self, name)
        self.regionprops[name].required = required

    def get_regionprops_at(self,t,channel,recompute=False):
        '''
        Load or compute (if not exist) all region properties for at a given time point and a given channel
        '''
        if not recompute:
            if self.read_regionprops_at(t, channel):
                return True
        return self.compute_regionprops_at(t, channel,recompute=recompute)

    def ask_regionprop(self,property): #TODO now we only compute properties for channel 0 (Change firt in unity the cell-channel system)
        '''
        Unity ask for a specific region to plot
        '''
        printv("Ask "+property+" from region prop for all ",2)
        if property not in self.regionprops:
            printv("error this property does not exist ... " + property, -1)
            return None
        self.regionprops[property].asked = True
        for t in range(self.begin,self.end+1):
            for channel in self.segmented_channels:
                properties=self.regionprops[property].get_at(t,channel)
                if properties is None:
                    if not self.read_regionprops_at(t, channel,property=property):
                        self.compute_regionprops_at(t,channel,property=property)  #We Compute the property

    def get_regionprop_at(self,property,t,channel,ordered=False,recompute=False):
        '''
        Return a given property for all cells at a specific time point
        Returns a dictionnary of cell -  propertu value
        '''
        printv("Get "+property+" from region prop at "+str(t)+ " for channel "+str(channel),2)
        if property not in self.regionprops:
            printv("error this property does not exist : " + property, -1)
            return None

        #Property is already computed and well store
        if not recompute:
            properties=self.regionprops[property].get_at(t,channel)
            if properties is not None: #Look if file exist
                printv("Found " + property + " from region prop at " + str(t) + " for channel " + str(channel), 2)
                return properties

            if self.read_regionprops_at(t, channel,property=property):
                 return self.get_regionprop_at(property, t, channel, ordered=ordered,recompute=recompute)  # Relaunch the same function (but reading will be finished)


        self.compute_regionprops_at(t,channel)  #We Compute the property

        return self.get_regionprop_at(property, t, channel,ordered=ordered,recompute=recompute)  # Relaunch the same function (but computing will be finished)

    def get_regionprop(self, property, mo):
        # Return a given property for a specific cell at a specific time point
        if mo is None:
            return None

        prop = self.get_regionprop_at(property,mo.t,mo.channel)
        if prop is None:
            return None

        return prop.get(mo)

    def compute_regionprops_at(self,t,channel,property=None,recompute=False,filename=None):
        if recompute: #Compute All regions
            printv("Re compute region properties at " + str(t) + " for channel " + str(channel), 0)
            self.compute_voxel_regionprops_at(t, channel,filename=filename)
            self.compute_voxel_regionprops_at(t, channel, voxel=False,filename=filename)
        else: #Compute specific region
            if property is None: #All Default Properties (in voxel)
                printv("Compute region properties at " + str(t) + " for channel " + str(channel), 0)
                self.compute_voxel_regionprops_at(t,channel,filename=filename)
            else:
                printv("Compute region property for "+str(property)+" at " + str(t) + " for channel " + str(channel), 0)
                self.compute_voxel_regionprops_at(t,channel, voxel=self.regionprops[property].voxel,filename=filename)
        self.parent.check_exit()
        
    def compute_voxel_regionprops_at(self, t, channel,voxel=True,filename=None):

        region_tocompute=[]
        for name in self.regionprops:
            rp = self.regionprops[name]
            if rp.voxel == voxel and (rp.required or rp.asked):
                region_tocompute.append(rp)

        if len(region_tocompute)==0:
            printv("no region Voxel="+str(voxel)+" to compute at "+str(t)+" for channel "+str(channel),2)
            return False

        if t not in self.seg_datas or channel not in self.seg_datas[t]:  #We need to read the data first
            data = self.get_seg(t, channel=channel)
        if self.seg_datas[t][channel] is None:
            printv("WARNING: seg datas at t {} and channel {} is null. cannot compute regionprops for this time", 1)
            return False

        printv("Compute Voxel="+str(voxel)+" for  "+str(len(region_tocompute))+" region props at " + str(t) + " for channel " + str(channel), 2)
        data = self.seg_datas[t][channel]

        #RAW IMAGES
        need_raw=False
        for rp in region_tocompute:
            if "intensity" in rp.name or rp.name=="distance_to_center":
                need_raw=True
        raw_data=None
        if need_raw:
            raw_data = self.get_raw(t, channel)

        vs = None if voxel else self.get_voxel_size(t, channel)
        region = compute_scikit_region(data, raw_data, t, channel, background=self.background,voxel_size=vs)
        if region is not None:
            for reg in region:  # Each region from segmented data
                c = reg['label']
                mo = self.get_object(t, c, channel)
                self.set_last_id(t, c)

                for rp in region_tocompute: #TODO This can be parallelzise ...
                    value = None
                    if rp.scikit_name in reg:
                        try:
                            value = reg[rp.scikit_name]  # Get Computed value from Scikit
                        except:
                            printv("error calculating scikit propery '" + rp.scikit_name + "' for object " + str(
                                c) + " at " + str(t), 2)
                    if value is None:  # Get Other functions value
                        try:
                            if rp.scikit_name == "intensity_heterogeneity":
                                value = intensity_heterogeneity(reg, data, raw_data)
                            elif rp.scikit_name == "intensity_distance":
                                value = intensity_distance(reg, raw_data) # Additional Properties
                            elif rp.scikit_name == "roughness":
                                value = roughness(reg,data) # Additional Properties
                            elif rp.scikit_name == "connected_neighbors":
                                value = connected_neighbors(reg,data,self.background) # Additional Properties
                            else:
                                value = eval(rp.scikit_name + "(reg)")  # Additional Properties
                        except:
                            printv("error calculating '" + rp.scikit_name + "' for object " + str(
                                c) + " at " + str(t), 2)
                    if value is not None:
                        self.regionprops[rp.name].set(mo, value)  # FILL DATASET PROPERTY
                        rp.send()

            self.save_regionprops(t, channel,filename=filename)
            return True
        return False

    def save_regionprops(self, t, channel, filename=None):
        if filename is None:
            filename = self.get_last_version(self.temp_segname.format(int(t), int(channel)))
            #filename = join(self.step_folder, self.temp_segname.format(int(t), int(channel)))


        regionprops_filename = self._regionprops_filename(filename)

        regions_dump = {}
        for property in self.regionprops:
            properties = self.regionprops[property].get_at(t, channel)
            if properties is not None:
                for mo in properties:
                    if mo.id not in regions_dump: regions_dump[mo.id] = {}
                    regions_dump[mo.id][property]=properties[mo]

        with open(regionprops_filename, "wb") as outfile:  # Save region prop
            pickle.dump(regions_dump, outfile)
        printv("save regions properties at " + str(t) + " for channel " + str(channel) + " for " + str(len(regions_dump))+ " objects  in " + regionprops_filename,2)


    def read_regionprops_at(self,t,channel,property=None,filename=None):
        if filename is None:
            filename = self.get_last_version(self.temp_segname.format(int(t), int(channel)))
        if filename is None:
            return False

        f = self._regionprops_filename(filename)
        if isfile(f):
            printv("read properties file " + f, 1)
            region_readed=[]
            with open(f, "rb") as infile:
                prop = pickle.load(infile)
                for c in prop:
                    self.set_last_id(t,c)
                    for p in prop[c]:
                        if p in self.regionprops:   #We do not read prevoius property (area)
                            self.regionprops[p].set(self.get_object(t, c,channel), prop[c][p]) #FILL THE PROPERTY
                            if p not in region_readed:region_readed.append(p)
            printv("look for "+str(property)+" in regions readed "+str(region_readed),2)
            for p in region_readed:
                self.regionprops[p].send() #Resend all this regions
            if property is not None:
                if property in region_readed:
                    return True
                else:
                    return False
            elif len(region_readed)>0:
                return True
            return False #Error reading the regions...
        return False

    def delete_regionprops_at(self, t, channel, filename=None, delete_file=False):
        # Delete filename
        printv("Delete region props at "+str(t)+' for channel '+str(channel),2)
        if filename is None :
            filename = self.get_last_version(self.temp_segname.format(int(t), int(channel)))

        if delete_file:
            if filename is not None and isfile(filename):
                regionprops_filename = self._regionprops_filename(filename)
                if isfile(regionprops_filename):
                    rm(regionprops_filename)

        # Delete everything
        #TODO : remettre cells_updated plus tard pour optimisation

        for property in self.regionprops:
            self.regionprops[property].del_at(t, channel)
            self.regionprops[property].send()  # Ready to send

        return True

    ##### ##### ##### #####  FAST SELECTION COMMAND

    def np_where(self, mo):
        '''
        is equal to np.where(data==mo.id)
        '''
        data_object_T = self.get_seg(mo.t, mo.channel)
        if mo.t not in self.seg_datas: return ([], [], [])
        if mo.channel not in self.seg_datas[mo.t]: return ([], [], [])
        data=self.seg_datas[mo.t][mo.channel]
        bbox = self.get_regionprop("bbox",mo)
        if bbox is not None and data is not None:
            databox = data[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
            coords = np.where(databox == mo.id)
            return (coords[0] + bbox[0], coords[1] + bbox[1], coords[2] + bbox[2])
        return ([], [], [])

    def set_cell_value(self, mo, v):
        # is equal to data[np.where(data==c)]=v
        if mo.t not in self.seg_datas:
            self.get_seg(mo.t,mo.channel)#try at least once to compute seg.
            if mo.t not in self.seg_datas:
                printv("could not set cell {} to {}, wrong time".format(mo, v),1)
                return
        if mo.channel not in self.seg_datas[mo.t]:
            self.get_seg(mo.t, mo.channel)  # try at least once to compute seg.
            if mo.channel not in self.seg_datas[mo.t]:
                printv("could not set cell {} to {}, wrong channel".format(mo, v),1)
                return
        data = self.seg_datas[mo.t][mo.channel]
        bbox = self.get_regionprop("bbox",mo)
        if bbox is not None :
            databox = data[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
            databox[np.where(databox == mo.id)] = v
            data[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]] = databox
        else:
            printv("could not set cell {} to {}, bounding box issue".format(mo,v),1)
        return data

    def get_mask_cell(self, mo, border):
        '''
        Return a given property for a specific cell at a specific time point
        '''
        bbox = self.get_regionprop("bbox", mo)
        data = self.seg_datas[mo.t][mo.channel]
        bbox = shift_bbox(bbox, border=border, shape=data.shape)
        return data[bbox[0]:bbox[1], bbox[2]:bbox[3], bbox[4]:bbox[5]]


    ##### ##### ##### #####  SEGMENTATION AND MESH

    def _set_seg(self, t, channel, data=None):
        if t not in self.seg_datas:
            self.seg_datas[t] = {}
        self.seg_datas[t][channel] = data
        if channel not in self.segmented_channels:
            self.segmented_channels.append(channel)

    def set_seg(self, t, data, channel=0, cells_updated=None):
        """Define the segmented data at a specitic time point (Used in the plugins )
        Call this function when you modifiy something in the data

        Parameters
        ----------
        t : int
            the time point
        data : numpy matrix
            the segmented image
        channel: int
            channel of the seg to set
        cells_updated : (optional) list
            list of cell just udpated by the plugin (in order to compute faster)
            None #All Cells to update
            [] #No Cells to update
            =[1,2] #Sepcifc cells to update


        Examples
        --------
        dataset.set_seg(1,data)
        """
        printv("Re set segmentation data at " + str(t) + " with cells to update  " + str(cells_updated), 2)
        self._set_seg(t,channel,data)
        if t not in self.times_updated: self.times_updated.append(t)
        if t not in self.cells_updated:self.cells_updated[t]={}
        self.cells_updated[t][channel]=cells_updated
        if channel not in self.segmented_channels: self.segmented_channels.append(channel)
        self.copy_previous_vtk(t, channel, cells_updated)
        self._save_seg(t,channel,data) #Save the data
        self.delete_regionprops_at(t,channel) #Cancel previous regions prop
        self.get_regionprops_at(t,channel,recompute=True) #Recompute Region Props
        self.update_cells_at(t,channel) #Update new and old cells
        self.update_properties(t,channel)

    def set_voxel_size(self, t, vsize, c=0,force=False):
        if c is None: c=0
        if vsize is not None:
            if t in self.voxel_size_by_t and len(self.voxel_size_by_t[t])>0:#if we already have voxel sizes in channel
                for key, vs in self.voxel_size_by_t[t].items():
                    if key is not c:
                        if not np.equal(vsize, vs).all():
                            printv(str(vsize) + " // " + str(vs), 3)
                            printv("WARNING : detected different voxel size values for time " + str( t) + ". Will cause errors.", 0)

            if force:
                if t not in self.voxel_size_by_t:
                    self.voxel_size_by_t[t] = {}
                self.voxel_size_by_t[t][c] = vsize
            elif t not in self.voxel_size_by_t or self.voxel_size_by_t[t] is None:
                if t not in self.voxel_size_by_t:
                    self.voxel_size_by_t[t] = {}
                self.voxel_size_by_t[t][c] = vsize

    def get_voxel_size(self, t, c=0, txt=False):
        vsize = None
        if t in self.voxel_size_by_t and c in self.voxel_size_by_t[t]:
            vsize = self.voxel_size_by_t[t][c]
        if vsize is None:
            vsize = (1, 1, 1)
        if txt:
            return str(vsize[0]) + "_" + str(vsize[1]) + "_" + str(vsize[2])
        else:
            return vsize

    def get_current_voxel_size(self):
        return self.get_voxel_size(self.parent.current_time)

    def get_voxel_json(self):
        #Return the voxel size writing in the json dictionnary (set by the user)
        if self.seg_dict  is None : return None
        for t in self.seg_dict:
            for channel in self.seg_dict[t]:
                if "VoxelSize" in self.seg_dict[t][channel]:
                    return self.seg_dict[t][channel]["VoxelSize"]
        return None

    def _save_seg(self, t, channel,data=None,filename=None,rewrite=False):

        if data is None:
            if t in  self.seg_datas and channel in  self.seg_datas[t]:
                data = self.seg_datas[t][channel]
        else:
            self._set_seg(t,channel,data)
        if filename is None:
            filename=join(self.step_folder ,self.temp_segname.format(int(t),int(channel)))

        if not isfile(filename) or rewrite:

            sst = _save_seg_thread(filename, data, self.get_voxel_size(t))
            sst.start()


    def _read_seg(self,t):
        """
        Call the first time we have to read the segmented data
        """
        if self.seg_dict is not None and str(t) in self.seg_dict:  # dict & multichannel
            if str(t) not in self.seg_dict:
                return None
            filename = self.seg_dict[str(t)]["0"]["Path"]

            if len(self.seg_dict[str(t)]) > 1:  # if multiple images on the channel, check if only one file
                paths = ""
                onefile = True
                sizes = None  # also check dimensions. if they differ, we cannot stitch images, and it will fail
                for elem in self.seg_dict[str(t)]:
                    if sizes is None: sizes = self.seg_dict[str(t)][elem]["Size"]
                    if paths == "": paths = self.seg_dict[str(t)][elem]["Path"]
                    if paths != self.seg_dict[str(t)][elem]["Path"]: onefile = False
                    if sizes != self.seg_dict[str(t)][elem]["Size"]:
                        printv("ERROR : 3D images in time " + str(t) + " forming the channels have different " +
                               "dimensions. Unable to get seg.", 1)
                        return None

                s = (self.seg_dict[str(t)]["0"]["Size"][0],
                     self.seg_dict[str(t)]["0"]["Size"][1],
                     self.seg_dict[str(t)]["0"]["Size"][2], len(self.seg_dict[str(t)]))

                ch = 0
                if onefile:  # if one file, do not read every time
                    seg = imread(filename, reorder_image_dimension=True, new_order=self.seg_dict[str(t)]["0"]["Encoding"])
                    for elem in self.seg_dict[str(t)]:
                        if len(seg.shape) > 3:
                            o_t = self.seg_dict[str(t)][elem]["OriginalTime"]
                            o_c = self.seg_dict[str(t)][elem]["OriginalChannel"]
                            subimg = get_image_at(seg, o_t, o_c)

                        else:
                            subimg = seg

                        self._set_seg(t,ch,subimg)

                        vsize = self.seg_dict[str(t)][elem]["VoxelSize"]
                        self.set_voxel_size(t, vsize, ch, force=True)
                        output_filename = join(self.temp_path, "0", self.temp_segname.format(int(t),  int(ch)))  # WE always save the orignal image in the 0 folder
                        self._save_seg(t, ch,filename=output_filename)  # Save it in npz the first time we load the data

                        ch += 1

                else:  #Multiple Files
                    # get shape of projected stitched image
                    for elem in self.seg_dict[str(t)]:
                        seg = imread(self.seg_dict[str(t)][elem]["Path"],reorder_image_dimension=True,    new_order=self.seg_dict[str(t)][elem]["Encoding"])
                        if len(seg.shape) > 3:
                            o_t = self.seg_dict[str(t)][elem]["OriginalTime"]
                            o_c = self.seg_dict[str(t)][elem]["OriginalChannel"]
                            subimg = get_image_at(seg, o_t, o_c)
                        else:
                            subimg=seg


                        self._set_seg(t,ch,subimg)

                        vsize = self.seg_dict[str(t)][elem]["VoxelSize"]
                        self.set_voxel_size(t, vsize, ch, force=True)
                        output_filename = join(self.temp_path, "0", self.temp_segname.format(int(t),
                                                                                             int(ch)))  # WE always save the orignal image in the 0 folder

                        self._save_seg(t, ch,filename=output_filename)  # Save it in npz the first time we load the data


                        ch += 1

            else:  # otherwise just read the file, get the proper time/channel if 4/5D
                seg = imread(self.seg_dict[str(t)]["0"]["Path"],reorder_image_dimension=True, new_order=self.seg_dict[str(t)]["0"]["Encoding"])
                if seg is not None:
                    if len(seg.shape) > 3:
                        o_t = self.seg_dict[str(t)]["0"]["OriginalTime"]
                        o_c = self.seg_dict[str(t)]["0"]["OriginalChannel"]
                        subimg = get_image_at(seg, o_t, o_c)
                    else:
                        subimg= seg
                    self._set_seg(t,0,subimg)
                    vsize = self.seg_dict[str(t)]["0"]["VoxelSize"]
                    self.set_voxel_size(t, vsize, 0, force=True)
                    output_filename = join(self.temp_path, "0", self.temp_segname.format(int(t),int(0)))  # WE always save the orignal image in the 0 folder
                    self._save_seg(t, 0,filename=output_filename)  # Save it in npz the first time we load the data


        else:
            #old system : just read a file and assign
            data, metadata = imread(join(self.segment_path, self.segment_files.format(t)), return_metadata=True)
            data = data[:,:,:,:,0]
            vsize = metadata["voxel_size"]
            if len(data.shape) > 3:  # (X,Y,Z,C,T)
                for c in range(data.shape[3]):
                    if c not in self.segmented_channels:
                        self.segmented_channels.append(c)
                for c in self.segmented_channels:
                    self._set_seg(t, c, data[..., c])
                    self.set_voxel_size(t, vsize, c)
                    self._save_seg(t, c)

            else:
                self.segmented_channels = [0]
                self.seg_datas[t][0] = data
                self._save_seg(t, 0)
                self.set_voxel_size(t, vsize, 0)

    def get_seg(self, t,channel=0,filename=None):

        """Get the segmented data at a specitic time point

        Parameters
        ----------
        t : int
            the time point
        channel : int
            the channel

        Return
        ----------
        numpy matrix
            the segmented image

        Examples
        --------
        dataset.get_seg(1,0)
        """
        self._set_last(t)  # Define the time step as used
        if t not in self.seg_datas or channel not in self.seg_datas[t]: #FIRST TIME WE LOAD THE DATA
            if filename is None :
                filename=self.get_last_version(self.temp_segname.format(int(t),int(channel)))

            data,vsize = _load_seg(filename) # Look in the step folder
            self._set_seg(t, channel,data) #Initialisation
            if t in self.seg_datas and channel in self.seg_datas[t] and self.seg_datas[t][channel] is None:  #First time ,  we read the original data
                if self.segment_files is not None and isfile(join(self.segment_path, self.segment_files.format(t))):
                    self._read_seg(t)
                elif self.seg_dict is not None and len(self.seg_dict) > 0 and str(t) in self.seg_dict\
                        and isfile(self.seg_dict[str(t)]["0"]["Path"]):
                    self._read_seg(t)
            #TO FIX EN ARROR OF BAD VOXEL SIZE WRITE WITH THE NPZ
            original_voxel_size=self.get_voxel_json()
            if original_voxel_size is not None :
                rewrite=False
                if vsize is None:
                    rewrite=True
                else:
                    for i in range(len(original_voxel_size)):
                        if original_voxel_size[i] != vsize[i]:
                            rewrite=True
                if rewrite and filename is not None:
                    printv(f"Voxel size are different :{str(original_voxel_size)} != {str(vsize)}",2)
                    printv(f"Rewrite the npz {filename}",2)
                    vsize = np.array(original_voxel_size) #We update the value
                    self.set_voxel_size(t, vsize, channel)
                    self._save_seg(t, channel, filename=filename,rewrite=True)  # Save it in npz the first time we load the data
            #END VOXEL SIZE FIXINING

            self.set_voxel_size(t,vsize, channel)
        return self.seg_datas[t][channel]

    def get_center(self, data=None, txt=False):  # Calculate the center of a dataset
        """Get the barycenter of a matrix passed in argument

        Parameters
        ----------
        data : numpy matrix
            the 3D image (could be segmented or rawdata)

        Return
        ----------
        list of coordinates
            the barycenter of the image

        Examples
        --------
        center=dataset.get_center(seg)
        """

        center_filename = join(self.temp_path, "center.npy")
        if self.center is None:
            if isfile(center_filename):
                self.center = np.load(center_filename)

        if self.center is None and data is not None:
            self.center = [np.round(data.shape[0] / 2), np.round(data.shape[1] / 2), np.round(data.shape[2] / 2)]

        if self.center is None:
            if len(self.seg_datas) == 0:
                for t in range(self.begin,self.end+1):
                    self.get_seg(t)

            for t in self.seg_datas:
                for channel in self.seg_datas[t]:
                    if self.center is None and self.seg_datas[t][channel] is not None:
                        printv("compute center from seg at "+str(t),2)
                        self.center = [np.round(self.seg_datas[t][channel].shape[0] / 2), np.round(self.seg_datas[t][channel].shape[1] / 2), np.round(self.seg_datas[t][channel].shape[2] / 2)]

        if self.center is None:
            printv("Error miss center ", -1)
            if txt:
                return "0_0_0"
            else:
                return [0, 0, 0]

        if self.center is not None and not isfile(center_filename):
            np.save(center_filename, self.center)

        if txt: return str(int(round(self.center[0]))) + "_" + str(int(round(self.center[1]))) + "_" + str(
            int(round(self.center[2])))
        return self.center

    def get_mesh(self,t,channel):
        """
        Return the full mesh at t
        """
        return self.parent.compute_mesh(t,channel)

    def get_mesh_object(self, mo):
        '''
        Return the specific mesh of the object
        '''
        return self.parent.get_mesh_object(mo)

    ##### ##### ##### #####  INTENSITY IMAGES (RAW)

    def init_raw(self):
        if self.raw and self.raw_dict is not None and len(self.raw_dict) > 0:
            for elem in self.raw_dict:
                self.nb_raw_channels[int(elem)] = len(self.raw_dict[elem])
            # Start Convert Image in Thread
            sir = start_init_raw(self)
            sir.start()

        elif self.raw:
            #Detect number of channel
            self.nb_raw_channels[self.begin] = 1
            #check first image that exists if the first(s) are missing
            time = self.begin
            for i in range(self.begin, self.end+1):
                if self.raw_exists(i):
                    time = i
                    break
            im_raw = self.get_raw(time, channel=None)
            if im_raw is None:  # No images found
                for i in range(self.begin, self.end + 1):
                    self.nb_raw_channels[i] = 0
            else:
                if len(im_raw.shape) > 3:  # Contains Multiple Channels  [X,Y,Z,C]
                    for i in range(self.begin, self.end + 1):
                        self.nb_raw_channels[i]=im_raw.shape[3]
                else:
                    for i in range(self.begin, self.end + 1):
                        self.nb_raw_channels[i]=1 # Just one channel

            # Start Convert Image in Thread
            sir = start_init_raw(self)
            sir.start()
        self.parent.check_exit()

    def get_raw(self, t, channel=0):
        """Get the rawdata data at a specitic time point

        Parameters
        ----------
        t : int
            the time point
        Return
        ----------
        numpy matrix
            the raw data

        Examples
        --------
        dataset.get_raw(1)
        """
        if self.raw_path is None and self.raw_dict is None:
            printv("miss raw path", 1)
            return None
        if self.raw_dict is None:
            filename = join(self.raw_path, self.raw_files.format(t))
        elif self.raw_dict is not None and len(self.raw_dict) > 0:
            chn=channel
            filename=""
            if channel is None:chn=0
            if str(t) in self.raw_dict and str(chn) in self.raw_dict[str(t)]:
                filename = self.raw_dict[str(t)][str(chn)]["Path"]
        else:
            filename = ""
        if not isfile(filename):
            if filename!="": printv(" Miss raw file " + filename, 1)
            return None
        if t not in self.raw_datas:
            if self.raw_dict is not None and str(t) in self.raw_dict:  # dict & multichannel
                if len(self.raw_dict[str(t)]) > 1: #if multiple images on the channel, check if only one file
                    paths = ""
                    onefile=True
                    sizes = None# also check dimensions. if they differ, we cannot stitch images, and it will fail
                    for elem in self.raw_dict[str(t)]:
                        if sizes is None: sizes = self.raw_dict[str(t)][elem]["Size"]
                        if paths=="": paths = self.raw_dict[str(t)][elem]["Path"]
                        if paths != self.raw_dict[str(t)][elem]["Path"]: onefile = False
                        if sizes != self.raw_dict[str(t)][elem]["Size"]:
                            printv("ERROR : 3D images in time "+str(t)+" forming the channels have different " +
                                                                  "dimensions. Unable to get raw." , 1)
                            return None

                    s = (self.raw_dict[str(t)]["0"]["Size"][0],
                         self.raw_dict[str(t)]["0"]["Size"][1],
                         self.raw_dict[str(t)]["0"]["Size"][2], len(self.raw_dict[str(t)]))

                    ch = 0

                    if onefile:#if one file, do not read every time
                        raw = imread(filename,reorder_image_dimension=True,new_order=self.raw_dict[str(t)]["0"]["Encoding"])
                        composite = np.zeros(s, raw.dtype)
                        for elem in self.raw_dict[str(t)]:
                            if len(raw.shape) > 3:
                                o_t = self.raw_dict[str(t)][elem]["OriginalTime"]
                                o_c = self.raw_dict[str(t)][elem]["OriginalChannel"]
                                subimg = get_image_at(raw, o_t, o_c)
                                composite = set_image_at(composite, subimg, ch)
                            else:
                                composite = set_image_at(composite, raw, ch)
                            if composite is None:
                                printv("ERROR: mismatch between expected image dimensions and actual image dimensions. "
                                       "Please make sure your image series are of the same XYZ dimensions, "
                                       "or add them one by one",-1)
                            vsize = self.raw_dict[str(t)][elem]["VoxelSize"]
                            self.set_voxel_size(t, vsize, ch, force=True)
                            ch += 1



                        self.raw_datas[t] = composite

                    else:#
                        # get shape of projected stitched image
                        composite = None
                        for elem in self.raw_dict[str(t)]:
                            raw = imread(self.raw_dict[str(t)][elem]["Path"],reorder_image_dimension=True,
                                                new_order=self.raw_dict[str(t)][elem]["Encoding"])

                            read_s = (raw.shape[0], raw.shape[1], raw.shape[2], len(self.raw_dict[str(t)]))
                            if read_s != s:  # catch potential rounding errors in npz raw files
                                printv("dimensions in dict are not accurate. changing {} into {}".format(s, read_s), 2)
                                s = read_s

                            if composite is None:
                                composite = np.zeros(s, raw.dtype)
                            if len(raw.shape) > 3:
                                o_t = self.raw_dict[str(t)][elem]["OriginalTime"]
                                o_c = self.raw_dict[str(t)][elem]["OriginalChannel"]
                                subimg = get_image_at(raw, o_t, o_c)
                                composite = set_image_at(composite, subimg, ch)
                            else:
                                composite = set_image_at(composite, raw, ch)
                            if composite is None:
                                printv("ERROR: mismatch between expected image dimensions and actual image "
                                       "dimensions. Please make sure your image series are of the same XYZ dimensions, "
                                       "or add them one by one",-1)
                            ch += 1
                            vsize = self.raw_dict[str(t)][elem]["VoxelSize"]
                            self.set_voxel_size(t, vsize, ch, force=True)

                        self.raw_datas[t] = composite
                else:# otherwise just read the file, get the proper time/channel if 4/5D
                    raw = imread(self.raw_dict[str(t)]["0"]["Path"],reorder_image_dimension=True,new_order=self.raw_dict[str(t)]["0"]["Encoding"])
                    if len(raw.shape) > 3:
                        o_t = self.raw_dict[str(t)]["0"]["OriginalTime"]
                        o_c = self.raw_dict[str(t)]["0"]["OriginalChannel"]
                        subimg = get_image_at(raw,o_t,o_c)
                        self.raw_datas[t] = subimg
                    else:
                        self.raw_datas[t] = raw

                    vsize = self.raw_dict[str(t)]["0"]["VoxelSize"]
                    self.set_voxel_size(t, vsize, channel, force=True)

            else:# "old version' : just read file and assign
                data, metadata = imread(filename, return_metadata=True)
                self.raw_datas[t] = data[:,:,:,:,0]
                vsize = metadata["voxel_size"]
                self.set_voxel_size(t, vsize, channel, force=True)

            self.get_center(self.raw_datas[t])
        self._set_last(t)  # Define the time step as used
        if channel is None:  # Return the full matrix without specific channel
            return self.raw_datas[t]

        if len(self.raw_datas[t].shape) > 3:  # Contains Multiple Channels  [X,Y,Z,C]
            if channel >= self.raw_datas[t].shape[3]:
                printv("This channel " + str(channel) + " do not exist ..", 0)
                channel = 0  # Send the first one
            return self.raw_datas[t][..., channel]
        return self.raw_datas[t]  # One channels

    def raw_exists(self, t):
        if self.raw_path is None and self.raw_dict is None:
            printv("miss raw path", 1)
            return False
        if self.raw_dict is None:
            filename = join(self.raw_path, self.raw_files.format(t))
        else:
            if str(t) in self.raw_dict:
                filename = self.raw_dict[str(t)]["0"]["Path"] #here we test for min channel
            else:
                return False
        if not isfile(filename):
            printv(" Miss raw file " + filename, 1)
            return False
        return True

    ##### ##### ##### #####  SEEDS

    def add_seed(self, seed):
        """Add a seed in the seed list

        Parameters
        ----------
        seed : numpy array
            the coordinate of a seed


        Examples
        --------
        dataset.add_seed(np.int32([23,34,45]),1)
        """

        if self.seeds is None:
            self.seeds = []
        center = self.get_center()
        printv("Create a seed at " + str(seed[0]) + "," + str(seed[1]) + "," + str(seed[2]), 0)
        self.seeds.append(np.int32([seed[0] - center[0], seed[1] - center[1], seed[2] - center[2]]))

    def get_seeds(self):
        """Return the list of seeds as string

        Examples
        --------
        seeds=mc.get_seeds()
        """

        if self.seeds is None or len(self.seeds) == 0:
            return None
        strseed = ""
        for s in self.seeds:
            vs = self.get_current_voxel_size()
            strseed += str(s[0] * vs[0]) + "," + str(s[1] * vs[1]) + "," + str(s[2] * vs[2]) + ";"
        self.seeds = None  # Reinitializeation
        return strseed[0:-1]

    ##### ##### ##### ##### PROPERTIES FUNCTIONS

    def update_properties(self,t,channel=0):
        """
        Update properties with deleted cells

        """
        toremove = []
        if len(self.cells_updated)>0:
            printv("updating properties for time {}, channel {}, please wait...".format(t,channel),1)
            if t in self.cells_updated:
                if channel in self.cells_updated[t]:
                    if self.cells_updated[t][channel] is None:  #Remove all cells
                        for c in self.cells[t][channel]:  # means cell does not exist anymore
                            toremove.append(str(t) + "," + str(c) + "," + str(channel))
                    else:
                        for c in self.cells_updated[t][channel]:
                            if c not in self.cells[t][channel]:
                                toremove.append(str(t)+","+str(c)+","+str(channel))
            if len(toremove)>0:
                self.update_txt_properties_cells(toremove)

    def read_last_properties(self):
        """
        Read the last version of eacch property from the various step folder (FOR CELL LINEAGE)

        """
        bc = self.step
        while isdir(join(self.temp_path, str(bc))):
            for filename in listdir(join(self.temp_path, str(bc))):
                if isfile(join(self.temp_path, str(bc), filename)) and filename.endswith(
                        ".txt"):  # All files finishing with txt are property
                    property_name = filename.replace(".txt", "")
                    if property_name not in self.properties:  # Not already read before
                        inf = self.get_property(property_name)
                        inf.read(join(self.temp_path, str(bc), filename))
            bc -= 1

    def read_properties(self):
        """
        Read the properties  from the property folder

        """
        # Read All Properties
        printv("reading properties from files...",1)
        properties = []
        path = Path(self.temp_path)
        # get all individual .txt properties files
        for i in range(int(self.get_last_step()) + 1):
            files = list(path.glob(join(str(i), "*.txt")))
            files = [f.name for f in files]
            properties = list(set(properties) | set(files))
        if len(properties) > 0:
            for prop in properties:
                last_version = None
                for i in range(self.get_last_step() + 1):
                    f = join(self.temp_path, str(i), prop)
                    if isfile(f):
                        last_version = f
                if last_version is not None:
                    property_name = prop.replace(".txt", "")
                    type = "string"
                    if property_name not in self.xml_properties_type:  # Not already read before
                        with open(last_version, "r") as pf:
                            head = ""
                            try:
                                for x in range(3):  # only check 5 first lines to get type ? could be prone to errors
                                    head += next(pf)
                            except Exception as e:
                                printv("warning: property {} may be too short".format(property_name),1)
                            type = _get_type(head)
                            self.xml_properties_type[property_name] = type

                    p = self.get_property(property_name, type, create=True)
                    if p is not None:
                        with open(last_version, "r") as pf:
                            d = pf.read()
                            p.add_data(d)
                            printv("loaded property {} from .txt file".format(property_name), 1)

    def get_property(self, property_name, property_type=None, reload=False, create=True):
        """
        Return the property for the dataset
        """
        if property_type is None:
            property_type = get_property_type(property_name)
            if property_type is None:
                property_type = "string"

        if reload and property_name in self.properties:  # Clear Property
            self.properties[property_name].clear()

        if property_name not in self.properties and create:  # Create a new one
            self.properties[property_name] = Property(self, property_name, property_type)

        if property_name not in self.properties:
            return None
        return self.properties[property_name]

    def update_txt_properties_cells(self,deleted_cells):
        if len(deleted_cells)>0:
            #TODO: ONLY DO THE FILE THING FOR PROPS NOT IN MEMORY, OTHERWISE BETTER FUNCS EXIST
            for prop in self.xml_properties_type.keys():
                if prop not in self.properties and self.xml_properties_type[prop] != "time":
                    last_ver = None
                    for i in range(int(self.get_last_step()) + 1):
                        pfile = join(self.temp_path,str(i),prop+".txt")
                        if isfile(pfile):
                            last_ver = pfile
                    if last_ver is not None:
                        with open(last_ver, "r") as f:
                            lines = f.readlines()
                        with open(join(self.temp_path,str(self.get_last_step()),prop+".txt"), "w") as f:
                            #TODO: OPTIMIZE THIS IF POSSIBLE
                            for line in lines:
                                w = True
                                for elem in deleted_cells:
                                    if line.startswith(elem+":"):
                                        w = False
                                if w:
                                    f.write(line)


    ##### ##### ##### ##### XML
    def read_properties_files(self):
        properties = []
        path = Path(self.temp_path)
        #get all individual .txt properties files
        for i in range(int(self.get_last_step())+1):
            files = list(path.glob(join(str(i), "*.txt")))
            files = [f.name for f in files]
            properties = list(set(properties) | set(files))
            # if none are found, parse the XML and save the properties. otherwise read the properties.
            # (WARNING: threads write ? means we have to join...)
        if len(properties)==0 and self.xml_file is not None:
            if self.xml_file.endswith(".xml"):
                self.read_xml(self.xml_file)
            elif self.xml_file.endswith(".txt"):
                self.read_first_txt(self.xml_file)
            else:
                printv("ERROR: unsupported properties file format (must be .txt or .xml)",0)
                return
            #and here all the properties must be loaded in memory
        elif len(properties)>0:#if properties are found, init them as empty, get the lineage(s) & send properties to be downloaded later
            for prop in properties:
                last_version = None
                for i in range(self.get_last_step()+1):
                    f = join(self.temp_path,str(i),prop)
                    if isfile(f):
                        last_version=f
                if last_version is not None:
                    property_name = prop.replace(".txt","")
                    if property_name not in self.xml_properties_type:  # Not already read before
                        type="string"
                        n = prop.replace(".txt", "")
                        with open(last_version,"r") as pf:
                            head=""
                            try:
                                for x in range(3):#only check 5 first lines to get type ? could be prone to errors
                                    head += next(pf)
                            except Exception as e:
                                printv("warning: property {} may be too short".format(n),1)
                            type = _get_type(head)
                            self.xml_properties_type[n] = type
                        if type == "time":
                            p = self.get_property(n, type, create=True)
                            if p is not None:
                                with open(last_version, "r") as pf:
                                    d = pf.read()
                                    p.add_data(d)
                                    printv("loaded lineage {} from .txt file".format(n), 1)




                        """# Look if there is a correspondant annotation
                        if isfile(join(self.annotations_path, prop)):
                            inf.read_annotation(join(self.annotations_path, prop))
                        else:
                            inf.read(last_version"""

    def read_txt(self, propname):
        filename = None
        for i in range(self.get_last_step() + 1):
            f = join(self.temp_path, str(i), propname+".txt")
            if isfile(f):
                filename = f

        if filename is None or not exists(filename) or not filename.endswith(".txt"):
            printv("property file missing: {}".format(filename),1)
            return None

        if propname in self.xml_properties_type:
            p = self.get_property(propname,self.xml_properties_type[propname],create=True)
            if p is not None:
                with open(filename,"r") as pf:
                    d = pf.read()
                    p.add_data(d)
                    printv("loaded property {} from .txt file".format(propname),1)
            else:
                printv("ERROR: read_text, could not create property {} with get_property".format(propname),1)
        else:
            printv("WARNING: trying to read property {} when it has not been initialized".format(propname),1)

    def read_first_txt(self,filename):
        """
        Read txt property file when initializing dataset (must be temporal)
        Parameters
        ----------
        filename : path to the property file

        Returns
        -------
        """
        if not isfile(filename):
            printv("ERROR: property text file {} does not exist".format(filename),1)
            return
        with open(filename,"r") as pf:
            head = ""
            try:
                for x in range(3):  # only check 5 first lines to get type ? could be prone to errors
                    head += next(pf)
            except Exception as e:
                printv("warning: lineage property file {} may be too short".format(filename),1)
            type = _get_type(head)
            if type != "time":
                printv("ERROR: property text file {} must be of type:time".format(filename), 1)
                return
            self.xml_properties_type["temporal"] = type
        with open(filename,"r") as pf:
            data = pf.read()
            p = self.get_property("temporal", "time", create=True)
            p.add_data(data)
            p.export(filename=join(self.step_folder, "temporal.txt"), wait=False)

    def read_xml(self, filename, property=None, all=True, export=True, wait=False):
        if filename is None or not exists(filename) or not filename.endswith("xml"):
            printv('properties file missing ' + str(filename), 2)
            return None

        if all: self.xml_properties_type = {}
        import xml.etree.ElementTree as ElementTree
        inputxmltree = ElementTree.parse(filename)
        root = inputxmltree.getroot()
        for child in root:
            property_name = child.tag
            if property_name not in self.regionprops_name:
                property_type = get_property_type(property_name)
                if property_type == 'time' : property_name = "temporal"
                if all: self.xml_properties_type[property_name] = property_type
                if (property is not None and child.tag == property) or all is True:
                    printv("Read " + child.tag, 0)
                    prop = _set_dictionary_value(child)
                    inf = self.get_property(property_name, property_type=property_type)
                    if type(prop) == list:  # List of Cells
                        for idl in prop:
                            t, c = get_id_t(idl)
                            mo = self.get_object(get_name(t, c))
                            inf.set(mo, 1)
                    else:  # DICT
                        for idl in prop:
                            t, c = get_id_t(idl)
                            mo = self.get_object(get_name(t, c))
                            if property_type == 'time':
                                daughters = []
                                for daughter in prop[idl]:
                                    td, d = get_id_t(daughter)
                                    do = self.get_object(get_name(td, d))
                                    do.add_mother(mo)
                                    daughters.append(do)
                                inf.set(mo, daughters)
                            else:
                                if type(prop[idl]) == list:
                                    for elt in prop[idl]:
                                        inf.set(mo, elt)
                                else:
                                    inf.set(mo, prop[idl])
                    if export:
                        inf.export(filename=join(self.step_folder, inf.name + ".txt"),wait=wait)

        if all: printv("Property found in the XML file  " + str(self.xml_properties_type.keys()), 1)

    def export_xml(self, filename):
        if filename is not None:
            properties = {}
            for property_name in self.properties:
                inf = self.properties[property_name]
                property_name_w = property_name
                if (inf.property_type == "selection" and property_name.find("selection_") == -1) or (
                        inf.property_type == "label" and property_name.find("label_") == -1):
                    property_name_w = "label_" + property_name
                properties[property_name_w] = inf.get_dict()
            write_XML_properties(properties, filename)

    def export_properties_csv(self,filename):
        if filename is not None:
            properties = {}
            for property_name in self.properties:
                inf = self.properties[property_name]
                property_name_w = property_name
                if (inf.property_type == "selection" and property_name.find("selection_") == -1) or (
                        inf.property_type == "label" and property_name.find("label_") == -1):
                    property_name_w = "label_" + property_name
                properties[property_name_w] = inf
            write_csv_properties(properties,filename)


    ################## TEMPORAL FUNCTIONS

    def clear_lineage(self):
        if "temporal" in self.properties:
            self.properties["temporal"].clear()
        for t in self.cells:
            for channel in self.cells[t]:
                for cid in self.cells[t][channel]:
                    self.cells[t][channel][cid].clear_temporal_links()

    def _get_at(self, objects, t):
        cells = []
        for cid in objects:
            o = self.get_object(cid)
            if o is not None and o.t == t:
                cells.append(o)
        return cells

    def add_link(self, c1, c2):
        """Create a temporal link in the lineage between two object

        Parameters
        ----------
        c1 : MorphoObject
            the  cell
        c2: MorphoObject
            the other cell


        Examples
        --------
        mc.add_link(c,m)
        """
        if c1 is None or c2 is None:   return False

        if c1.t < c2.t:   return self.add_daughter(c1, c2)
        return self.add_daughter(c2, c1)

    def add_mother(self, c, m):
        """Create a temporal PAST link in the lineage

        Parameters
        ----------
        c : MorphoObject
            the  cell
        m : MorphoObject
            the mother cell


        Examples
        --------
        mc.add_mother(c,m)
        """
        if c is None or m is None:
            return False
        return self.add_daughter(m, c)

    def del_link(self, c1, c2):
        """Delete any temporal link between c1 and c2

        Parameters
        ----------
        c1 : MorphoObject
            the  cell
        c2 : MorphoObject
            the pther cell


        Examples
        --------
        mc.del_link(c,d)
        """
        if c1 is None or c2 is None:
            return False
        if c1.t < c2.t: return self.del_daughter(c1, c2)
        return self.del_daughter(c2, c1)

    def del_mother(self, c, m):
        """Remove a temporal FUTUR link in the lineage

        Parameters
        ----------
        c : MorphoObject
            the  cell
        m : MorphoObject
            the mother cell


        Examples
        --------
        mc.del_mother(c,m)
        """
        if c is None or m is None:
            return False
        return self.del_daughter(m, c)

    def del_cell_from_properties(self, cell):
        """ Delete a cell from properties (

        Parameters
        ----------
        cell : MorphoObject
            the  cell

        """
        updated = False
        if cell is None:
            printv("Error during cell deletion from properties", 1)
            return False

        infos_name = self.properties
        for name in infos_name:
            inf = infos_name[name]
            value = inf.get(cell)
            inf.del_annotation(cell, value)
            inf.updated = True
            updated = True
        return updated

    def del_daughter(self, c, d):
        """Create a temporal PAST link in the lineage

        Parameters
        ----------
        c : MorphoObject
            the  cell
        d : MorphoObject
            the daughter cell


        Examples
        --------
        mc.del_daughter(c,d)
        """
        if c is None or d is None:
            return False
        if c.del_daughter(d):
            inf = self.get_property("temporal", property_type="time")
            inf.updated = True
            inf.del_annotation(c, d)
            return True
        return False

    def add_daughter(self, c, d):
        """Create a temporal FUTUR link in the lineage

        Parameters
        ----------
        c : MorphoObject
            the  cell
        d : MorphoObject
            the daughter cell

        Examples
        --------
        mc.add_daughter(c,d)
        """
        if c is None or d is None:
            return False
        if c.add_daughter(d):
            inf = self.get_property("temporal", property_type="time")
            inf.set(c,d) #Add this new cell s
            inf.updated = True
            return True
        return False

    # DEPRECATED FUNCS

    def read_infos(self):
        printv("deprecated please use read_properties() ", 2)
        return self.read_properties()

    def get_info(self, info_name, info_type=None, reload=False, create=True):
        printv("deprecated please use get_property() ", 2)
        return self.get_property(property_name=info_name, property_type=info_type, reload=reload, create=create)
