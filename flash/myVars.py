# 2022-03-20
# by Paulus Schulinck (PaulskPt@Github)
# Class for global variables

# keys to myVarsDict
k_sd  = 0
k_dbg = 1
k_ftp = 2
k_fsz = 3
k_ico = 4

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
        if not isinstance(new_sd, type(None)):
            # self.sd = new_sd
            self.myVarsDict[k_sd] = new_sd
    
    def get_my_debug(self):
        return self.myVarsDict[k_dbg]
    
    def set_my_debug(self, new_my_debug):
        if not isinstance(new_my_debug, type(None)):
            if not self.myVarsDict[k_dbg]:
                print("MYVARS.set_my_debug(): setting myVarsDict[k_dbg] to: ", new_my_debug)
            self.myVarsDict[k_dbg] = new_my_debug
        else:
            print("MYVARS.set_my_debug(): value variable new_my_debug: ", new_my_debug)
            
    def get_font(self):
        return "FONT_" + self.fonts[self.myVarsDict[k_ftp]]
    
    def set_font(self, fnt):
        if not isinstance(fnt, type(None)):
            self.myVarsDict[k_ftp] = fnt
            
    def get_fontsize(self):
        return self.myVarsDict[k_fsz]
    
    def set_fontsize(self, fsz):
        if not isinstance(fsz, type(None)):
            self.myVarsDict[k_fsz] = fsz
            
    def get_icon(idx):
        if not isinstance(idx, type(None)):
            if idx >= 0 and idx < len(self.icons.keys()):
                if idx in self.icons.keys():
                    self.icons[idx]
                else:
                    if self.myVarsDict[k_dbg]:
                        print("myVars.get_icon(): key {} not found in: {}".format(idx, self.icons.keys()))