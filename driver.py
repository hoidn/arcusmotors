import ctypes
from ctypes import cdll, POINTER, c_bool, c_void_p, c_long, c_int, byref

PERFORMAX_RETURN_SERIAL_NUMBER = 0x0
PERFORMAX_RETURN_DESCRIPTION = 0x1
PERFORMAX_MAX_DEVICE_STRLEN = 256

arcuslib = cdll.LoadLibrary("Performax_Linux_Driver_104/libarcus.so")
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
    return ret, voidptr

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
    print(ctypes.cast(rvoidptr,ctypes.c_char_p).value)
    return ret, rvoidptr


def Flush(usb_handle_p):
    return arcuslib.fnPerformaxComFlush(usb_handle_p)

