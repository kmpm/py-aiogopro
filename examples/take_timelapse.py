import asyncio
from aiogopro import Camera

from aiogopro.constants import MultiShotSettings, Mode, SubMode

camera = Camera()
TIMER = 10


async def run():
    print('connecting')
    print(await camera.connect())
    print('mode=', await camera.mode(Mode.MULTI_SHOT, SubMode.MultiShot.TIME_LAPSE_PHOTO))
    print('set_setting=', await camera.set_setting(
        MultiShotSettings.Section.TIMELAPSE_RATE,
        MultiShotSettings.TimelapseRate.RATE_1_PHOTO_IN_0_5_SEC
    ))

    print(f'capture for {TIMER} seconds')
    print('capture=', await camera.capture(TIMER))

    print('avaliable', await camera.ensureAvailable())
    files = await camera.list_media()
    print('list_media=', [x.path for x in files])

    await camera.quit()

asyncio.get_event_loop().run_until_complete(run())
print("Done")
