

class ScikitProperty():
    """ Quantitative Information extract from Regions Properties from scikit image
    Parameters
    ----------
    name : string
        the name of the info
    """

    def __init__(self, dataset, name):
        self.name = name
        self.dataset = dataset
        self.data = {}
        self.updated = False
        self.asked = False
        self.sent=False
        self.required=False

        if self.name == 'bbox' or self.name == 'centroid' or self.name == 'coords':
            self.type = "dict"
            self.voxel = True  # IN VOXELS
        else:
            self.type = "float"
            if self.name.find("intensity") >= 0 or self.name == "diameter":
                self.voxel = True  # IN VOXEL
            else:
                self.voxel = False  # IN REAL UNIT

        self.scikit_name = name
        if self.name.find("volume") >= 0:
            self.scikit_name = self.name.replace("volume","area")
        if self.name == "volume_real":
            self.scikit_name = "area"
            self.voxel = False
        if self.name == "volume":
            self.voxel = True

    def show(self):
        print(self.name+ " voxel="+str(self.voxel)+ " required="+str(self.required)+ " asked="+str(self.asked)+ " sent="+str(self.sent))

    def send(self):
        self.sent = False

    def delete(self,mo):
        if mo.t in self.data and mo in self.data[mo.t]:
            self.data[mo.t].pop(mo.t)

    def set(self,mo,value):
        if mo.t not in self.data: self.data[mo.t]={}
        if mo.channel not in self.data[mo.t]:  self.data[mo.t][mo.channel]={}
        #print("For property "+self.name+ " at "+str(mo.t)+ " for channel "+str(mo.channel)+ " add for cell "+str(mo.id)+ " value = "+str(value))
        self.data[mo.t][mo.channel][mo] = value
        self.updated=True

    def get(self,mo):
        if mo.t not in self.data: return None
        if mo.channel not in self.data[mo.t]: return None
        if mo not in  self.data[mo.t][mo.channel]: return None
        return self.data[mo.t][mo.channel][mo]

    def get_at(self,t,channel):
        if t not in self.data: return None
        if channel not in self.data[t]: return None
        return self.data[t][channel]

    def del_at(self, t, channel):
        if t not in self.data: return False
        if channel not in self.data[t]: return False
        self.data[t].pop(channel)
        return True

    def del_cell(self, mo):
        if mo.t not in self.data: return False
        if mo.channel not in self.data[mo.t]: return False
        if mo not in self.data[mo.t][mo.channel]: return False
        self.data[mo.t][mo.channel].pop(mo)
        return True

    def get_txt(self):
        Text =  "#MorphoPlot" + '\n'
        Text += "#"+self.name+" property computed from Scikit image\n"
        Text += "type:" + self.type + "\n"
        for t in self.data:
            for c in self.data[t]:
                for o in self.data[t][c]:
                    if o.id!=self.dataset.background:
                        Text += o.get_name() + ':' + str(self.data[t][c][o])
                        Text += '\n'
        return Text
