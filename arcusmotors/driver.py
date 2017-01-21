import ctypes
from ctypes import cdll, POINTER, c_bool, c_void_p, c_long, c_int, byref
from utils.utils import resource_path

PERFORMAX_RETURN_SERIAL_NUMBER = 0x0
PERFORMAX_RETURN_DESCRIPTION = 0x1
PERFORMAX_MAX_DEVICE_STRLEN = 256

arcuslib = cdll.LoadLibrary(resource_path(
    "Performax_Linux_Driver_104/libarcus.so",pkg_name='arcusmotors'))
class usb_dev_handle(ctypes.Structure):
    pass
    #_pack_ = packed_on_windows_only
usb_dev_handle_p = ctypes.POINTER(usb_dev_handle)

arcuslib.fnPerformaxComGetNumDevices.restype = c_bool
arcuslib.fnPerformaxComGetProductString.restype = c_bool
arcuslib.fnPerformaxComOpen.restype = c_bool
arcuslib.fnPerformaxComClose.restype = c_bool
arcuslib.fnPerformaxComSetTimeouts.restype = c_bool
arcuslib.fnPerformaxComSendRecv.restype = c_bool
arcuslib.fnPerformaxComFlush.restype = c_bool

arcuslib.fnPerformaxComGetNumDevices.argtypes = [POINTER(c_long)]
arcuslib.fnPerformaxComGetProductString.argtypes = [c_long, c_void_p, c_long]
arcuslib.fnPerformaxComOpen.argtypes = [c_long, POINTER(usb_dev_handle_p)]
arcuslib.fnPerformaxComClose.argtypes = [POINTER(usb_dev_handle)]
arcuslib.fnPerformaxComSetTimeouts.argtypes = [c_long, c_long]
arcuslib.fnPerformaxComSendRecv.argtypes = [usb_dev_handle_p, c_void_p, c_long, c_long, c_void_p]
arcuslib.fnPerformaxComFlush.argtypes = [usb_dev_handle_p]


def GetNumDevices():
    nd = c_long()
    arcuslib.fnPerformaxComGetNumDevices(byref(nd))
    return nd

def GetProductString(num_device = 0, option = PERFORMAX_RETURN_SERIAL_NUMBER):
    long1 = c_long()
    long1.value = num_device
    long2 = c_long()
    long2.value = option
    cptr = ctypes.c_char_p(b'\0'*256)
    #voidptr = c_void_p()
    voidptr = ctypes.cast(cptr, c_void_p)
    ret = arcuslib.fnPerformaxComGetProductString(long1, voidptr, long2)
    return ret, ctypes.cast(voidptr,ctypes.c_char_p).value

def Open(device_num = 0):
    usb_handle = usb_dev_handle_p()
    arcuslib.fnPerformaxComOpen(device_num,byref(usb_handle))
    return usb_handle


def Close(usb_handle_p):
    return arcuslib.fnPerformaxComClose(usb_handle_p)


def SetTimeouts(readtimeout,writetimeout):
    readlong = c_long()
    readlong.value = readtimeout
    writelong = c_long()
    writelong.value = writetimeout
    return arcuslib.fnPerformaxComSetTimeouts(readlong,writelong)


def SendRecv(usb_handle_p,command_str):
    wrbufferptr = ctypes.c_char_p(command_str.encode('ascii'))
    wrbuffervoidptr = ctypes.cast(wrbufferptr,c_void_p)
    rbuffptr = ctypes.c_char_p(b'\0'*64)
    rvoidptr = ctypes.cast(rbuffptr,c_void_p)
    ret = arcuslib.fnPerformaxComSendRecv(usb_handle_p, wrbuffervoidptr, 64, 64, rvoidptr)
    print("Sent message:",ctypes.cast(wrbuffervoidptr,ctypes.c_char_p).value)
    print("Return message:",ctypes.cast(rvoidptr,ctypes.c_char_p).value)
    return ret, ctypes.cast(rvoidptr,ctypes.c_char_p).value


def Flush(usb_handle_p):
    return arcuslib.fnPerformaxComFlush(usb_handle_p)

#Above are all the commands which are accessed through the performax Driver.
#Below are functions specific to our project.

global motordict
motordict = {'camera':{'devnum':1,'devname':'SDE02','stepsperrev':200,'leadscrewpitch':0.635,'microstep':4},
            'sample':{'devnum':0,'devname':'SDE01','stepsperrev':200,'pulleyratio':16/60,'microstep':25}}

def initialize_motor(device_key):
    """Initializes motors for control.

    Initializes the Arcus ACE-SDE controllers to control the motors.
    After opening, checks to make sure the controller device name 'devname'
    matches the entry in the global variable 'motordict'.  If not, raises
    an assertion error.

    Args:
        device_key: key to access motordict dictionary.  Current 
        possibilities are 'camera' and 'sample'

    Returns:
        Nothing.  Maybe I should change that...
        It does however add the motor handle to the global variable
        under motordict[device_key]['handle']

    Raises:
        AssertionError: Device name did not match entry in motordict.
    """
    motorhandle = Open(motordict[device_key]['devnum'])
    SetTimeouts(1000,1000)
    Flush(motorhandle)
    assert str(SendRecv(motorhandle,'DN')[1],'utf-8') == motordict[device_key]['devname'], "Motor name error, check motor configuration"
    SendRecv(motorhandle,'EO=1')
    motordict[device_key]['handle'] = motorhandle
    print(device_key+" motor successfully initialized.")

def shutdown_motor(device_key):
    """Shuts down the motor USB connection.

    To re-initialize, call the inialize_motor function.

    Args:
        device_key: key to access motordict dictionary.  Current 
        possibilities are 'camera' and 'sample'
    """
    SendRecv(motordict[device_key]['handle'],'EO=0')
    Close(motordict[device_key]['handle'])

def send_message_str(string, device_key):
    """Send a message string to the controller.

    See the ACE-SDE manual for possible strings to send. Some
    useful examples are:
    'PX': current motor position (measured from start point)
    'J+': Jog+, move continually
    'DN': device name

    Args:
        string: command string to send to coontroller
        device_key: key to access motordict dictionary.  Current 
        possibilities are 'camera' and 'sample'
    """
    SendRecv(motordict[device_key]['handle'],string)

def go_to_degree(degree):
    """Move sample motor to angular position indicated by degree.
    
    This moves the sample rotator to the indicated position.
    Current implementation sets degree=0 to location at 
    powerup of the controller. Zero location can be reset
    by sending 'PX=0' string to the controller.

    Angular position is calculated based on configuration
    in motordict dictionary.  Calculation makes use of
    'pulleyratio', 'stepsperrev', and 'microstep'.

    Args:
        degree: Degree of position to rotate to.
    """
    steps = degree/360/motordict['sample']['pulleyratio']*motordict['sample']['stepsperrev']*motordict['sample']['microstep']
    xstr='X'+str(int(steps))
    SendRecv(motordict['sample']['handle'],xstr)

def go_to_mm(distance):
    """Move camera motor to position indicated by distance(mm).
    
    This moves the camera stage to the indicated position.
    Make sure to zero the controller out by using the 'L-'
    command string, so that distance=0 is properly calibrated.

    Distance (mm) is calculated based on configuration
    in motordict dictionary.  Calculation makes use of
    'leadscrewpitch', 'stepsperrev', and 'microstep'.

    Args:
        distance: Distance in mm to move the camera to.
    """
    steps = distance/motordict['camera']['leadscrewpitch']*motordict['camera']['stepsperrev']*motordict['camera']['microstep']
    xstr="X"+str(int(steps))
    print(xstr)
    SendRecv(motordict['camera']['handle'],xstr)

#motordict['camera']['handle'] = initialize_motor('camera')
#motordict['sample']['handle'] = initialize_motor('sample')

