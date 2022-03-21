# M5Stack_DS3231_uRTC

 Micropython module for DS3231 RTC and M5Stack Core.
 
 This repo is created and tested on a M5Stack Core1 (BASIC) processor.

 Origin: Adafruit-uRTC (https://github.com/adafruit/Adafruit-uRTC)
 Adafruit's library has the status 'Deprecated' because Adafruit changed it's policy to support only CircuitPython.
 The RTC module: ```urtc.py``` differs is in various ways from the original urtc.py from Adafruit.
 Adafruit's urtc library is suitable for various RTC modules. My urtc library serves only the DS3231 RTC,
 in combination with a M5Stack Core1 (BASIC) controller. It can also be used with other M5Stack units like the Core2.

 In file ```myVars.py``` is the ```class MVARS```, used to save various values so they can be used 
 globally between various scripts. This class has placeholders for variables and functions to set and get the variables.

 The file ```main.py``` was originally created as an exercise while getting acquainted to the M5Stack Core1 processor.
 This script was in the first instance written to display info about the firmware flashed into this processor. When that worked,
 I connected an external DS3231 RTC to the ```I2C pins``` of the Core1. I needed a library for the external RTC. I found a suitable one in the
 Adafruit-uRTC. I removed the classes for other brands of RTC models. Below info about the alterations I did to urtc.py.


In urtc.py, because I could not find a library ```ucollections``` for micropython,
as an alternative, I use a ```Dictionary``` with the name ```DtDict```. This dictionary is used in functions ```datetime_tuple()``` and
```seconds2tuple```.

```
Added:
- list days_since_jan1
- indexes for dictionary keys: yy, mo, dd, wd, hh, mm, ss and ms.
- dictionaries: WeekdaysDict, MonthsDict, MonthsDictShort, DtNames, rtcRegsDict, NamesDt, DtDict and DtDfltDict
- In class DS3231:, functions: weekday(), isLeapYear(), daysInMonth(), yearday() and cur_month().
Modified:
- functions: datetime_tuple(), tuple2seconds() and seconds2tuple().
- In class: _BaseRTC, function: datetime()
Removed:
- import ucollection
```
In the file ```main.py``` is created an ```SD-Card object```. To accomplish this function ```mountit()``` in file ```mount_sd.py``` is called.
(M5Stack usually mounts the SD-Card at boot time from within the file ```boot.py```. To control better the mounting/unmounting I decided to write the functions outside of boot.py). When the SD-Card has been mounted successfully, an image file is loaded which then is displayed.
The image loaded I did copy to this repo in the subfolder ```/flash/sd```.
You can copy the image file ```Avatar_01clr.jpg``` to an ```img``` folder on the SD-Card. If you have an SD-Card in your M5Stack processor
and you have not yet a folder ```img```, you have to create it. Then copy the file ```Avatar_01clr.jpg``` to the folder ```/sd/img/```.

In ```main.py``` an rtc object is created using the following commands:
```
i2c = I2C(sda=Pin(21), scl=Pin(22))

rtc = DS3231(i2c)
```

The script ```main.py``` uses two different text fonts:
    ```lcd.FONT_DejaVu18```  and ```lcd.FONT_Default```.

The copying of files to your M5Stack processor can be done with the ```Thonny``` app.

