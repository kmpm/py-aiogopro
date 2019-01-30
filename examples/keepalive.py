import asyncio
from datetime import datetime

from aiogopro import Camera, constants


MINUTES = 15
SLEEP_TIME = 60 * MINUTES
camera = Camera()


async def run():
    print(await camera.connect())
    # print('status:', await camera.getStatus())
    print('internal_battery_level:', await camera.getStatus(constants.Status.system.internal_battery_level))
    print('date_time:', await camera.timeGet())
    print('keepAlive:', await camera.keepAlive())

    print(f'Will now sleep for {MINUTES} minutes. {datetime.now()}')
    await asyncio.sleep(SLEEP_TIME)
    print(f'Back now. {datetime.now()}')
    print('internal_battery_level:', await camera.getStatus(constants.Status.system.internal_battery_level))
    await camera.quit()


asyncio.get_event_loop().run_until_complete(run())
print("Done")
