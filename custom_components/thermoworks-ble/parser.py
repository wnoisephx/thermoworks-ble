"""Parser for ThermoWork BLE advertisements.

MIT License applies.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from enum import Enum, auto

from bleak import BleakError, BLEDevice
from bleak_retry_connector import (
    BleakClientWithServiceCache,
    establish_connection,
    retry_bluetooth_connection_error,
)
from bluetooth_data_tools import short_address
from bluetooth_sensor_state_data import BluetoothData
from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data import SensorDeviceClass, SensorUpdate, Units
from sensor_state_data.enum import StrEnum

from .const import (
)

_LOGGER = logging.getLogger(__name__)

class ThermoWorksSensor(StrEnum):
    TIME = "time"

class Models(Enum):
    TMW022 = auto()

@dataclass
class ModelDescription:
    device_type: str
    Probes: dict[int, str]

DEVICE_TYPES = {
    Models.Signels: ModelDescription("Signels", 4),
}

THERMOWORKS_MANUFACTURER = 0x6224

class ThermoWorksBluetoothDeviceData(BluetoothData):
    """Data for ThermoWorks BLE sensors."""

    def __init__(self) -> None:
        super().__init__()

    def _start_update(self, service_info: BluetoothServiceInfo) -> None:
        """Update from BLE advertisement data."""
        _LOGGER.debug("Parsing ThermoWorks BLE advertisement data: %s", service_info)
        manufacturer_data = service_info.manufacturer_data
        address = service_info.address
        if THERMOWORKS_MANUFACTURER not in manufacturer_data:
            return None
        data = manufacturer_data[THERMOWORKS_MANUFACTURER]
        self.set_device_manufacturer("ThermoWorks")
        _LOGGER.debug("Parsing ThermoWorks sensor: %s", data)
        msg_length = len(data)

    def poll_needed(
        self, service_info: BluetoothServiceInfo, last_poll: float | None
    ) -> bool:
        """
        This is called every time we get a service_info for a device. It means the
        device is working and online.
        """
        if last_poll is None:
            return True
        return last_poll > update_interval

    @retry_bluetooth_connection_error()
    async def _get_payload(self, client: BleakClientWithServiceCache) -> None:
        """Get the payload from the gatt_characteristics."""
        _LOGGER.debug("Successfully read active gatt characters")

    async def async_poll(self, ble_device: BLEDevice) -> SensorUpdate:
        """
        Poll the device to retrieve any values we can't get from passive listening.
        """
        _LOGGER.debug("Polling ThermoWorks device: %s", ble_device.address)
        client = await establish_connection(
            BleakClientWithServiceCache, ble_device, ble_device.address
        )
        try:
            await self._get_payload(client)
        except BleakError as err:
            _LOGGER.warning(f"Reading gatt characters failed with err: {err}")
        finally:
            await client.disconnect()
            _LOGGER.debug("Disconnected from active bluetooth client")
        return self._finish_update()
