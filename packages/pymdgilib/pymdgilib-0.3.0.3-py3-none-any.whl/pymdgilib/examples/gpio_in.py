"""DGI GPIO example

Monitors DGI GPIO0 and GPIO1 for changes for 5 seconds and prints any changes to stdout
with the DGI timestamp value.

"""
import sys
from time import time, sleep
from pymdgilib.dgidevice import UsbError, get_usb_backend
from pymdgilib.dgi import Dgi, DgiInterface, DgiInterfaceState, DgiGpioConfig, DgiProtocolError

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
        print(f"DGI interface description: {interface_description}")
        major, minor = dgi.get_version()
        print(f"DGI version: {major}.{minor}")

        interfaces = dgi.list_interfaces()
        for interface in interfaces:
            print(f"{interface.name} ({interface.value})")

        dgi.set_mode(2, False)

        if DgiInterface.GPIO in interfaces:
            dgi.set_interface_state(DgiInterface.TIMESTAMP, DgiInterfaceState.ON)
            dgi.set_interface_state(DgiInterface.GPIO, DgiInterfaceState.ON_TIMESTAMPED)

            status = dgi.get_interfaces_status()
            dgi.print_interfaces_status(status)

            configs = [(DgiGpioConfig.INPUT_PINS.value, 0x3)]
            dgi.set_interface_config(DgiInterface.GPIO, configs)

            configs = dgi.get_interface_config(DgiInterface.GPIO)
            for (conf_id, conf_value) in configs:
                print(f"GPIO Interface - Config ID: {conf_id} Config value: {conf_value}")

            configs = dgi.get_interface_config(DgiInterface.TIMESTAMP)
            for (conf_id, conf_value) in configs:
                print(f"Timestamp interface - Config ID: {conf_id} Config value: {conf_value}")

            end_time = time() + 5
            while time() < end_time:
                data, overflow = dgi.poll_interface_data(DgiInterface.TIMESTAMP)
                samples = dgi.decode_timestamp_data(data)
                for sample in samples:
                    if sample["interface"] == DgiInterface.GPIO:
                        print(f"DGI GPIO status: {sample["data"]} @{sample["timestamp"]}")
                sleep(0.5)
        dgi.sign_off()
    except UsbError as exc:
        print("USB error")
        print(exc)
    except DgiProtocolError as exc:
        print("DGI protocol error")
        print(exc)
