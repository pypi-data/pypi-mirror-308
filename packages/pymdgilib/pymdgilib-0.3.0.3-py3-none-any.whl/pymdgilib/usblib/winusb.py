"""WinUSB library wrapper functions

https://learn.microsoft.com/en-us/windows/win32/api/winusb

"""
from logging import getLogger
import platform
from enum import Enum
from ctypes import windll, POINTER, Structure, create_string_buffer, cast, c_uint8, c_uint16
from ctypes import wstring_at, byref, sizeof, resize
from ctypes.wintypes import DWORD, BYTE, USHORT, LPVOID, HANDLE, ULONG, BOOL
from pymdgilib.usblib.winsetupapi import SetupDiEnumDeviceInterfaces, SetupDiGetClassDevsW,\
            SetupDiGetDeviceInterfaceDetailW, SpDeviceInterfaceData, SpDeviceInterfaceDetailData,\
            SpDevinfoData, USB_WINUSB_GUID, DIGCF, winapi_result,\
            DEVPROPKEY_DEVICE_PARENT, SetupDiGetDevicePropertyW
from pymdgilib.usblib.winkernel32 import CreateFile, CloseHandle, GENERIC_READ, GENERIC_WRITE, FILE_SHARE_READ,\
                        FILE_SHARE_WRITE, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, FILE_FLAG_OVERLAPPED

if platform.architecture()[0].startswith('64'):
    WIN_PACK = 8
else:
    WIN_PACK = 1

# USB PIPE TYPE
PIPE_TYPE_CONTROL = 0
PIPE_TYPE_ISO = 1
PIPE_TYPE_BULK = 2
PIPE_TYPE_INTERRUPT = 3

class UsbDescriptorType(Enum):
    """USB descriptor types"""
    DEVICE                                  = 0x01
    CONFIGURATION	                        = 0x02
    STRING                                  = 0x03
    INTERFACE                               = 0x04
    ENDPOINT 	                            = 0x05
    DEVICE_QUALIFIER                        = 0x06
    OTHER_SPEED_CONFIGURATION               = 0x07
    INTERFACE_POWER                         = 0x08
    OTG 	                                = 0x09
    DEBUG                                   = 0x0a
    INTERFACE_ASSOCIATION 	                = 0x0b
    BOS                                     = 0x0f
    DEVICE_CAPABILITY                       = 0x10
    SUPERSPEED_ENDPOINT_COMPANION           = 0x30
    HUB_20                                  = 0x29
    HUB_30                                  = 0x2a
    SUPERSPEEDPLUS_ISOCH_ENDPOINT_COMPANION = 0x31

class Overlapped(Structure): #pylint: disable=too-few-public-methods
    """
    Represents the OVERLAPPED structure used in Windows for asynchronous I/O operations.

    This structure is used with functions like ReadFile, WriteFile, and other I/O functions
    that support overlapped I/O.

    Attributes
    ----------
    Internal : c_void_p
        Reserved for use by the operating system. Applications should not set this member.
    InternalHigh : c_void_p
        Reserved for use by the operating system. Applications should not set this member.
    Offset : c_ulong
        Specifies a file position at which to start the transfer. This is used with files
        that support byte offsets (e.g., files opened with CreateFile).
    OffsetHigh : c_ulong
        Specifies the high-order word of the byte offset at which to start the transfer.
        This is used when working with large files.
    Pointer : c_void_p
        Reserved for system use; it can be used to store a pointer to a buffer.
    hEvent : c_void_p
        A handle to an event that will be set to the signaled state when the operation has
        been completed.
    """
    _pack_ = WIN_PACK
    _fields_ = [
        ('Internal', LPVOID),
        ('InternalHigh', LPVOID),
        ('Offset', DWORD),
        ('OffsetHigh', DWORD),
        ('Pointer', LPVOID),
        ('hEvent', HANDLE)
    ]

class UsbSetupPacket(Structure): #pylint: disable=too-few-public-methods
    """
    USB Setup Packet Structure

    This structure represents the USB setup packet as defined by the USB specification.
    It is used for control transfers between the host and the device.

    Attributes:
        bmRequestType (c_uint8): Characteristics of the specific request.
        bRequest (c_uint8): Specific request.
        wValue (c_uint16): Word-sized field that varies according to the request.
        wIndex (c_uint16): Word-sized field that varies according to the request;
            typically used to pass an index or offset.
        wLength (c_uint16): Number of bytes to transfer if there is a data stage.
    """
    _fields_ = [
        ("bmRequestType", c_uint8),
        ("bRequest", c_uint8),
        ("wValue", c_uint16),
        ("wIndex", c_uint16),
        ("wLength", c_uint16)
    ]

    def __str__(self):
        """
        Return a string representation of the USB setup packet.
        """
        return (
            f"USB Setup Packet:\n"
            f"  bmRequestType: {self.bmRequestType:#04x}\n"
            f"  bRequest: {self.bRequest:#04x}\n"
            f"  wValue: {self.wValue:#06x}\n"
            f"  wIndex: {self.wIndex:#06x}\n"
            f"  wLength: {self.wLength:#06x}"
        )

class UsbDeviceDescriptor(Structure): #pylint: disable=too-few-public-methods
    """
    USB Device Descriptor Structure

    This class represents the USB device descriptor, which provides information about a USB device's characteristics.

    Attributes:
        bLength (c_uint8): Size of this descriptor in bytes.
        bDescriptorType (c_uint8): DEVICE Descriptor Type.
        bcdUSB (c_uint16): USB Specification Release Number in Binary-Coded Decimal.
        bDeviceClass (c_uint8): Class code (assigned by the USB-IF).
        bDeviceSubClass (c_uint8): Subclass code (assigned by the USB-IF).
        bDeviceProtocol (c_uint8): Protocol code (assigned by the USB-IF).
        bMaxPacketSize0 (c_uint8): Maximum packet size for endpoint zero.
        idVendor (c_uint16): Vendor ID (assigned by the USB-IF).
        idProduct (c_uint16): Product ID (assigned by the manufacturer).
        bcdDevice (c_uint16): Device release number in binary-coded decimal.
        iManufacturer (c_uint8): Index of string descriptor describing manufacturer.
        iProduct (c_uint8): Index of string descriptor describing product.
        iSerialNumber (c_uint8): Index of string descriptor describing the device's serial number.
        bNumConfigurations (c_uint8): Number of possible configurations.
    """
    _pack_ = 1  # Ensure the structure is packed
    _fields_ = [
        ("bLength", c_uint8),
        ("bDescriptorType", c_uint8),
        ("bcdUSB", c_uint16),
        ("bDeviceClass", c_uint8),
        ("bDeviceSubClass", c_uint8),
        ("bDeviceProtocol", c_uint8),
        ("bMaxPacketSize0", c_uint8),
        ("idVendor", c_uint16),
        ("idProduct", c_uint16),
        ("bcdDevice", c_uint16),
        ("iManufacturer", c_uint8),
        ("iProduct", c_uint8),
        ("iSerialNumber", c_uint8),
        ("bNumConfigurations", c_uint8)
    ]
    def __str__(self):
        txt = (
            f"USB Setup Packet:\n"
            f"  bLength: {self.bLength}\n"
            f"  bDescriptorType: {UsbDescriptorType(self.bDescriptorType).name} "
            f"({UsbDescriptorType(self.bDescriptorType).value})"
            f"  bcdUSB: {self.bcdUSB:#06x}\n"
    	    f"  bDeviceClass: {self.bDeviceClass:#04x}\n"
            f"  bDeviceSubClass: {self.bDeviceSubClass:#04x}\n"
            f"  bDeviceProtocol: {self.bDeviceProtocol:#04x}\n"
            f"  bMaxPacketSize0: {self.bMaxPacketSize0}\n"
            f"  idVendor: {self.idVendor:#06x}\n"
            f"  idProduct: {self.idProduct:#06x}\n"
            f"  bcdDevice: {self.bcdDevice:#06x}\n"
            f"  iManufacturer: {self.iManufacturer}\n"
            f"  iProduct: {self.iProduct}\n"
            f"  iSerialNumber: {self.iSerialNumber}\n"
            f"  bNumConfigurations: {self.bNumConfigurations}\n"
        )
        return txt

class UsbConfigurationDescriptor(Structure): #pylint: disable=too-few-public-methods
    """
    Represents a USB configuration descriptor.

    This descriptor provides information about a specific configuration of a USB device,
    including the number of interfaces, power consumption, and other attributes.

    Attributes
    ----------
    bLength : c_uint8
        Size of this descriptor in bytes.
    bDescriptorType : c_uint8
        CONFIGURATION Descriptor Type. Typically set to 2.
    wTotalLength : c_uint16
        Total length of data returned for this configuration. Includes the combined length
        of all descriptors (configuration, interface, endpoint, etc.) for this configuration.
    bNumInterfaces : c_uint8
        Number of interfaces supported by this configuration.
    bConfigurationValue : c_uint8
        Value to use as an argument to select this configuration.
    iConfiguration : c_uint8
        Index of string descriptor describing this configuration.
    bmAttributes : c_uint8
        Configuration characteristics. This is a bitmask that specifies attributes such as
        whether the device is self-powered or supports remote wakeup.
    bMaxPower : c_uint8
        Maximum power consumption of the USB device from the bus in this configuration,
        expressed in 2 mA units. For example, a value of 50 indicates a maximum power
        consumption of 100 mA.
    """
    _pack_ = 1  # Ensure the structure is packed with no padding
    _fields_ = [
        ("bLength", c_uint8),
        ("bDescriptorType", c_uint8),
        ("wTotalLength", c_uint16),
        ("bNumInterfaces", c_uint8),
        ("bConfigurationValue", c_uint8),
        ("iConfiguration", c_uint8),
        ("bmAttributes", c_uint8),
        ("bMaxPower", c_uint8)
    ]
    def __str__(self):
        txt = (
            "USB configuration descriptor:\n"
            f"  bLength: {self.bLength}\n"
            f"  bDescriptorType: {UsbDescriptorType(self.bDescriptorType).name} "
            f"({UsbDescriptorType(self.bDescriptorType).value})\n"
            f"  wTotalLength: {self.wTotalLength}\n"
            f"  bNumInterfaces: {self.bNumInterfaces}\n"
            f"  bConfigurationValue: {self.bConfigurationValue}\n"
            f"  iConfiguration: {self.iConfiguration}\n"
            f"  bmAttributes: {self.bmAttributes}\n"
            f"  bMaxPower: {self.bMaxPower}\n"
        )
        return txt

class UsbInterfaceDescriptor(Structure): #pylint: disable=too-few-public-methods
    """
    USB Interface Descriptor Structure

    This structure represents the USB interface descriptor as defined by the USB specification.
    It provides information about a specific interface within a USB device.

    Attributes:
        bLength (c_uint8): Size of this descriptor in bytes.
        bDescriptorType (c_uint8): Descriptor type (constant value 4 for interface descriptor).
        bInterfaceNumber (c_uint8): Number of this interface.
        bAlternateSetting (c_uint8): Value used to select this alternate setting.
        bNumEndpoints (c_uint8): Number of endpoints used by this interface (excluding endpoint 0).
        bInterfaceClass (c_uint8): Class code (assigned by the USB-IF).
        bInterfaceSubClass (c_uint8): Subclass code (assigned by the USB-IF).
        bInterfaceProtocol (c_uint8): Protocol code (assigned by the USB-IF).
        iInterface (c_uint8): Index of string descriptor describing this interface.
    """
    _pack_ = 1
    _fields_ = [
        ("bLength", c_uint8),
        ("bDescriptorType", c_uint8),
        ("bInterfaceNumber", c_uint8),
        ("bAlternateSetting", c_uint8),
        ("bNumEndpoints", c_uint8),
        ("bInterfaceClass", c_uint8),
        ("bInterfaceSubClass", c_uint8),
        ("bInterfaceProtocol", c_uint8),
        ("iInterface", c_uint8)
    ]
    def __str__(self):
        txt = (
            "USB interface descriptor:\n"
            f"  bLength: {self.bLength}\n"
            f"  bDescriptorType: {UsbDescriptorType(self.bDescriptorType).name} "
            f"({UsbDescriptorType(self.bDescriptorType).value})\n"
            f"  bInterfaceNumber: {self.bInterfaceNumber}\n"
            f"  bAlternateSetting: {self.bAlternateSetting}\n"
            f"  bNumEndpoints: {self.bNumEndpoints}\n"
            f"  bInterfaceClass: {self.bInterfaceClass}\n"
            f"  bInterfaceSubClass: {self.bInterfaceSubClass}\n"
            f"  bInterfaceProtocol: {self.bInterfaceProtocol}\n"
            f"  iInterface: {self.iInterface}\n"
        )
        return txt

class PipeInfo(Structure):#pylint: disable=too-few-public-methods
    """
    A class to represent the information about a USB pipe.

    Attributes
    ----------
    pipe_type : ULONG
        The type of the pipe (e.g., control, isochronous, bulk, interrupt).
    pipe_id : BYTE
        The identifier for the pipe.
    maximum_packet_size : USHORT
        The maximum packet size that the pipe can handle.
    interval : USHORT
        The interval for polling the endpoint for data transfers (relevant for interrupt and isochronous pipes).

    Fields
    ------
    _pack_ : int
        The alignment of the structure in memory.
    _fields_ : list of tuples
        The fields of the structure, each defined as a tuple with the field name, type, and optionally, size.
    """
    _pack_ = WIN_PACK
    _fields_ = [
        ("pipe_type", ULONG),
        ("pipe_id", BYTE),
        ("maximum_packet_size", USHORT),
        ("interval", USHORT)
    ]
    def __str__(self):
        """
        Return a string representation of the pipe info.
        """
        return (
            f"USB pipe info:\n"
            f"  Pipe type: {self.pipe_type}\n"
            f"  Pipe id: {self.pipe_id:#04x}\n"
            f"  Maximum packet size: {self.maximum_packet_size}\n"
            f"  interval: {self.interval}\n"
        )

WinUsb_Initialize = windll.winusb.WinUsb_Initialize
WinUsb_Initialize.restype = BOOL
WinUsb_Initialize.argtypes = [HANDLE, # _In_ HANDLE DeviceHandle
                              POINTER(HANDLE)] #  _Out_  PWINUSB_INTERFACE_HANDLE InterfaceHandle

WinUsb_Free = windll.winusb.WinUsb_Free
WinUsb_Free.restype = BOOL
WinUsb_Free.argtypes = [HANDLE] # [in]  WINUSB_INTERFACE_HANDLE  InterfaceHandle,

WinUsb_GetDescriptor = windll.winusb.WinUsb_GetDescriptor
WinUsb_GetDescriptor.restype = BOOL
WinUsb_GetDescriptor.argtypes = [POINTER(HANDLE), #[in]  WINUSB_INTERFACE_HANDLE InterfaceHandle,
                                 BYTE, #[in]  UCHAR DescriptorType,
                                 BYTE, #[in]  UCHAR Index,
                                 USHORT,#[in]  USHORT LanguageID,
                                 POINTER(BYTE),#[out] PUCHAR Buffer,
                                 ULONG,#[in]  ULONG BufferLength,
                                 POINTER(ULONG)]# [out] PULONG LengthTransferred

WinUsb_ReadPipe = windll.winusb.WinUsb_ReadPipe
WinUsb_ReadPipe.restype = BOOL
WinUsb_ReadPipe.argtypes = [HANDLE,#[in] WINUSB_INTERFACE_HANDLE InterfaceHandle,
                            BYTE,#[in] UCHAR PipeID,
                            POINTER(BYTE),#[out] PUCHAR Buffer,
                            ULONG,#[in] ULONG BufferLength,
                            POINTER(ULONG),#[out, optional] PULONG LengthTransferred,
                            POINTER(Overlapped)]#[in, optional] LPOVERLAPPED Overlapped

WinUsb_WritePipe = windll.winusb.WinUsb_WritePipe
WinUsb_WritePipe.restype = BOOL
WinUsb_WritePipe.argtypes = [HANDLE,#[in] WINUSB_INTERFACE_HANDLE InterfaceHandle,
                             BYTE,#[in] UCHAR PipeID,
                             POINTER(BYTE),#[in] PUCHAR Buffer,
                             ULONG,#[in] ULONG BufferLength,
                             POINTER(ULONG),#[out, optional] PULONG LengthTransferred,
                             POINTER(Overlapped)]#[in, optional] LPOVERLAPPED Overlapped

# [in]  WINUSB_INTERFACE_HANDLE  InterfaceHandle,
# [in]  UCHAR                    AssociatedInterfaceIndex,
# [out] PWINUSB_INTERFACE_HANDLE AssociatedInterfaceHandle
WinUsb_GetAssociatedInterface = windll.winusb.WinUsb_GetAssociatedInterface
WinUsb_GetAssociatedInterface.restype = BOOL
WinUsb_GetAssociatedInterface.argtypes = [HANDLE, BYTE, POINTER(HANDLE)]

# BOOL WinUsb_QueryInterfaceSettings(
#  [in]  WINUSB_INTERFACE_HANDLE   InterfaceHandle,
#  [in]  UCHAR                     AlternateInterfaceNumber,
#  [out] PUSB_INTERFACE_DESCRIPTOR UsbAltInterfaceDescriptor
WinUsb_QueryInterfaceSettings = windll.winusb.WinUsb_QueryInterfaceSettings
WinUsb_QueryInterfaceSettings.restype = BOOL
#WinUsb_QueryInterfaceSettings.argtypes = [HANDLE, BYTE, POINTER(UsbInterfaceDescriptor)]

#BOOL WinUsb_QueryPipe(
#  [in]  WINUSB_INTERFACE_HANDLE  InterfaceHandle,
#  [in]  UCHAR                    AlternateInterfaceNumber,
#  [in]  UCHAR                    PipeIndex,
#  [out] PWINUSB_PIPE_INFORMATION PipeInformation
WinUsb_QueryPipe = windll.winusb.WinUsb_QueryPipe
WinUsb_QueryPipe.restype = BOOL
#WinUsb_QueryPipe.argtypes = [HANDLE, BYTE, BYTE, POINTER(PipeInfo)]

def list_winusb_devices():
    """
    List WinUSB devices.

    This function enumerates all currently connected WinUSB devices and retrieves detailed information
    about each device, including the device path and serial number. If the device is a composite device,
    it also retrieves the parent device's serial number.

    :return: A list of dictionaries, each containing information about a WinUSB device.
    :rtype: list of dict

    Each dictionary in the returned list contains the following keys:

    - **path** (*str*): The device path.
    - **serial_number** (*str*): The device serial number in upper case.
    - **parent_path** (*str*, optional): The parent device path, if the device is a composite device.
    - **interface_number** (*int*, optional): The interface number, if the device is a composite device.

    :raises Exception: If any of the Windows API calls fail.
    """
    required_size = ULONG(0)
    member_index = DWORD(0)
    sp_device_info_data = SpDevinfoData()
    sp_device_info_data.cb_size = sizeof(SpDevinfoData)
    sp_device_interface_data = SpDeviceInterfaceData()
    sp_device_interface_data.cb_size = sizeof(sp_device_interface_data)
    sp_device_interface_detail_data = SpDeviceInterfaceDetailData()

    # Get a handle to a list of currently enumerated WinUSB devices
    h_info = SetupDiGetClassDevsW(byref(USB_WINUSB_GUID), None, None, (DIGCF.PRESENT | DIGCF.DEVICEINTERFACE))
    winapi_result(h_info)
    devices = []
    # iterate over the list of WinUSB devices to get more information on each of them
    while SetupDiEnumDeviceInterfaces(h_info, None, byref(USB_WINUSB_GUID), member_index,
                                        byref(sp_device_interface_data)):

        # Get required size for sp_device_interface_data
        ret = SetupDiGetDeviceInterfaceDetailW(h_info, byref(sp_device_interface_data), None, 0,
                                                byref(required_size), None)
        # Only raise an exception if required size value is also 0
        if ret == 0 and required_size.value == 0:
            winapi_result(ret)
        resize(sp_device_interface_detail_data, required_size.value)
        sp_device_interface_detail_data.cb_size = sizeof(SpDeviceInterfaceDetailData)
        ret = SetupDiGetDeviceInterfaceDetailW(h_info, byref(sp_device_interface_data),
                                        byref(sp_device_interface_detail_data), required_size, byref(required_size),
                                        byref(sp_device_info_data))
        winapi_result(ret)
        path = wstring_at(byref(sp_device_interface_detail_data, sizeof(DWORD)))

        device = parse_device_path(path)
        device["path"] = path
        # Different path types can have serial number in upper or lower case
        # To be consistent we reside to upper case which also matches the actual
        # format of the Gen4 device serial numbers.
        device["serial_number"] = device["serial_number"].upper()

        # If we have an interface number it is a composite device
        # and we need to get the parent to obtain the serial number
        if "interface_number" in device:
            property_type = ULONG(0)
            property_buffer = (BYTE * 256)()
            property_buffer_size = DWORD(sizeof(property_buffer))
            required_size = DWORD(0)
            # Get the device parent property
            ret = SetupDiGetDevicePropertyW(h_info, byref(sp_device_info_data),
                                        byref(DEVPROPKEY_DEVICE_PARENT),
                                        byref(property_type),
                                        property_buffer,
                                        property_buffer_size,
                                        byref(required_size),
                                        DWORD(0))
            winapi_result(ret)
            path = wstring_at(byref(property_buffer))
            device["parent_path"] = path
            parent = parse_device_path(path)
            device["serial_number"] = parent["serial_number"].upper()

        devices.append(device)

        member_index.value = member_index.value + 1
    return devices

def parse_device_path(path):
    r"""Parse Windows USB device path.

    Extracts USB vendor ID, product ID and serial number from a Windows device path.
    Example paths:
    \\?\usb#vid_03eb&pid_2175&mi_03#6&319d7dcd&1&0003#{dee824ef-729b-4a0e-9c14-b7117d33a817}
    \\?\usb#vid_04d8&pid_9018#bur182626045#{dee824ef-729b-4a0e-9c14-b7117d33a817}
    USB\VID_03EB&PID_2175\ATML3203081800009066

    :param path: Windows USB device path
    :type path: str
    :return: Vendor ID, product ID and serial number for non composite devices.
             Vendor ID, product ID, interface number for composite devices.
    :rtype: dict
    """
    device = {}
    try:
        _, vid_pid_mi, device["serial_number"],_ = path.split("#", 3)
    except ValueError:
        _, vid_pid_mi, device["serial_number"] = path.split("\\", 2)
    tmp = vid_pid_mi.lower().split("&")
    device["vendor_id"] = int(tmp[0].strip("vid_"), 16)
    device["product_id"] = int(tmp[1].strip("pid_"), 16)
    if len(tmp) == 3:
        device["interface_number"] = int(tmp[2].strip("mi_"))

    return device

class WinUsb():
    """WinUSB API"""
    def __init__(self):
        """
        Initialize the WinUsb object.

        This method sets up the initial state of the WinUsb object, including
        setting the file handle, WinUSB handle, and logger.
        """
        self.file_handle = None
        self.winusb_handle = None
        self.logger = getLogger(__name__)

    @classmethod
    def filter_devices(cls, devices, vendor_id=None, product_id=None, serialnumber=None):
        """Filter a list of devices based on vendor ID, product ID, and serial number.

        :param devices: List of devices to filter.
        :param vendor_id: USB Vendor ID as a match criteria, defaults to None.
        :param product_id: USB Product ID as a match criteria, defaults to None.
        :param serialnumber: USB Serial Number as a match criteria, defaults to None.
        :return: List of devices that match the criteria.
        """
        devices = [device for device in devices if cls.device_filter(
                    device, vendor_id=vendor_id, product_id=product_id, serialnumber=serialnumber)]
        return devices

    @staticmethod
    def device_filter(device, vendor_id=None, product_id=None, serialnumber=None):
        """Filter to find specific DGI devices

        All parameters that are not None will be used in the matching
        algorithm and there will only be a match if all of these are equal to
        the provided corresponding members of the device.

        :param device: Device to test for a match
        :type device: DgiDevice
        :param vendor_id: USB Vendor ID as a match criteria, defaults to None
        :type vendor_id: int, optional
        :param product_id: USB product ID as a match criteria, defaults to None
        :type product_id: int, optional
        :param serialnumber: USB serial number as a match criteria, defaults to None
        :type serialnumber: str, optional
        :return: Match result
        :rtype: bool
        """
        match = True
        if vendor_id is not None:
            match = match and bool(device["vendor_id"] == vendor_id)
        if product_id is not None:
            match = match and bool(device["product_id"] == product_id)
        if serialnumber is not None:
            match = match and bool(device["serial"] == serialnumber)
        return match

    @classmethod
    def find_devices(cls, vendor_id=None, product_id=None, serialnumber=None):
        """
        Find and filter USB devices based on the provided criteria.

        :param vendor_id: USB Vendor ID as a match criteria, defaults to None.
        :type vendor_id: int, optional
        :param product_id: USB Product ID as a match criteria, defaults to None.
        :type product_id: int, optional
        :param serialnumber: USB Serial Number as a match criteria, defaults to None.
        :type serialnumber: str, optional
        :return: List of filtered devices.
        :rtype: list
        """
        devices = list_winusb_devices()
        filtered_device_list = cls.filter_devices(devices, vendor_id=vendor_id,
                                                  product_id=product_id,
                                                  serialnumber=serialnumber)
        return filtered_device_list

    def open(self, path):
        """
        Open a WinUSB device.

        :param path: Path to the device (wstring).
        :type path: str
        :raises Exception: If the device cannot be opened.
        """
        self.winusb_handle = HANDLE()
        self.file_handle = CreateFile(path, GENERIC_WRITE | GENERIC_READ, FILE_SHARE_WRITE | FILE_SHARE_READ,
                                      None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL | FILE_FLAG_OVERLAPPED, None)
        if self.file_handle == HANDLE(-1):
            winapi_result(False)
        ret = WinUsb_Initialize(self.file_handle, byref(self.winusb_handle))
        winapi_result(ret)

    def close(self):
        """
        Close the WinUSB device.

        :return: Boolean indicating if both file and WinUSB handles were successfully closed.
        :rtype: bool
        """
        ret_file = WinUsb_Free(self.winusb_handle)
        ret_winusb = CloseHandle(self.file_handle)
        return ret_file and ret_winusb

    def write(self, endpoint, data):
        """
        Write data to a specified endpoint.

        :param endpoint: Endpoint to write to.
        :type endpoint: int
        :param data: Data to write.
        :type data: bytes
        :return: Number of bytes written.
        :rtype: int
        """
        data = bytearray(data)
        write_buf = (BYTE * len(data)).from_buffer(data)
        written =ULONG(0)
        ret = WinUsb_WritePipe(self.winusb_handle,
                               BYTE(endpoint),
                               write_buf,
                               ULONG(len(write_buf)),
                               byref(written), None)
        winapi_result(ret)
        return written.value

    def read(self, endpoint, size):
        """
        Read data from a specified endpoint.

        :param endpoint: Endpoint to read from.
        :type endpoint: int
        :param size: Number of bytes to read.
        :type size: int
        :return: Data read from the endpoint.
        :rtype: bytes
        """
        read_buffer = create_string_buffer(size)
        read = ULONG(0)
        ret = WinUsb_ReadPipe(self.winusb_handle,
                              BYTE(endpoint),
                              cast(read_buffer, POINTER(BYTE)),
                              ULONG(size),
                              byref(read),
                              None)
        winapi_result(ret)
        return read_buffer.raw[:read.value]

    def get_interface_descriptor(self):
        """
        Retrieve the interface descriptor.

        :return: Interface descriptor.
        :rtype: UsbInterfaceDescriptor
        """
        iface = UsbInterfaceDescriptor()
        read = ULONG(0)
        ret = WinUsb_GetDescriptor(self.winusb_handle,
                                   BYTE(UsbDescriptorType.INTERFACE.value),
                                   0,
                                   0,
                                   cast(byref(iface), POINTER(BYTE)),
                                   ULONG(sizeof(UsbInterfaceDescriptor)),
                                   byref(read))
        winapi_result(ret)
        return iface

    def get_usb_device_descriptor(self, handle=None):
        """
        Retrieve the USB device descriptor.

        Note: This will only work if the first interface of a USB composite device
        is registered with WinUSB.

        :param handle: Handle to the device, defaults to None.
        :type handle: HANDLE, optional
        :return: USB device descriptor.
        :rtype: UsbDeviceDescriptor
        """
        device_desc = UsbDeviceDescriptor()
        read = ULONG(0)
        if handle is None:
            handle = self.winusb_handle
        ret = WinUsb_GetDescriptor(handle,
                                   BYTE(UsbDescriptorType.DEVICE.value),
                                   0,
                                   0,
                                   cast(byref(device_desc), POINTER(BYTE)),
                                   ULONG(sizeof(UsbDeviceDescriptor)),
                                   byref(read))
        winapi_result(ret)
        return device_desc

    def get_configuration_descriptor(self, index) -> UsbConfigurationDescriptor:
        """
        Retrieve the configuration descriptor.

        :param index: Index of the configuration descriptor.
        :type index: int
        :return: Configuration descriptor.
        :rtype: UsbConfigurationDescriptor
        """
        config_desc = UsbConfigurationDescriptor()
        read = ULONG(0)
        ret = WinUsb_GetDescriptor(self.winusb_handle,
                                   BYTE(UsbDescriptorType.CONFIGURATION.value),
                                   index,
                                   0,
                                   cast(byref(config_desc), POINTER(BYTE)),
                                   ULONG(sizeof(UsbConfigurationDescriptor)),
                                   byref(read))
        winapi_result(ret)
        return config_desc

    def get_associated_interface(self, index):
        """
        Retrieve the associated interface.

        Note: For a composite device this will only work if the interfaces are registered with WinUSB.

        :param index: Index of the associated interface.
        :type index: int
        :return: Handle to the associated interface.
        :rtype: HANDLE
        """
        associated_iface = HANDLE()
        ret = WinUsb_GetAssociatedInterface(self.winusb_handle, index, byref(associated_iface))
        winapi_result(ret)
        return associated_iface

    def query_interface_settings(self, alternate_setting=0):
        """
        Query the interface settings.

        This works on composite class interfaces and will return the interface
        information of the currently opened interface. In contrast to Windows
        API documentation, it is not possible to obtain other interfaces of a
        composite device, just the one we have opened.

        :param alternate_setting: Alternate setting number, defaults to 0.
        :type alternate_setting: int, optional
        :return: Interface descriptor.
        :rtype: UsbInterfaceDescriptor
        """
        interface_desc = UsbInterfaceDescriptor()
        ret = WinUsb_QueryInterfaceSettings(self.winusb_handle, alternate_setting, byref(interface_desc))
        winapi_result(ret)
        return interface_desc

    def query_pipe_info(self, alternate_intf_number, pipe) -> PipeInfo:
        """
        Query pipe information.

        :param alternate_intf_number: Alternate interface number.
        :type alternate_intf_number: int
        :param pipe: Pipe number.
        :type pipe: int
        :return: Pipe information.
        :rtype: PipeInfo
        """
        pipe_info = PipeInfo()
        ret = WinUsb_QueryPipe(self.winusb_handle, alternate_intf_number, pipe, byref(pipe_info))
        winapi_result(ret)
        return pipe_info
