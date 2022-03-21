# 2022-03-20
# by Paulus Schulinck (PaulskPt@Github)
# Class for global variables

# keys to myVarsDict
k_sd  = 0  # SD-Card object
k_dbg = 1  # debug print flag
k_ftp = 2  # font chosen
k_fsz = 3  # font size
k_ico = 4  # icon chosen

class MYVARS:
    
    def __init__(self):

        self.myVarsDict = {
            k_sd: None,
            k_dbg: True,
            k_ftp: None,
            k_fsz: 0
            }
        
        self.fonts = {
            0: "Default",
            1: "DejaVu18",
            2: "DejaVu24",
            3: "Ubuntu",
            4: "Comic",
            5: "Minya",
            6: "Tooney",
            7: "Small",
            8: "DefaultSmall",
            9: "7seg",
            11: "DejaVu40",
            12: "DejaVu56",
            13: "DejaVu72",
            16: "UNICODE",
            }
        
        self.icons = {
            0: "SetMenu",
            1: "Machine",
            2: "ListON",
            3: "ListOFF",
            4: "App",
            5: "AppIcon",
            6: "AppMenu",
            7: "Eath",
            8: "Key",
            9: "Retry",
            10: "Setup",
            11: "Url",
            12: "Wifi",
            13: "WifiBig",
            14: "USB",
            15: "Cloud",
            }


    def get_sd(self):
        if self.myVarsDict[k_dbg]:
            print("MYVARS.get_sd: returning self.myVarsDict[k_sd]: ", self.myVarsDict[k_sd])
        return self.myVarsDict[k_sd]
    
    def set_sd(self, new_sd):
        if new_sd:
            # self.sd = new_sd
            self.myVarsDict[k_sd] = new_sd
    
    def get_my_debug(self):
        return self.myVarsDict[k_dbg]
    
    def set_my_debug(self, new_my_debug):
        if new_my_debug is not None:
            if self.myVarsDict[k_dbg]:
                print("MYVARS.set_my_debug(): setting myVarsDict[k_dbg] to: ", new_my_debug)
            self.myVarsDict[k_dbg] = new_my_debug
        else:
            print("MYVARS.set_my_debug(): value variable new_my_debug: ", new_my_debug)
            
    def get_font(self):
        return "FONT_" + self.fonts[self.myVarsDict[k_ftp]]
    
    def set_font(self, new_fnt):
        if new_fnt >= 0:
            if self.myVarsDict[k_dbg]:
                print("myVars.set_font(): param new_fnt = {}, this is font: {}".format(new_fnt, self.fonts[new_fnt]))
            self.myVarsDict[k_ftp] = new_fnt
        else:
            if self.myVarsDict[k_dbg]:
                print("myVars.set_font(): param new fnt = ", new_fnt)
            
    def get_fontsize(self):
        return self.myVarsDict[k_fsz]
    
    def set_fontsize(self, fsz):
        if fsz >= 0:
            self.myVarsDict[k_fsz] = fsz
            
    def get_icon(idx):
        if idx >= 0 and idx < len(self.icons.keys()):
            if idx in self.icons.keys():
                self.icons[idx]
            else:
                if self.myVarsDict[k_dbg]:
                    print("myVars.get_icon(): key {} not found in: {}".format(idx, self.icons.keys()))
