"""DGI info example

This example gets information from a DGI e.g. version, available interfaces ...
and prints it to stdout.
"""
import sys
from pymdgilib.dgidevice import UsbError, get_usb_backend
from pymdgilib.dgi import Dgi, DgiInterface, DgiProtocolError

DEVICE_SERIALNUMBER = None
if __name__ == "__main__":

    try:
        backend = get_usb_backend()
        devices = backend.find_dgi_devices(serialnumber=DEVICE_SERIALNUMBER)
        if 1 < len(devices):
            print("More than one DGI interface found. Please specify interface by providing serial number")
            sys.exit(1)
        if 0 == len(devices):
            print("No DGI interface found.")
            sys.exit(1)
        backend.open(devices[0])
        dgi = Dgi(backend)

        interface_description = dgi.sign_on()
        print(f"DGI Interface Description: {interface_description}")
        major, minor = dgi.get_version()
        print(f"DGI Version: {major}.{minor}")

        interfaces = dgi.list_interfaces()
        print("\nDGI Interfaces:")
        for interface in interfaces:
            print(f"{interface.name} ({hex(interface.value)})")

        print("")
        print("DGI Interface status:")
        status = dgi.get_interfaces_status()
        dgi.print_interfaces_status(status)

        print("")
        print("GPIO Interface Configuration:")
        configs = dgi.get_interface_config(DgiInterface.GPIO)
        for (conf_id, conf_value) in configs:
            print(f"GPIO Interface - Config ID: {conf_id} Config value: {conf_value}")

        print("")
        print("Timestamp Interface Configuration:")
        configs = dgi.get_interface_config(DgiInterface.TIMESTAMP)
        for (conf_id, conf_value) in configs:
            print(f"Timestamp Interface - Config ID: {conf_id} Config value: {conf_value}")

        dgi.sign_off()
    except UsbError as exc:
        print("USB error")
        print(exc)
    except DgiProtocolError as exc:
        print("DGI protocol error")
        print(exc)
