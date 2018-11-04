import asyncio
from aiogopro import Camera, constants
camera = Camera()


async def run():
    print(await camera.connect())
    # print('status:', await camera.getStatus())
    print('internal_battery_level:', await camera.getStatus(constants.Status.system.internal_battery_level))
    print('date_time:', await camera.timeGet())
    print('keepAlive:', await camera.keepAlive())

    await asyncio.sleep(60 * 15)
    print('internal_battery_level:', await camera.getStatus(constants.Status.system.internal_battery_level))
    await camera.quit()


asyncio.get_event_loop().run_until_complete(run())
print("Done")
