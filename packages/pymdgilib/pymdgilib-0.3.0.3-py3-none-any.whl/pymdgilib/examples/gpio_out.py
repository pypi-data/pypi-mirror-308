"""DGI GPIO example

Toggles DGI GPIO0 pin 10 times with a frequency of 2 Hz. Starts with setting pin low.
"""
import sys
from time import sleep
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

        dgi.sign_on()
        dgi.set_mode(2, False)
        interfaces = dgi.list_interfaces()

        if DgiInterface.GPIO in interfaces:
            # In order to use the GPIO interface the timestamp interface must be on
            dgi.set_interface_state(DgiInterface.TIMESTAMP, DgiInterfaceState.ON)
            dgi.set_interface_state(DgiInterface.GPIO, DgiInterfaceState.ON_TIMESTAMPED)

            # Enable DGI GPIO0 as output
            configs = [(DgiGpioConfig.OUTPUT_PINS.value, 0x01)]
            dgi.set_interface_config(DgiInterface.GPIO, configs)

            for i in range(5):
                # Drive DGI GPIO0 low
                dgi.send_interface_data(DgiInterface.GPIO, bytes([0x00]))
                sleep(0.5)
                # Drive DGI GPIO0 high
                dgi.send_interface_data(DgiInterface.GPIO, bytes([0x01]))
                sleep(0.5)

            # Disable DGI GPIO interface (should go into high impedance state)
            dgi.set_interface_state(DgiInterface.GPIO, DgiInterfaceState.OFF)
        dgi.sign_off()
    except UsbError as exc:
        print("USB error")
        print(exc)
    except DgiProtocolError as exc:
        print("DGI protocol error")
        print(exc)
