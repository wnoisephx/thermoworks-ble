import asyncio
import platform
import sys

from bleak import BleakClient
from bleak.uuids import normalize_uuid_16, uuid16_dict

# change this to match your device
ADDRESS = (
    "xx:xx:xx:xx:xx:xx"
)

uuid16_lookup = {v: normalize_uuid_16(k) for k, v in uuid16_dict.items()}

#SYSTEM_ID_UUID = uuid16_lookup["System ID"]
MODEL_NBR_UUID = uuid16_lookup["Model Number String"]
DEVICE_NAME_UUID = uuid16_lookup["Device Name"]
IO_DATA_CHAR_UUID = "783F2991-23E0-4BDC-AC16-78601BD84B39"


async def main(address):
    async with BleakClient(address, winrt=dict(use_cached_services=True)) as client:
        print(f"Connected: {client.is_connected}")

        try:
            device_name = await client.read_gatt_char(DEVICE_NAME_UUID)
            print("Device Name: {0}".format("".join(map(chr, device_name))))
        except Exception:
            pass

        async def notification_handler(characteristic, data):
            print(f"{characteristic.description}: {data}")

	# Get the Data
        temp_data = await client.read_gatt_char(IO_DATA_CHAR_UUID)
        print("Temp Data: {0}".format(":".join(format(x, '02x') for x in temp_data)))

        ProbeStatus = temp_data[0]
        Temperature = temp_data[1]
        AlarmTemp = temp_data[5]
        MACAddress = temp_data[13:19]
        
        print("Probe Status : " + hex(ProbeStatus))
        print("Temperature  : " + str(int(Temperature)))
        print("Alarm Temperature  : " + str(int(AlarmTemp)))
        print("MACAddress : {0}".format(":".join(format(x, '02x') for x in  MACAddress)))

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else ADDRESS))

