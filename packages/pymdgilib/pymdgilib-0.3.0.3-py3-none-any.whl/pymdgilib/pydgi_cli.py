"""
pymdgilib CLI: "pydgi"
"""
import sys
import os
import logging
from time import sleep, time
from logging.config import dictConfig
import argparse
from appdirs import user_log_dir

try:
    # When Python 3.11 becomes the minimum supported version for this tool
    # we can remove the tomli fallback solution here since this version
    # will have tomllib in its standard library.
    import tomllib as toml_reader
except ModuleNotFoundError:
    import tomli as toml_reader #pylint: disable=import-error
from pymdgilib.dgidevice import UsbError, get_usb_backend
from pymdgilib.dgi import Dgi, DgiInterface, DgiInterfaceState, DgiGpioConfig, DgiProtocolError

try:
    from . import __version__ as VERSION
    from . import BUILD_DATE, COMMIT_ID
except ImportError:
    print("Version info not found!")
    VERSION = "0.0.0"
    COMMIT_ID = "N/A"
    BUILD_DATE = "N/A"

class DeviceNotFoundError(Exception):
    """Device not found exception"""

def setup_logging(user_requested_level=logging.WARNING, default_path='logging.toml',
                  env_key='MICROCHIP_PYTHONTOOLS_CONFIG'):
    """
    Setup logging configuration for this CLI
    """
    # Logging config TOML file can be specified via environment variable
    value = os.getenv(env_key, None)
    if value:
        path = value
    else:
        # Otherwise use the one shipped with this application
        path = os.path.join(os.path.dirname(__file__), default_path)
    # Load the TOML if possible
    if os.path.exists(path):
        try:
            with open(path, 'rb') as file:
                # Load logging configfile from toml
                configfile = toml_reader.load(file)
                # File logging goes to user log directory under Microchip/modulename
                logdir = user_log_dir(__name__, "Microchip")
                # Look through all handlers, and prepend log directory to redirect all file loggers
                num_file_handlers = 0
                for handler in configfile['handlers'].keys():
                    # A filename key
                    if 'filename' in configfile['handlers'][handler].keys():
                        configfile['handlers'][handler]['filename'] = os.path.join(
                            logdir, configfile['handlers'][handler]['filename'])
                        num_file_handlers += 1
                if num_file_handlers > 0:
                    # Create it if it does not exist
                    os.makedirs(logdir, exist_ok=True)

                if user_requested_level <= logging.DEBUG:
                    # Using a different handler for DEBUG level logging to be able to have a more detailed formatter
                    configfile['root']['handlers'].append('console_detailed')
                    # Remove the original console handlers
                    try:
                        configfile['root']['handlers'].remove('console_only_info')
                    except ValueError:
                        # The TOML file might have been customized and the console_only_info handler might
                        # already have been removed
                        pass
                    try:
                        configfile['root']['handlers'].remove('console_not_info')
                    except ValueError:
                        # The TOML file might have been customized and the console_only_info handler might
                        # already have been removed
                        pass
                else:
                    # Console logging takes granularity argument from CLI user
                    configfile['handlers']['console_only_info']['level'] = user_requested_level
                    configfile['handlers']['console_not_info']['level'] = user_requested_level

                # Root logger must be the most verbose of the ALL TOML configurations and the CLI user argument
                most_verbose_logging = min(user_requested_level, getattr(logging, configfile['root']['level']))
                for handler in configfile['handlers'].keys():
                    # A filename key
                    if 'filename' in configfile['handlers'][handler].keys():
                        level = getattr(logging, configfile['handlers'][handler]['level'])
                        most_verbose_logging = min(most_verbose_logging, level)
                configfile['root']['level'] = most_verbose_logging
            dictConfig(configfile)
            return
        except (toml_reader.TOMLDecodeError, TypeError):
            # Error while parsing TOML config file
            print(f"Error parsing logging config file '{path}'")
        except KeyError as keyerror:
            # Error looking for custom fields in TOML
            print(f"Key {keyerror} not found in logging config file")
    else:
        # Config specified by environment variable not found
        print(f"Unable to open logging config file '{path}'")

    # If all else fails, revert to basic logging at specified level for this application
    print("Reverting to basic logging.")
    logging.basicConfig(level=user_requested_level)

def print_version_and_release(args):
    """Print version and/or release information

    :param args: CLI arguments
    :type args: Namespace
    """
    print(f"pydgi version {VERSION}")
    if args.release_info:
        print(f"Build date:  {BUILD_DATE}")
        print(f"Commit ID:   {COMMIT_ID}")
        print(f"Installed in {os.path.abspath(os.path.dirname(__file__))}")

def dgi_init(serial_number=None):
    """Initialize USB backend and DGI.

    :param serial_number: USB serial number of DGI device, optional 
    :type serial_number: str
    :raises DeviceNotFoundError: If no device or too many devices are found
    :return: DGI instance
    :rtype: Dgi
    """
    backend = get_usb_backend()
    devices = backend.find_dgi_devices(serialnumber=serial_number)
    if 1 < len(devices):
        print("More than one DGI interface found. Please specify interface by providing serial number")
        raise DeviceNotFoundError()
    if 0 == len(devices):
        print("No DGI interface found.")
        raise DeviceNotFoundError()
    backend.open(devices[0])
    dgi = Dgi(backend)

    dgi.sign_on()
    dgi.set_mode(2, False)
    return dgi

def dgi_exit(dgi: Dgi):
    """Close DGI and USB backend

    :param dgi: DGI instance
    :type dgi: Dgi
    """
    dgi.sign_off()
    dgi.dev.close()

def gpio_read(args):
    """Poll DGI GPIO status 

    :param args: Namespace with members
        - pins: Bitmask to select GPIO pins
        - sampling_time: defines how long GPIO pins are sampled
        - serial: DGI device serial number as string or None
    :type args: Namespace
    """
    dgi = dgi_init(args.serial)
    # In order to use the GPIO interface the timestamp interface must be on
    dgi.set_interface_state(DgiInterface.TIMESTAMP, DgiInterfaceState.ON)
    dgi.set_interface_state(DgiInterface.GPIO, DgiInterfaceState.ON_TIMESTAMPED)

    # Set pins as input
    configs = [(DgiGpioConfig.INPUT_PINS.value, args.pins)]

    dgi.set_interface_config(DgiInterface.GPIO, configs)

    end_time = time() + args.sampling_time
    while time() < end_time:
        data, _ = dgi.poll_interface_data(DgiInterface.TIMESTAMP)
        samples = dgi.decode_timestamp_data(data)
        for sample in samples:
            if sample["interface"] == DgiInterface.GPIO:
                print(f"DGI GPIO status: {sample['data']} @{sample['timestamp']}")
    dgi_exit(dgi)

def gpio_write(args):
    """Set GPIO pins for a defined duration

    :param args: Namespace with members
        - pins: bitmask to select GPIO pins
        - value: bitmask for pin values
        - assertion_time: guaranteed time the pins are asserted
        - serial: DGI device serial number as string or None
    :type args: Namespace
    """
    dgi = dgi_init(args.serial)
    # In order to use the GPIO interface the timestamp interface must be on
    dgi.set_interface_state(DgiInterface.TIMESTAMP, DgiInterfaceState.ON)
    dgi.set_interface_state(DgiInterface.GPIO, DgiInterfaceState.ON_TIMESTAMPED)

    # set pins. Not sure if this sequence works might need to first set as output and then send a value
    dgi.send_interface_data(DgiInterface.GPIO, bytes([args.value]))
    # Set pins as output
    configs = [(DgiGpioConfig.OUTPUT_PINS.value, args.pins)]
    dgi.set_interface_config(DgiInterface.GPIO, configs)

    sleep(args.assertion_time)
    dgi_exit(dgi)

def reset(args):
    """Reset target device through DGI

    :param args: Namespace with members
        - assertion_time: guaranteed time the reset is asserted
        - serial: DGI device serial number as string or None
    :type args: Namespace
    """
    dgi = dgi_init(args.serial)
    print("Note this is not implemented in current DGI firmware on nEDBG but other tools should work")
    print(f"Target reset with assertion duration of {args.assertion_time}")
    dgi.target_reset(True)
    sleep(args.assertion_time)
    dgi.target_reset(False)

    dgi_exit(dgi)

def convert_to_int(s):
    """Convert a string to an integer

    :param s: String in one of the following formats
        - Decimal value that can be converted directly by int() e.g. 10
        - Hexadecimal value, must be prefixed with 0x e.g. 0xaabc
        - Binary value, must be prefixed with 0b e.g. 0b110110
    :type s: str
    :return: Integer value
    :rtype: int
    """
    if s.startswith("0x"):
        return int(s, 16)
    if s.startswith("0b"):
        return int(s, 2)
    return int(s, 10)

def main():
    """
    Entrypoint for installable CLI

    Configures the CLI and parses the arguments
    """
    common_argument_parser = argparse.ArgumentParser(add_help=False)
    common_argument_parser.add_argument("-v", "--verbose",
                                        default="info",
                                        choices=['debug', 'info', 'warning', 'error', 'critical'])
    # Action-less switches.  These are all "do X and exit"
    common_argument_parser.add_argument("-V", "--version", action="store_true")
    common_argument_parser.add_argument("-R", "--release-info", action="store_true")
    common_argument_parser.add_argument("-S", "--serial", type=str, default=None)

    parser = argparse.ArgumentParser(parents=[common_argument_parser])
    subparsers = parser.add_subparsers(title='actions', dest='action',
                        # This makes the action argument optional
                        # only if -V/--version or -R/release_info argument is given
                        required=False if "-V" in sys.argv or "--version" in sys.argv \
                        or "-R"  in sys.argv or "--release-info" in sys.argv else True,)

    gpio_parser = subparsers.add_parser(name='gpio')
    gpio_subparsers = gpio_parser.add_subparsers(title='GPIO action', dest='gpio_action', required=True)
    gpio_write_parser = gpio_subparsers.add_parser(name='write')
    gpio_write_parser.set_defaults(func=gpio_write)
    gpio_write_parser.add_argument("-p", "--pins", type=int)
    gpio_write_parser.add_argument("-v", "--value", type=int)
    gpio_write_parser.add_argument("-a", "--assertion-time", type=float, default=0.5)

    gpio_read_parser = gpio_subparsers.add_parser(name="read")
    gpio_read_parser.set_defaults(func=gpio_read)
    gpio_read_parser.add_argument("-s", "--sampling-time", type=float, default=0.5)
    gpio_read_parser.add_argument("-p", "--pins", type=convert_to_int)

    reset_parser = subparsers.add_parser(name='reset')
    reset_parser.add_argument("-a", "--assertion-time", type=float, default=0.5)
    reset_parser.set_defaults(func=reset)

    args = parser.parse_args()
    # Setup logging
    setup_logging(user_requested_level=getattr(logging, args.verbose.upper()))
    logger = logging.getLogger("pymdgilib")
    logger.debug(args)

    if args.version or args.release_info:
        print_version_and_release(args)
        return 0
    try:
        # Call the command handler
        return args.func(args)
    except DeviceNotFoundError as exc:
        print(exc)
        return -1
    except UsbError as exc:
        print("USB transport error")
        print(exc)
        return -1
    except DgiProtocolError as exc:
        print("DGI protocol error")
        print(exc)
        return -1

if __name__ == "__main__":
    sys.exit(main())
