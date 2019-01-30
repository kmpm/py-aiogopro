import asyncio
from aiogopro import Camera, constants
camera = Camera()


async def run():
    print('connecting')
    print(await camera.connect())

    print('internal_battery_level:', await camera.get_status(constants.Status.System.internal_battery_level))
    print('ap_ssid:', await camera.get_status(constants.Status.Wireless.ap_ssid))
    print('date_time:', await camera.timeGet())
    print('time sync:', await camera.timeSync())
    await asyncio.sleep(1)
    print('date_time:', await camera.timeGet())
    await camera.quit()

asyncio.get_event_loop().run_until_complete(run())
print("Done")
