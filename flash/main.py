# 2022-03-19
# M5Stack BASIC
# UIFlow MicroPython test script
# by Paulus Schulinck (PaulskPt@Github.com)
# Filename: main.py

try:
    import flash.mount_sd
except ImportError:
    import mount_sd
from m5stack import display, lcd
from m5ui import *
from uiflow import get_version
import uos
import time
from machine import I2C, Pin
try:
    from flash.urtc import _BaseRTC, DS3231
except ImportError:
    from urtc import _BaseRTC, DS3231

lStart = True
sd = None
my_debug = None
#time.sleep(5)

i2c = I2C(sda=Pin(21), scl=Pin(22))

rtc = DS3231(i2c)

lcd.image(lcd.CENTER,lcd.CENTER, "img/BASIC_img1_a.jpg") # img/m5.jpg")
time.sleep(5)

def M5Info_s(myV):
    global lStart, sd, my_debug, rtc
    TAG = "M5Info(): "
    myV.set_my_debug(False)
    my_debug = myV.get_my_debug()
    sd = myV.get_sd()
    
    #------------------------------------------
    my_font = lcd.FONT_DejaVu18
    lcd.font(my_font)
    myV.set_font(my_font) # save current font type
    if my_debug:
        print(TAG+"line 24: lcd.font type set to:", myV.get_font())
    #-----------------------------------------

    if rtc is None:
        print("Creating rtc object failed. RTC connected? If so, check wiring.")
        dt = None
    else:
        lcd.fill(lcd.BLACK)
        if my_debug:
            print("rtc object created")
        
        """ Uncomment next line and adjust the items if you want to set the rtc """
        #rtc.datetime((2022,3,21,0,14,11,0,0))  # set the rtc
        
        #time.sleep(.5)
        dt = rtc.datetime() # get the datetime from the rtc
        month_in_text = True
        month_text_long = False
        if month_in_text:
            dts1 = "{}, {:04d}-{:s}-{:02d}".format(rtc.weekday(), dt[0], rtc.cur_month(dt[1], month_text_long), dt[2])
        else:
            dts1 = "{}, {:04d}-{:02d}-{:02d}".format(rtc.weekday(), dt[0], dt[1], dt[2])
        dts2 = "Time: {:02d}:{:02d}:{:02d}".format(dt[4], dt[5], dt[6])
        print(dts1)
        print(dts2)
        lcd.print(dts1, 0, 40,lcd.WHITE)
        lcd.print(dts2, 0, 80,lcd.WHITE)
        doty = "Day of the year: {}".format(rtc.yearday(dt[0], dt[1], dt[2]))
        print(doty)

        lcd.print(doty, 0, 120, lcd.WHITE)
        #-------------------------------------------------------------
        my_font = lcd.FONT_Default
        lcd.font(my_font)
        myV.set_font(my_font) # save current font type
        if my_debug:
            print(TAG+"line 82: lcd.font type changed to:", myV.get_font())
        #-------------------------------------------------------------
        time.sleep(5)

    if sd is None and lStart:
        try:
            from flash.mount_sd import mountit
        except ImportError as exc:
            from mount_sd import mountit
        sd = mountit(sd, myV)
        if sd is not None:
            lStart = False
            if my_debug:
                print(TAG+"SD-card successfully mounted")
            lcd.fill(lcd.BLACK)
            try:
                #buffer = open("/sd/img/AvatarDuck.jpg").read()
                #buffer = open("/sd/img/Avatar1.jpg").read()
                buffer = open("/sd/img/Avatar1clr.jpg").read()
                #buffer = open("img/LvMyAvatar.jpg").read()
                lcd.image_buff(210,10, buffer)
            except Exception as exc:
                print(TAG+"Error loading image: ", exc.args[0])
    lcd.setCursor(0,40)
    lcd.setTextColor(lcd.GREEN)

    lcd.print('M5Stack BASIC')
    lcd.setCursor(0,80)
    lcd.setTextColor(lcd.NAVY)
    lcd.print("UIFlow version : ")
    lcd.println(get_version())
    lcd.println('')
    lcd.println("UIFlow O.S.")
    lcd.print("sysname: ")
    lcd.println(uos.uname().sysname)
    lcd.print("release..: ")
    lcd.println(uos.uname().release)
    lcd.print("version..: ")
    lcd.println(uos.uname().version)
    lcd.print("machine.: ")
    lcd.println(uos.uname().machine)
    time.sleep(10)
    lcd.fill(lcd.BLACK)
    s = "M5INFO_S: THE END"
    lcd.print(s,0,0,lcd.WHITE)
    print(s)
    if not isinstance(sd, type(None)):
        sd.deinit() 
    time.sleep(5)
    lcd.fill(lcd.BLACK)
    return

if __name__ == "__main__":
    try:
        from flash.myVars import MYVARS # contains class that keeps track of certain global variables
    except ImportError as exc:
        from myVars import MYVARS
    myV = MYVARS() 
    M5Info_s(myV)
