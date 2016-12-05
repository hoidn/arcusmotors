import ctypes
from ctypes import cdll, POINTER, c_bool, c_void_p, c_long, c_int 

arcuslib = cdll.LoadLibrary("Performax_Linux_Driver_104/libarcus.so")
class usb_dev_handle(ctypes.Structure):
    pass
    #_pack_ = packed_on_windows_only
usb_dev_handle_p = ctypes.POINTER(usb_dev_handle)

#class AR_BOOL(Structure):
#    _fields_=[("i",c_int),
#              ("b1",POINTER(c_int)),
#              ("w1",POINTER(c_float))]

arcuslib.fnPerformaxComGetNumDevices.restype = c_bool
arcuslib.fnPerformaxComGetProductString.restype = c_bool
arcuslib.fnPerformaxComOpen.restype = c_bool
arcuslib.fnPerformaxComClose.restype = c_bool
arcuslib.fnPerformaxComSetTimeouts.restype = c_bool
arcuslib.fnPerformaxComSendRecv.restype = c_bool
arcuslib.fnPerformaxComFlush.restype = c_bool

arcuslib.fnPerformaxComGetNumDevices.argtypes = [POINTER(c_long)]
arcuslib.fnPerformaxComGetProductString.argtypes = [POINTER(c_long), c_void_p, POINTER(c_long)]
arcuslib.fnPerformaxComOpen.argtypes = [c_long, POINTER(usb_dev_handle_p)]
arcuslib.fnPerformaxComClose.argtypes = [usb_dev_handle_p]
arcuslib.fnPerformaxComSetTimeouts.argtypes = [c_long, c_long]
arcuslib.fnPerformaxComSendRecv.argtypes = [usb_dev_handle_p, c_void_p, c_long, c_long, c_void_p]
arcuslib.fnPerformaxComFlush.argtypes = [usb_dev_handle_p]


def fnPerformaxComGetNumDevices():
    nd = c_long()
    arcuslib.fnPerformaxComGetNumDevices(ctypes.byref(nd))
    return nd
