# 2022-03-19
# M5Stack BASIC
# UIFlow MicroPython sd mount script
# by Paulus Schulinck (PaulskPt@Github.com)
#
# Docs: https://docs.micropython.org/en/v1.9.4/pyboard/library/uos.html

import machine, uos
from flash.myVars import MYVARS
#myV = MYVARS()  # create instance of myVars class
#my_debug = myV.get_my_debug()
#myV = None
my_debug = None

def mountit(sd, myV):
    global my_debug
    TAG = "mountit(): "
    do_mount = False
    sd_crd_info = None
    my_debug = myV.get_my_debug()
    if my_debug:
        print(TAG+"value debug = ", my_debug)
    
    try:
        if isinstance(sd, type(None)):  # Only try to mount if sd-card was not already mounted
            if my_debug:
                print(TAG+"sd is not defined, we go to create sd and mount it")
            do_mount = True
        else:
            if my_debug:
                print(TAG+"sd-card was already mounted")
            
    except NameError as exc:
        print(TAG+"NameError occurred")
        print(exc.args[0])
        sd = None
        do_mount = True
        sd_crd_info = None
        
    if do_mount:
        try:    
            sd = machine.SDCard(slot=3, miso=19, mosi=23, sck=18, cs=4)
            sd_crd_info = sd.info()
            if not isinstance(sd_crd_info, type(None)):
                myV.set_sd(sd)  # save the sd value
                if my_debug:
                    print(TAG+"SD-card info: ")
                    print("\tsize...........:", sd_crd_info[0])
                    print("\tbytes per track:", sd_crd_info[1])
                uos.mount(sd, '/sd')
                mp = uos.getcwd()
                if my_debug:
                    print(TAG+"SD card mounted at: \'{}\'".format(mp))
            else:
                print(TAG+"Creating sd object failed")
        except OSError as exc:
            print(TAG+"Mounting SD-Card failed")
            if exc.args[0] == 1:
                print(TAG+"mount point already mounted")  # EPERM error
            else:
                print(TAG+"Error {} occurred".format(exc))
                raise RuntimeError
    if my_debug:
        print(TAG+"returning value sd", type(sd))
    return sd
