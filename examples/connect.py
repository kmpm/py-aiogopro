import asyncio
from aiogopro import Camera, constants, parse_datetime
from datetime import datetime
camera = Camera()


async def run():
    print(await camera.connect())
    # print('status:', await camera.getStatus())
    print('internal_battery_level:', await camera.getStatus(constants.Status.system.internal_battery_level))
    print('ap_ssid:', await camera.getStatus(constants.Status.wireless.ap_ssid))
    print('date_time:', await camera.timeGet())
    print('time sync:', await camera.timeSync())
    await asyncio.sleep(1)
    print('date_time:', await camera.timeGet())

    # print('shutter', await camera.command(constants.Command.GPCAMERA_SHUTTER, 1))
    # await asyncio.sleep(2)
    # print('shutter', await camera.command(constants.Command.GPCAMERA_SHUTTER, 0))
    await camera.quit()

asyncio.get_event_loop().run_until_complete(run())
print("Done")
