# The origin of this file is from: adafruit/Adafruit-uRTC,
# a 'deprecated library' for MicroPython, at:
# https://github.com/adafruit/Adafruit-uRTC/blob/master/urtc.py
# 'Deprecated' because Adafruit changed its policy for support only to CircuitPython.
# For full documentation see http://micropython-urtc.rtfd.io/.
# Downloaded by PaulskPt@Github.com on 2022-03-21 at 10h10 UTC
# This is a modified version. The classes other than DS3231 I removed from this script
# In this file, because I could not find a library 'ucollections' for micropython,
# instead I use a Dictionary with name 'DtDict'. This dictionary is used in functions 'datetime_tuple()' and
# 'seconds2tuple'.
# Added:
# - list 'days_since_jan1'
# - indexes for dictionary keys: yy, mo, dd, wd, hh, mm, ss and ms
# - dictionaries: WeekdaysDict, MonthsDict, MonthsDictShort, DtNames, rtcRegsDict, NamesDt, DtDict and DtDfltDict
# - functions in class DS3231: weekday(), isLeapYear(), daysInMonth(), yearday(), cur_month()
# Modified:
# - functions: datetime_tuple(), tuple2seconds() and seconds2tuple()
# - In class: _BaseRTC, function: datetime()
# Removed:
# - import ucollection
# See my repo: https:://github.com/PaulskPt/DS3231_lib_for_M5Stack_CORE1
import utime

# Added by @paulsk, copied from micropython timeutils.c
days_since_jan1 = ( 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365 )

yy = 0
mo = 1
dd = 2
wd = 3
hh = 4
mm = 5
ss = 6
ms = 7

# +--------------+
# | DICTIONARIES |
# +--------------+

WeekdaysDict = {0:"Monday",
            1:"Tuesday",
            2:"Wednesday",
            3:"Thursday",
            4:"Friday",
            5:"Saturday",
            6:"Sunday"}

MonthsDict = {0: "dummy",
          1: "January",
          2: "February",
          3: "March",
          4: "April",
          5: "May",
          6: "June",
          7: "July",
          8: "August",
          9: "September",
          10: "October",
          11: "November",
          12: "December"}

MonthsDictShort = {0: "dummy",
          1: "Jan",
          2: "Feb",
          3: "Mar",
          4: "Apr",
          5: "May",
          6: "Jun",
          7: "Jul",
          8: "Aug",
          9: "Sep",
          10: "Oct",
          11: "Nov",
          12: "Dec"}

DtNames = {yy: "year",
           mo: "month",
           dd: "day",
           wd: "weekday",
           hh: "hour",
           mm: "minute",
           ss: "second",
           ms: "millisecond"}

rtcRegsDict = {6: "year",
           5: "month",
           4: "day",
           3: "weekday",
           2: "hour",
           1: "minute",
           0: "second",
           7: "millisecond"}

NamesDt = {"year":yy,
           "month":mo,
           "day":dd,
           "weekday":wd,
           "hour":hh,
           "minute":mm,
           "second":ss,
           "millisecond":ms}

DtDict = {
        yy: 2000,
        mo: 1,
        dd: 1,
        wd: 0,
        hh: 0,
        mm: 0,
        ss: 0,
        ms: 0}

# This is the DateTime default dictionary, containing default parameters
DtDfltDict = {yy:2000,
              mo:1,
              dd:1,
              wd:0,
              hh:0,
              mm:0,
              ss:0,
              ms:0}

# +-----------+
# | UTILITIES |
# +-----------+

# A factory function for DtDict
def datetime_tuple(year=None, month=None, day=None, weekday=None, hour=None,
                   minute=None, second=None, millisecond=None):
    for _ in range(8):
        if _ == 0:
            if year is not None:
                DtDict[yy] = year
            else:            
                DtDict[yy] = DtDfltDict[yy]
        elif _ == 1:
            if month is not None:
                DtDict[mo] = month
            else:
                DtDict[mo] = DtDfltDict[mo]
        elif _ == 2:
            if day is not None:
                DtDict[dd] = day
            else:
                DtDict[dd] = DtDfltDict[dd]
        elif _ == 3:
            if weekday is not None:
                DtDict[wd] = weekday
            else:
                DtDict[wd] = DtDfltDict[wd]
        elif _ == 4:
            if hour is not None:
                DtDict[hh] = hour
            else:
                DtDict[hh] = DtDfltDict[hh]
        elif _ == 5:
            if minute is not None:
                DtDict[mm] = minute
            else:
                DtDict[mm] = DtDfltDict[mm]
        elif _ == 6:
            if second is not None:
                DtDict[ss] = second
            else:
                DtDict[ss] = DtDfltDict[ss]
        elif _ == 7:
            if millisecond is not None:
                DtDict[ms] = millisecond
            else:
                DtDict[ms] = 0

    return (DtDict[yy],
            DtDict[mo],
            DtDict[dd],
            DtDict[wd],
            DtDict[hh],
            DtDict[mm],
            DtDict[ss],
            DtDict[ms])

def _bcd2bin(value):
    return (value or 0) - 6 * ((value or 0) >> 4)


def _bin2bcd(value):
    return (value or 0) + 6 * ((value or 0) // 10)

# Convert datetime DtDict into seconds since Jan 1, 2000
def tuple2seconds(datetime):
    return utime.mktime((DtDict[yy], DtDict[mo], DtDict[dd],
        DtDict[hh], DtDict[mm], DtDict[ss], DtDict[wd], 0))

#  Convert seconds since Jan 1, 2000 into a DateTime DtDict dictionary
def seconds2tuple(seconds):
    (year, month, day, hour, minute,
     second, weekday, _yday) = utime.localtime(seconds)

    return (DtDict[yy],
            DtDict[mo],
            DtDict[dd],
            DtDict[wd],
            DtDict[hh],
            DtDict[mm],
            DtDict[ss],
            0)

# +---------+
# | CLASSES |
# +---------+

class _BaseRTC:
    _SWAP_DAY_WEEKDAY = False

    def __init__(self, i2c, address=0x68): # 0x68 = 104 dec, 0x75 = 117 dec
        self.i2c = i2c
        self.address = address

    def _register(self, register, buffer=None):
        if buffer is None:
            return self.i2c.readfrom_mem(self.address, register, 1)[0]
        self.i2c.writeto_mem(self.address, register, buffer)

    def _flag(self, register, mask, value=None):
        data = self._register(register)
        if value is None:
            return bool(data & mask)
        if value:
            data |= mask
        else:
            data &= ~mask
        self._register(register, bytearray((data,)))

    def datetime(self, datetime=None):
        #print("_BaseRTC.datetime(): param datetime received: ", datetime)
        if datetime is None:
            # return the current datetime values from the rtc registers
            buffer = self.i2c.readfrom_mem(self.address,
                                           self._DATETIME_REGISTER, 7)
            if self._SWAP_DAY_WEEKDAY:
                day = buffer[3]
                weekday = buffer[4]
            else:
                day = buffer[4]
                weekday = buffer[3]
                
            DtDict[yy]=_bcd2bin(buffer[6]) + 2000
            DtDict[mo]=_bcd2bin(buffer[5])
            DtDict[dd]=_bcd2bin(day)
            DtDict[wd]=_bcd2bin(weekday)
            DtDict[hh]=_bcd2bin(buffer[2])
            DtDict[mm]=_bcd2bin(buffer[1])
            DtDict[ss]=_bcd2bin(buffer[0])
            DtDict[ms]=0
            
            retval = (DtDict[yy],
                DtDict[mo],
                DtDict[dd],
                DtDict[wd],
                DtDict[hh],
                DtDict[mm],
                DtDict[ss],
                0)
            #print("_BaseRTC.datetime() return value: ", retval)
            return retval
        else:
            # set the rtc registers with the values handed over 
            datetime = datetime_tuple(*datetime)
            buffer = bytearray(7)
            buffer[0] = _bin2bcd(datetime[ss])
            buffer[1] = _bin2bcd(datetime[mm])
            buffer[2] = _bin2bcd(datetime[hh])
            if self._SWAP_DAY_WEEKDAY:
                buffer[4] = _bin2bcd(datetime[wd])
                buffer[3] = _bin2bcd(datetime[dd])
            else:
                buffer[3] = _bin2bcd(datetime[wd])
                buffer[4] = _bin2bcd(datetime[dd])
            buffer[5] = _bin2bcd(datetime[mo])
            buffer[6] = _bin2bcd(datetime[yy] - 2000)
            self._register(self._DATETIME_REGISTER, buffer)
            #print("_BaseRTC.datetime() rtc set to: ", end='\n')
            #for _ in range(7):
            #    print("buffer[{}] = value {}".format(rtcRegsDict[_], _bcd2bin(buffer[_])), end='\n')


class DS3231(_BaseRTC):
    _CONTROL_REGISTER = 0x0e
    _STATUS_REGISTER = 0x0f
    _DATETIME_REGISTER = 0x00
    _ALARM_REGISTERS = (0x08, 0x0b)
    _SQUARE_WAVE_REGISTER = 0x0e

    # Return True if the clock lost the power recently and needs to be re-set.
    def lost_power(self):
        return self._flag(self._STATUS_REGISTER, 0b10000000)

    # get or set the value of the alarm flag. This is set to True when an alarm is triggered
    # and has to be cleared manually
    def alarm(self, value=None, alarm=0):
        return self._flag(self._STATUS_REGISTER,
                          0b00000011 & (1 << alarm), value)

    # Set interrupt for alarm
    def interrupt(self, alarm=0):
        return self._flag(self._CONTROL_REGISTER,
                          0b00000100 | (1 << alarm), 1)
    # Clear interrupt
    def no_interrupt(self):
        return self._flag(self._CONTROL_REGISTER, 0b00000011, 0)

    # get or set the status of the stop clock flag.
    # This can be used to start the clock at a precise moment in time.
    def stop(self, value=None):
        return self._flag(self._CONTROL_REGISTER, 0b10000000, value)

    # get or set the current time. The datetime is an 8-tuple of the format:
    # (year, month, day, weekday, hour, minute, second, millisecond)
    def datetime(self, datetime=None):
        #print("rtc.datetime(): parameter datetime received:", datetime)
        if datetime is not None:
            status = self._register(self._STATUS_REGISTER) & 0b01111111
            self._register(self._STATUS_REGISTER, bytearray((status,)))
        return super().datetime(datetime)
    
    # self evident
    def isLeapYear(self, year):
        return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
    
    # return the text representation of the day of the week.
    # for this the current value of DtDict[wd] is taken as key to the WeekdaysDict dictionary.
    def weekday(self):
        retval = "Unknown"
        try:
            retval = WeekdaysDict[DtDict[wd]]
        except KeyError:
             pass
        return retval
    
    # return the text respresentation of the month
    # the optional flag 'long' determines what type of text will be returned, e.g.: 'Sep' or 'September'
    # if parameter 'long' is not given. this flag defaults to 'False' (i.e.: the short version)
    def cur_month(self, month, long=False):
        retval = "Unknown"
        if month is not None:
            if month >= 1 and month <= 12:
                try:
                    if long:
                        retval = MonthsDict[month]
                    else:
                        retval = MonthsDictShort[month]
                except KeyError:
                    pass
        return retval
    
    # month is one based
    def daysInMonth(self, year, month):
        mdays = days_since_jan1[month] - days_since_jan1[month - 1]
        if (month == 2 and self.isLeapYear(year)):
            mdays += 1
        return mdays

    # compute the day of the year, between 1 and 366
    # month should be between 1 and 12, date should start at 1
    def yearday(self, year, month, date):
        yday = days_since_jan1[month - 1] + date
        if month >= 3 and self.isLeapYear(year):
            yday += 1
        return yday

    # Get or set the alarm time
    def alarm_time(self, datetime=None, alarm=0):
        if datetime is None:
            buffer = self.i2c.readfrom_mem(self.address,
                                           self._ALARM_REGISTERS[alarm], 3)
            day = None
            weekday = None
            second = None
            if buffer[2] & 0b10000000:
                pass
            elif buffer[2] & 0b01000000:
                day = _bcd2bin(buffer[2] & 0x3f)
            else:
                weekday = _bcd2bin(buffer[2] & 0x3f)
            minute = (_bcd2bin(buffer[0] & 0x7f)
                      if not buffer[0] & 0x80 else None)
            hour = (_bcd2bin(buffer[1] & 0x7f)
                    if not buffer[1] & 0x80 else None)
            if alarm == 0:
                # handle seconds
                buffer = self.i2c.readfrom_mem(
                    self.address, self._ALARM_REGISTERS[alarm] - 1, 1)
                second = (_bcd2bin(buffer[0] & 0x7f)
                          if not buffer[0] & 0x80 else None)
            return datetime_tuple(
                day=day,
                weekday=weekday,
                hour=hour,
                minute=minute,
                second=second,
            )
        datetime = datetime_tuple(*datetime)
        buffer = bytearray(3)
        buffer[0] = (_bin2bcd(datetime.minute)
                     if datetime.minute is not None else 0x80)
        buffer[1] = (_bin2bcd(datetime.hour)
                     if datetime.hour is not None else 0x80)
        if datetime.day is not None:
            if datetime.weekday is not None:
                raise ValueError("can't specify both day and weekday")
            buffer[2] = _bin2bcd(datetime.day)
        elif datetime.weekday is not None:
            buffer[2] = _bin2bcd(datetime.weekday) | 0b01000000
        else:
            buffer[2] = 0x80
        self._register(self._ALARM_REGISTERS[alarm], buffer)
        if alarm == 0:
            # handle seconds
            buffer = bytearray([_bin2bcd(datetime.second)
                                if datetime.second is not None else 0x80])
            self._register(self._ALARM_REGISTERS[alarm] - 1, buffer)

