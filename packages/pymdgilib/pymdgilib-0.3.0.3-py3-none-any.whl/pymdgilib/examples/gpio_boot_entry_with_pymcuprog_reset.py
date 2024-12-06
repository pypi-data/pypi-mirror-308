"""DGI GPIO example"""
import subprocess
import sys
from pymdgilib.dgidevice import UsbError, get_usb_backend
from pymdgilib.dgi import Dgi, DgiInterface, DgiInterfaceState, DgiGpioConfig, DgiProtocolError


DEVICE_SERIALNUMBER = "MCHP3280042700000498" #None

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
            print("Enable bootloader entry pin")
            # Enable DGI GPIO0 output
            configs = [(DgiGpioConfig.OUTPUT_PINS.value, 0x01)]
            dgi.set_interface_config(DgiInterface.GPIO, configs)

            # Drive DGI GPIO0 (bootloader entry condition) low
            dgi.send_interface_data(DgiInterface.GPIO, bytes([0x08]))
            # Do a target reset
            print("Target reset")
            cmd = ['pymcuprog', 'reset']
            if DEVICE_SERIALNUMBER is not None:
                cmd.append("--serialnumber")
                cmd.append(DEVICE_SERIALNUMBER)
            try:
                output = subprocess.run(cmd, capture_output=True, check=True)
            except subprocess.CalledProcessError as exc:
                print(exc)
                dgi.sign_off()
                sys.exit(exc.returncode)

            print("Disable bootloader entry pin")
            # Disable DGI GPIO interface (should go into high impedance state)
            dgi.set_interface_state(DgiInterface.GPIO, DgiInterfaceState.OFF)
        dgi.sign_off()
    except UsbError as exc:
        print("USB error")
        print(exc)
    except DgiProtocolError as exc:
        print("DGI protocol error")
        print(exc)
