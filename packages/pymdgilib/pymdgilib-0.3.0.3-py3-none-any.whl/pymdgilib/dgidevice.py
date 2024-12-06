""" DGI USB device

On Linux the udev rules need to be adjusted to provide user level access
to the usb subsytem and the specific device.

Another approach e.g. on WSL where udev is not active is to modify the access
rights on the specific USB device in /dev/bus/usb/
For example:
sudo chmod o+rw /dev/bus/usb/001/003
where the in this case the 001 is the bus ID and the 002 is the device ID which can be obtained with e.g. lsusb
Bus 001 Device 003: ID 03eb:2175 Atmel Corp. nEDBG CMSIS-DAP

"""
import platform
from array import array
from dataclasses import dataclass
from itertools import tee
from typing import Union
import usb.core

if platform.system() == "Windows":
    from pymdgilib.usblib.winusb import WinUsb, list_winusb_devices

class UsbError(Exception):
    """Generic excpetion for USB backend errors"""

@dataclass
class DgiDevice:
    """DGI device information"""
    vendor_id: int
    product_id: int


nedbg = DgiDevice(0x03eb, 0x2175)
edbg = DgiDevice(0x3eb, 0x2111)
power_debugger = DgiDevice(0x3eb, 0x2144)
atmel_ice = DgiDevice(0x3eb, 0x2141)

class UsbBackend():
    """Base class for USB backends"""
    @classmethod
    def filter_dgi_devices(cls, devices: list, vendor_id: int = None, product_id: int = None, serialnumber: str = None):
        """Filter a list of devices based on vendor ID, product ID, and serial number.

        :param devices: List of devices to filter.
        :param vendor_id: USB Vendor ID as a match criteria, defaults to None.
        :param product_id: USB Product ID as a match criteria, defaults to None.
        :param serialnumber: USB Serial Number as a match criteria, defaults to None.
        :return: List of devices that match the criteria.
        """
        devices = [device for device in devices if
                   cls.dgi_device_filter(device, vendor_id=vendor_id, product_id=product_id, serialnumber=serialnumber)]
        return devices

    @staticmethod
    def dgi_device_filter(device: dict, vendor_id=None, product_id=None, serialnumber=None):
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

if platform.system() == "Windows":
    from pymdgilib.usblib.winusb import WinUsb, list_winusb_devices
    class WinUsbBackend(UsbBackend):
        """
        USB backend for Windows using WinUSB
        """
        def __init__(self):
            self.device = None
            self.in_endpoint_address = None
            self.out_endpoint_address = None
            self.usb_packet_size = 0

        def open(self, device):
            """
            Open a connection to a USB device.

            :param device: Device to open
            :type device: dict
            """
            self.device = WinUsb()
            self.device.open(device["path"])

            pipe_info = self.device.query_pipe_info(0, 0)
            self.usb_packet_size = pipe_info.maximum_packet_size
            if pipe_info.pipe_id & 0x80: # Test if it is an in-endpoint
                self.in_endpoint_address = pipe_info.pipe_id
            else:
                self.out_endpoint_address = pipe_info.pipe_id

            pipe_info = self.device.query_pipe_info(0, 1)
            if pipe_info.pipe_id & 0x80: # Test if it is an in-endpoint
                self.in_endpoint_address = pipe_info.pipe_id
            else:
                self.out_endpoint_address = pipe_info.pipe_id

        def close(self):
            """
            Close the connection to the USB device.
            """
            if self.device is not None:
                self.device.close()
                self.device = None

        def find_dgi_devices(self, serialnumber=None):
            """
            Find all connected DGI devices.

            :param serialnumber: USB Serial Number as a match criteria, defaults to None.
            :type serialnumber: str, optional
            :return: List of DGI devices that match the criteria.
            :rtype: list
            """
            devices = []

            winusb_devices = list_winusb_devices()
            nedbg_devices = self.filter_dgi_devices(winusb_devices,
                                                    vendor_id=nedbg.vendor_id,
                                                    product_id=nedbg.product_id,
                                                    serialnumber=serialnumber)
            devices.extend(nedbg_devices)
            edbg_devices = self.filter_dgi_devices(winusb_devices,
                                                vendor_id=edbg.vendor_id,
                                                product_id=edbg.product_id,
                                                serialnumber=serialnumber)
            devices.extend(edbg_devices)
            power_debuggers = self.filter_dgi_devices(winusb_devices,
                                                vendor_id=power_debugger.vendor_id,
                                                product_id=power_debugger.product_id,
                                                serialnumber=serialnumber)
            devices.extend(power_debuggers)

            return devices

        def write(self, cmd: Union[bytes, bytearray]):
            """
            Write a command to the USB device.

            :param cmd: Command to write
            :type cmd: bytes, bytearray
            """
            self.device.write(self.out_endpoint_address, cmd)

        def read(self, size: int) -> bytes:
            """
            Read a response from the USB device.

            :param size: Number of bytes to read
            :type size: int
            :return: Response from the device
            :rtype: bytes
            """
            response = self.device.read(self.in_endpoint_address, size)
            return response

class LibUsbBackend(UsbBackend):
    """
    USB backend for Linux/MAC using libusb
    """
    def __init__(self):
        self.device = None
        self.in_endpoint_address = None
        self.out_endpoint_address = None
        self.usb_packet_size = 0

    def get_configuration(self):
        """
        Get the active configuration of the USB device and extract
        endpoint information.
        """
        cfg = self.device.get_active_configuration()

        # All currently supported tools have DGI as interface number 3
        # but other devices might not
        intf = cfg[(3,0)] # interface 3 configuration 0

        endpoints = list(intf)
        if len(endpoints) != 2:
            raise UsbError("Unexpected number of endpoints in nEDBG DGI interface")
        for endpoint in endpoints:
            if endpoint.bEndpointAddress & 0x80:
                self.in_endpoint_address = endpoint.bEndpointAddress
            else:
                self.out_endpoint_address = endpoint.bEndpointAddress
        self.usb_packet_size = intf[0].wMaxPacketSize

    def open(self, device):
        """
        Open a connection to a USB device.

        :param device: Device to open
        :type device: usb.core.Device
        """
        self.device = device
        self.get_configuration()

    def close(self):
        """
        Close the connection to the USB device.
        """
        if self.device is not None:
            self.device = None

    def find_dgi_devices(self, serialnumber=None):
        """
        Find all connected DGI devices.

        :param serialnumber: USB Serial Number as a match criteria, defaults to None.
        :type serialnumber: str, optional
        :return: List of DGI devices that match the criteria.
        :rtype: list
        """
        devices = []
        # the find method returns an iterator that would be consumed after an iteration but
        # we want to do several iterations here, one for each DGI device type, so we
        # generate multiple independent generators with the tee function
        libusb_devices = usb.core.find(find_all=True)
        devs1, devs2, devs3 = tee(libusb_devices, 3)
        nedbg_devices = self.filter_dgi_devices(devs1,
                                                vendor_id=nedbg.vendor_id,
                                                product_id=nedbg.product_id,
                                                serialnumber=serialnumber)
        devices.extend(nedbg_devices)
        edbg_devices = self.filter_dgi_devices(devs2,
                                               vendor_id=edbg.vendor_id,
                                               product_id=edbg.product_id,
                                               serialnumber=serialnumber)
        devices.extend(edbg_devices)
        power_debuggers = self.filter_dgi_devices(devs3,
                                               vendor_id=power_debugger.vendor_id,
                                               product_id=power_debugger.product_id,
                                               serialnumber=serialnumber)
        devices.extend(power_debuggers)

        return devices

    def write(self, cmd: Union[bytes, bytearray]):
        """
        Write a command to the USB device.

        :param cmd: Command to write
        :type cmd: bytes or bytearray
        """
        array('B', cmd)
        self.device.write(self.out_endpoint_address, cmd)

    def read(self, size: int) -> bytes:
        """
        Read a response from the USB device.

        :param size: Number of bytes to read
        :type size: int
        :return: Response from the device
        :rtype: bytes
        """
        response = self.device.read(self.in_endpoint_address, size)
        response = response.tobytes()
        return response

    @staticmethod
    def dgi_device_filter(device: dict, vendor_id=None, product_id=None, serialnumber=None):
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
            match = match and bool(device.idVendor == vendor_id)
        if product_id is not None:
            match = match and bool(device.idProduct == product_id)
        if serialnumber is not None:
            match = match and bool(device.serial_number == serialnumber)
        return match

def get_usb_backend():
    """Get USB backend

    Will return a backend instance based on the used platform.
    For Windows it will be a WinUSB backend, for MAC and Linux it will be a
    libusb backend.

    :return: USB backend
    :rtype: WinUsbBackend or LibUsbBackend
    """
    if platform.system() == "Windows":
        return WinUsbBackend()
    return LibUsbBackend()
