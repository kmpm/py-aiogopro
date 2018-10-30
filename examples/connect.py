import asyncio
from aiogopro import Camera, constants, parse_datetime

camera = Camera()


async def run():
    print(await camera.connect())
    # print('status:', await camera.getStatus())
    print('internal_battery_level:', await camera.getStatus(constants.Status.system.internal_battery_level))
    print('ap_ssid:', await camera.getStatus(constants.Status.wireless.ap_ssid))
    dtm = await camera.getStatus(constants.Status.setup.date_time)
    print('date_time:', dtm, parse_datetime(dtm))
    print('shutter', await camera.gpControlCommand(constants.Command.GPCAMERA_SHUTTER, 1))
    await asyncio.sleep(2)
    print('shutter', await camera.gpControlCommand(constants.Command.GPCAMERA_SHUTTER, 0))
    await camera.quit()

asyncio.get_event_loop().run_until_complete(run())
print("Done")
