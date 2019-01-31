import asyncio
from aiogopro import Camera

from aiogopro.constants import MultiShot, Mode, SubMode

camera = Camera()
TIMER = 10


async def run():
    print('connecting')
    print(await camera.connect())
    print('mode=', await camera.mode(Mode.multi_shot, SubMode.MultiShot.time_lapse_photo))
    print('set_setting=', await camera.set_setting(MultiShot.TIMELAPSERATE, MultiShot.TimelapseRate.rate_1_photo_in_0_5_sec))

    print(f'capture for {TIMER} seconds')
    print('capture=', await camera.capture(TIMER))

    print('avaliable', await camera.ensureAvailable())
    files = await camera.list_media()
    print('list_media=', [x.path for x in files])
    path = await camera.get_last_media()
    print('download_media', await camera.dowload_media(path))

    await camera.quit()

asyncio.get_event_loop().run_until_complete(run())
print("Done")
