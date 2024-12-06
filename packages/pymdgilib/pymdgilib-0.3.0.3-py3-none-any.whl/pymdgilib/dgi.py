""" Microchip Data Gateway Interface
"""
from enum import Enum
from typing import Union
from pymdgilib.dgidevice import UsbBackend

class DgiProtocolError(Exception):
    """DGI protocol error exception"""

class DgiCommands(Enum):
    """DGI command codes
    """
    SIGN_ON = 0
    SIGN_OFF = 1
    GET_VERSION = 2
    SET_MODE = 0x0A
    TARGET_RESET = 0x20
    INTERFACES_LIST = 0x08
    INTERFACES_SET_STATE = 0x10
    INTERFACES_GET_STATUS = 0x11
    INTERFACES_SET_CONFIG = 0x12
    INTERFACES_GET_CONFIG = 0x13
    INTERFACES_POLL_DATA = 0x15
    INTERFACES_SEND_DATA = 0x14

class DgiResponseStatus(Enum):
    """DGI response codes
    """
    OK = 0x80
    FAIL = 0x99
    DATA = 0xA0
    UNKNOWN = 0xFF

class DgiInterfaceState(Enum):
    """DGI interface states"""
    OFF = 0
    ON = 1
    ON_TIMESTAMPED = 2

class DgiInterface(Enum):
    """DGI interface identifiers"""
    TIMESTAMP = 0
    SPI = 0x20
    USART = 0x21
    I2C = 0x22
    GPIO = 0x30
    POWER_DATA = 0x40
    POWER_EVENT = 0x41
    DEBUG = 0x50
    PRINT = 0x51
    RESERVED = 0xff

class DgiGpioConfig(Enum):
    """DGI GPIO configuration IDS"""
    INPUT_PINS = 0
    OUTPUT_PINS = 1

class DgiInterfaceStatus(): #pylint: disable=too-few-public-methods
    """DGI interface status"""
    DGI_IFACE_STATUS_STARTED = 0x01
    DGI_IFACE_STATUS_TIMESTAMPED = 0x02
    DGI_IFACE_STATUS_OVERFLOW = 0x04

    def __init__(self, interface: DgiInterface, status: int):
        self.interface = interface
        self.started = bool(self.DGI_IFACE_STATUS_STARTED & status)
        self.timestamped = bool(self.DGI_IFACE_STATUS_TIMESTAMPED)
        self.overflow = bool(self.DGI_IFACE_STATUS_OVERFLOW)

    def __str__(self):
        return \
f"{self.interface.name} interface status: started={self.started} \
timestamped={self.timestamped} overflow={self.overflow} "

class Dgi:
    """Data Gateway Interface
    """
    MAX_COMMAND_SIZE = 256
    def __init__(self, dev: UsbBackend):
        self.dev = dev
        self.poll_response_length = 2
        self.overflow_indicator = False

    def send_cmd(self, cmd):
        """
        Sends a DGI command to the device and read the response.

        :param cmd: The command to send to the device.
        :type cmd: Bytes or bytearray
        :raises DgiProtocolError: If the command in the response does not match the sent command.
        :raises AssertionError: If the command length exceeds the maximum allowed size.
        :return: The response data from the device.
        :rtype: bytearray
        """
        assert len(cmd) <= self.MAX_COMMAND_SIZE
        response_data = bytearray()
        self.dev.write(cmd)
        response_chunk = self.dev.read(self.dev.usb_packet_size)
        response_data.extend(response_chunk)

        # Check if the command in the response matches the sent command
        if cmd[0] != response_data[0]:
            raise DgiProtocolError("Command in response is not the same as in the command")

        # Continue reading until the response is fully received
        while len(response_chunk) == self.dev.usb_packet_size:
            response_chunk = self.dev.read(self.dev.usb_packet_size)
            response_data.extend(response_chunk)

        return response_data

    def sign_on(self):
        """
        Sign on to the device and retrieve the interface description.

        This function sends a SIGN_ON command to the device and expects a response
        containing the interface description. If the response status is not DATA,
        a DgiProtocolError is raised.

        :returns: The interface description as a UTF-8 encoded string.
        :rtype: str

        :raises DgiProtocolError: If the response status is not DATA.
        """
        cmd = bytes([DgiCommands.SIGN_ON.value, 0x00, 0x00])
        response = self.send_cmd(cmd)

        if DgiResponseStatus.DATA.value != response[1]:
            raise DgiProtocolError()
        length = int.from_bytes(response[2:4], byteorder="big")

        interface_description = response[4:4 + length].decode(encoding="utf-8")
        return interface_description

    def sign_off(self):
        """
        Sign off from the device.

        This function sends a SIGN_OFF command to the device. If the response status
        is not OK, a DgiProtocolError is raised.

        :raises DgiProtocolError: If the response status is not OK.
        """
        cmd = bytes([DgiCommands.SIGN_OFF.value, 0x00, 0x00])
        response = self.send_cmd(cmd)

        if DgiResponseStatus.OK.value != response[1]:
            raise DgiProtocolError()

    def get_version(self):
        """
        Get DGI version.

        This function sends a GET_VERSION command to the device and expects a response
        containing the major and minor version numbers. If the response status is not DATA,
        a DgiProtocolError is raised.

        :returns: A tuple containing the major and minor version numbers.
        :rtype: tuple

        :raises DgiProtocolError: If the response status is not DATA.
        """
        cmd = bytes([DgiCommands.GET_VERSION.value, 0x00, 0x00])
        response = self.send_cmd(cmd)

        if DgiResponseStatus.DATA.value != response[1]:
            raise DgiProtocolError()
        major = response[2]
        minor = response[3]
        return major, minor

    def set_mode(self, poll_response_length=2, overflow_indicator=False):
        """
        Set the mode of the data gateway interface.

        This function configures the DGI mode by sending a SET_MODE command. The mode
        is determined by the poll_response_length and overflow_indicator parameters. If the
        response status is not OK, a DgiProtocolError is raised.

        :param poll_response_length: The length of the poll response, either 2 or 4 bytes (default is 2).
        :type poll_response_length: int, optional
        :param overflow_indicator: Whether to enable the overflow indicator (default is False).
        :type overflow_indicator: bool, optional

        :raises AssertionError: If poll_response_length is not 2 or 4.
        :raises DgiProtocolError: If the response status is not OK.
        """
        assert(poll_response_length in [2, 4])
        mode = 0
        mode |= 1 if overflow_indicator else 0
        mode |= (1 << 1) if poll_response_length == 4 else 0

        cmd = bytes([DgiCommands.SET_MODE.value])\
                    + int(1).to_bytes(2, byteorder="big")\
                    + bytes([mode])
        response = self.send_cmd(cmd)

        if DgiResponseStatus.OK.value != response[1]:
            raise DgiProtocolError()
        self.poll_response_length = poll_response_length
        self.overflow_indicator = overflow_indicator

    def target_reset(self, active):
        """Set target reset

        :param active: State of the target reset
        :type active: bool, True will pull the target reset low and False will release the reset,
                      basically go into high impdance state and let any external pull up drive reset
                      signal back up to deassert voltage.
        :raises DgiProtocolError: When response for this command is not as expected.
        """
        assert isinstance(active, bool)
        reset_state = 1 if active else 0
        cmd = bytes([DgiCommands.TARGET_RESET.value])\
                + int(1).to_bytes(2, byteorder="big")\
                + bytes([reset_state])
        response = self.send_cmd(cmd)
        if DgiResponseStatus.OK.value != response[1]:
            raise DgiProtocolError()

    def list_interfaces(self) -> list[DgiInterface]:
        """List DGI interfaces

        :return: List of interface IDs
        :rtype: list(int)
        :raises DgiProtocolError: When response for this command is not as expected.
        """
        cmd = bytes([DgiCommands.INTERFACES_LIST.value]) + int(0).to_bytes(2, byteorder="big")
        response = self.send_cmd(cmd)
        if DgiResponseStatus.DATA.value != response[1]:
            raise DgiProtocolError()
        interface_count = response[2]
        interfaces = []
        for i in range(interface_count):
            interfaces.append(DgiInterface(response[3 + i]))
        return interfaces

    def set_interfaces_state(self, interfaces: list[tuple[DgiInterface, DgiInterfaceState]]):
        """Enable/disable interfaces

        :param interfaces: Interfaces to configure
        :type interfaces: list(tuple(int, DgiInterfaceState)), list of (interface id, state) tuples
        :raises DgiProtocolError: Upon unexpected command response
        """
        # Two bytes per interface, 1 byte interface ID and one byte interface state
        length = len(interfaces) * 2
        cmd = bytes([DgiCommands.INTERFACES_SET_STATE.value]) + length.to_bytes(2, byteorder="big")
        for interface_id, interface_state in interfaces:
            cmd += bytes([interface_id.value, interface_state.value])
        response = self.send_cmd(cmd)
        if DgiResponseStatus.OK.value != response[1]:
            raise DgiProtocolError("Failed to execute set interface state command.")

    def set_interface_state(self, interface: DgiInterface, state: DgiInterfaceState):
        """Enable/disable a interface

        :param interface: Interface ID
        :type interface: int
        :param state: Desired interface state
        :type state: DgiInterfaceState
        :raises DgiProtocolError: Upon unexpected command response
        """
        self.set_interfaces_state([(interface, state)])

    def get_interfaces_status(self) -> list[DgiInterfaceStatus]:
        """
        Retrieve the status of all interfaces.

        This function sends a command to the device to get the status of all interfaces.
        It parses the response and returns a list of `DgiInterfaceStatus` objects, each
        representing the status of an interface.

        :return: A list of `DgiInterfaceStatus` objects.
        :rtype: List[DgiInterfaceStatus]

        :raises DgiProtocolError: If the response status is not `DgiResponseStatus.DATA`.

        Example usage::

            interfaces_status = device.get_interfaces_status()
            for status in interfaces_status:
                print(f"Interface ID: {status.interface_id}, Status: {status.status}")

        The response is expected to be in the following format:

        - Byte 0: Command byte (already handled internally)
        - Byte 1: Response status (checked against `DgiResponseStatus.DATA`)
        - Byte 2 onwards: Pairs of bytes representing interface ID and status

        The function iterates over the response starting from the third byte, extracting
        interface IDs and their statuses, and appending them to the `interfaces_status` list.
        """
        cmd = bytes([DgiCommands.INTERFACES_GET_STATUS.value]) + int(0).to_bytes(2, byteorder="big")

        response = self.send_cmd(cmd)

        if DgiResponseStatus.DATA.value != response[1]:
            raise DgiProtocolError("Failed to execute get interface status command " +\
                                   f"({DgiResponseStatus(response[1]).name})")
        i = 2
        interfaces_status = []
        while i < len(response):
            interface_id = DgiInterface(response[i])
            status = response[i + 1]
            interfaces_status.append(DgiInterfaceStatus(interface_id, status))
            i += 2
        return interfaces_status

    def set_interface_config(self, interface: DgiInterface, configs: list[int, int]):
        """
        Set the configuration parameters for a specific interface.

        This function sends a command to the device to set configuration parameters
        for a specified interface. Each configuration parameter consists of an ID and
        a value.

        :param interface: The interface for which the configuration is to be set.
        :type interface: DgiInterface
        :param configs: A list of tuples, where each tuple contains a configuration ID and its corresponding value.
        :type configs: List[Tuple[int, int]]

        :raises DgiProtocolError: If the response status is not `DgiResponseStatus.OK`.

        Example usage::

            interface = DgiInterface.GPIO
            configs = [(DgiGpioConfig.INPUT_PINS.value, 0x3)]
            device.set_interface_config(interface, configs)

        The command is constructed as follows:

        - Byte 0: Command byte (`DgiCommands.INTERFACES_SET_CONFIG.value`)
        - Bytes 1-2: Length of the command (1 byte for interface ID + 6 bytes per configuration parameter)
        - Byte 3: Interface ID
        - Bytes 4 onwards: Configuration parameters, each consisting of:
            - 2 bytes for configuration ID
            - 4 bytes for configuration value

        The function sends the command and checks the response status. If the response
        status is not `DgiResponseStatus.OK`, it raises a `DgiProtocolError`.
        """
        # One byte for interface ID, 6 bytes per configuration parameter
        length = 1 + len(configs) * 6
        cmd = bytes([DgiCommands.INTERFACES_SET_CONFIG.value])\
            + length.to_bytes(2, byteorder="big")\
            + bytes([interface.value])
        for (config_id, config_value) in configs:
            cmd += config_id.to_bytes(2, byteorder="big")
            cmd += config_value.to_bytes(4, byteorder="big")

        response = self.send_cmd(cmd)
        if DgiResponseStatus.OK.value != response[1]:
            raise DgiProtocolError()

    def get_interface_config(self, interface: DgiInterface):
        """
        Retrieve the configuration parameters for a specific interface.

        This function sends a command to the device to get the configuration parameters
        for a specified interface. It parses the response and returns a list of tuples,
        each containing a configuration ID and its corresponding value.

        :param interface: The interface for which the configuration is to be retrieved.
        :type interface: DgiInterface
        :return: A list of tuples, where each tuple contains a configuration ID and its corresponding value.
        :rtype: List[Tuple[int, int]]

        :raises DgiProtocolError: If the response status is not `DgiResponseStatus.DATA` or if
            the interface ID in the response does not match the requested interface.

        Example usage::

            interface = DgiInterface.SOME_INTERFACE
            configs = device.get_interface_config(interface)
            for config_id, config_value in configs:
                print(f"Config ID: {config_id}, Config Value: {config_value}")

        The command is constructed as follows:

        - Byte 0: Command byte (`DgiCommands.INTERFACES_GET_CONFIG.value`)
        - Bytes 1-2: Length of the command (1 byte for interface ID)
        - Byte 3: Interface ID

        The response is expected to be in the following format:

        - Byte 0: Command byte (already handled internally)
        - Byte 1: Response status (checked against `DgiResponseStatus.DATA`)
        - Bytes 2-3: Length of the response
        - Byte 4: Interface ID (should match the requested interface)
        - Bytes 5 onwards: Configuration parameters, each consisting of:
            - 2 bytes for configuration ID
            - 4 bytes for configuration value

        The function sends the command, checks the response status, and verifies the interface ID.
        It then parses the response to extract configuration parameters and returns them as a list of tuples.
        """
        cmd = bytes([DgiCommands.INTERFACES_GET_CONFIG.value])\
            + int(1).to_bytes(2, byteorder="big")\
            + bytes([interface.value])
        response = self.send_cmd(cmd)
        if DgiResponseStatus.DATA.value != response[1]:
            raise DgiProtocolError("Failed to execute get interface configuration" +\
                                   f"({DgiResponseStatus(response[1]).name})")
        length = int.from_bytes(response[2:4], byteorder="big")

        # NOTE: The interface ID is not documented in the DGI user guide
        interface_id = response[4]
        if interface.value != interface_id:
            raise DgiProtocolError("Failed to execute get interface configuration." +\
                                f"Invalid interface ID returned expected {hex(interface.value)}" +\
                                f"but got {hex(interface_id)}")
        i = 5 # Configuration sections start at byte index 5
        configs = []
        while i < length:
            config_id = int.from_bytes(response[i:i + 2], byteorder="big")
            i += 2
            config_value = int.from_bytes(response[i:i + 4], byteorder="big")
            i += 4
            configs.append((config_id, config_value))
        return configs

    def send_interface_data(self, interface: DgiInterface, data: Union[bytes, bytearray]):
        """
        Send data to a specific interface.

        This function sends a command to the device to transmit data to a specified interface.

        :param interface: The interface to which the data is to be sent.
        :type interface: DgiInterface
        :param data: The data to be sent to the interface.
        :type data: bytes or bytearray

        :raises DgiProtocolError: If the response status is not `DgiResponseStatus.OK`.

        The function sends the command and checks the response status. If the response
        status is not `DgiResponseStatus.OK`, it raises a `DgiProtocolError`.
        """
        # The command is constructed as follows:
        # - Byte 0: Command byte (`DgiCommands.INTERFACES_SEND_DATA.value`)
        # - Bytes 1-2: Length of the command (1 byte for interface ID + length of data)
        # - Byte 3: Interface ID
        # - Bytes 4 onwards: Data to be sent
        cmd = bytes([DgiCommands.INTERFACES_SEND_DATA.value])\
            + int(1 + len(data)).to_bytes(2, byteorder="big")\
            + bytes([interface.value])\
            + data

        response = self.send_cmd(cmd)

        if DgiResponseStatus.OK.value != response[1]:
            raise DgiProtocolError("Command send interface data failed.")

    def poll_interface_data(self, interface: DgiInterface) -> tuple[bytes, int]:
        """
        Poll data from a specific interface.

        This function sends a command to the device to poll data from a specified interface.
        It parses the response and returns the polled data along with an optional overflow indicator.

        :param interface: The interface from which the data is to be polled.
        :type interface: DgiInterface
        :return: A tuple containing the polled data (bytes) and an optional overflow indicator (int).
        :rtype: Tuple[bytes, int]

        :raises DgiProtocolError: If the response status is not `DgiResponseStatus.DATA` or
        if the interface ID in the response does not match the requested interface.

        The function sends the command, checks the response status, and verifies the interface ID.
        It then parses the response to extract the polled data and an optional overflow indicator.
        """
        # The command is constructed as follows:
        # - Byte 0: Command byte (`DgiCommands.INTERFACES_POLL_DATA.value`)
        # - Bytes 1-2: Length of the command (1 byte for interface ID)
        # - Byte 3: Interface ID
        cmd = bytes([DgiCommands.INTERFACES_POLL_DATA.value])\
            + int(1).to_bytes(2, byteorder="big")\
            + bytes([interface.value])
        response = self.send_cmd(cmd)

        if DgiResponseStatus.DATA.value != response[1]:
            raise DgiProtocolError(f"Invalid response code {response[1]}")

        # The response is expected to be in the following format:
        # - Byte 0: Command byte (already handled internally)
        # - Byte 1: Response status (checked against `DgiResponseStatus.DATA`)
        # - Byte 2: Interface ID (should match the requested interface)
        # - Bytes 3 onwards: Polled data and optional overflow indicator
        # NOTE: The interface ID is not documented in the DGI user guide
        interface_id = response[2]
        if interface.value != interface_id:
            raise DgiProtocolError("Failed to execute get interface configuration." +\
                                f"Invalid interface ID returned expected {hex(interface.value)}" +\
                                f"but got {hex(interface_id)}")

        data_length = int.from_bytes(response[3:3 + self.poll_response_length], byteorder="big")

        overflow = None
        index = 3 + self.poll_response_length
        if self.overflow_indicator:
            overflow_size = 4
            overflow = int.from_bytes(response[index:index + overflow_size], byteorder="big")
            index += overflow_size
        data = response[index:index + data_length]
        return data, overflow

    def decode_timestamp_data(self, data: Union[bytes, bytearray]):
        """
        Decode timestamp data from a byte sequence.

        This function decodes a byte sequence containing timestamp data for various interfaces.
        It returns a list of dictionaries, each representing a sample with its associated interface,
        timestamp, overflow status, and data.

        :param data: The byte sequence containing the timestamp data.
        :type data: bytes or bytearray
        :return: A list of dictionaries, each containing the decoded data for a sample.
        :rtype: List[Dict[DgiInterface, int, bool, int] | Dict[DgiInterface, int]]

        :raises DgiProtocolError: If the interface ID in the data is not recognized.

        Example usage::

            data = bytes([0x00, 0x3e, 0x00, 0x3f, 0x00, 0x40, 0x30, 0x9b, 0x59, 0x00, 0x03])
            samples = device.decode_timestamp_data(data)
            for sample in samples:
                print(f"Interface: {sample['interface']}, Timestamp: {sample.get('timestamp')}, " +
                    f"Overflow: {sample.get('overflow')}, Data: {sample.get('data')}")

        The function iterates over the data, decoding each sample based on the interface ID.
        It supports decoding for GPIO and TIMESTAMP interfaces, and can be extended to support more interfaces.
        """
        samples = []
        index = 0
        while index < len(data):
            interface = DgiInterface(data[index])
            index += 1
            if interface == DgiInterface.GPIO:
                sample = {}
                sample["interface"] = DgiInterface.GPIO
                sample["timestamp"] = int.from_bytes(data[index:index + 2], byteorder="big")
                index += 2
                sample["overflow"] = bool(data[index])
                index += 1
                sample["data"] = data[index]
                index += 1
                samples.append(sample)
            elif interface == DgiInterface.TIMESTAMP:
                sample = {
                    "interface": DgiInterface.TIMESTAMP,
                    "counter": data[index]
                }
                index += 1
                samples.append(sample)
            # TODO: decode more interfaces
        return samples

    def print_interfaces_status(self, status: list[DgiInterfaceStatus]):
        """Print DGI interfaces status

        :param status: Status of DGI interfaces
        :type status: list[DgiInterfaceStatus]
        """
        for stat in status:
            print(f"{stat}")
