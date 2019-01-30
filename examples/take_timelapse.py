import asyncio
from aiogopro import Camera

from aiogopro.constants import MultiShot

camera = Camera()
TIMER = 10


async def run():
    print('connecting')
    print(await camera.connect())
    print('snap a photo')

    print('setting', await camera.set_setting(MultiShot.TIMELAPSERATE, MultiShot.TimelapseRate.rate_1_photo_in_0_5_sec))

    print('capture', await camera.capture(6))

    print('avaliable', await camera.ensureAvailable())

    path = await camera.get_last_media()
    print('download_media', await camera.dowload_media(path))

    await camera.quit()

asyncio.get_event_loop().run_until_complete(run())
print("Done")
