import asyncio
import platform
import sys

from bleak import BleakClient
from bleak.uuids import normalize_uuid_16, uuid16_dict

# Change this to match the mac address of your device
ADDRESS = (
    "xx:xx:xx:xx:xx:xx"
)

uuid16_lookup = {v: normalize_uuid_16(k) for k, v in uuid16_dict.items()}

FIRMWARE_REV_UUID = "3CE0C366-691F-43E6-B625-3F0912FF6EA7"
IO_DATA_CHAR_UUID = "5F5F9010-0E0D-4BD4-B5DC-E4FF47A45984"

# Probe data
PROBE_UUID = ["0A990C1F-B61A-441C-8F7D-F775B6FF9400",
"F7C21D1C-5CB9-4B9B-AB7E-E1D8E7A51724",
"CFACB2D0-2D81-4C82-A168-13314E38A338",
"C99C943F-DA4B-4EE3-92EC-C806006E9E7F"]


async def main(address):
    async with BleakClient(address, winrt=dict(use_cached_services=True)) as client:
        print(f"Connected: {client.is_connected}")

        try:
            device_name = await client.read_gatt_char(DEVICE_NAME_UUID)
            print("Device Name: {0}".format("".join(map(chr, device_name))))
        except Exception:
            pass

        firmware_data = await client.read_gatt_char(FIRMWARE_REV_UUID)
        print("Firmware Revision: {0}".format("".join(map(chr, firmware_data))))

        async def notification_handler(characteristic, data):
            print(f"{characteristic.description}: {data}")

	# Get probe data
        for p in range(4):
            probe_data = (await client.read_gatt_char(PROBE_UUID[p])).split(b",")
            print("Probe-" + str(p+1) + " High Alarm : " + str(int(probe_data[0])))
            print("Probe-" + str(p+1) + " Low Alarm  : " + str(int(probe_data[1])))
            print("Probe-" + str(p+1) + " Ch Name    : " + str(probe_data[3]))
            print("")
            
        temp_data = (await client.read_gatt_char(IO_DATA_CHAR_UUID)).split(b",")

        for p in range(4):
             probe = p * 7

             print("Probe-" + str(p+1) + " Temp  : " + str(float(temp_data[probe])))
             print("Probe-" + str(p+1) + " Max   : " + str(float(temp_data[probe+2])))
             print("Probe-" + str(p+1) + " Min   : " + str(float(temp_data[probe+4])))
             print("Probe-" + str(p+1) + " State : " + str(float(temp_data[probe+1])))
             print("")

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else ADDRESS))

