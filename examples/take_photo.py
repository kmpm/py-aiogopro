import asyncio
from aiogopro import Camera, constants

camera = Camera()


async def run():
    print('connecting')
    print(await camera.connect())
    print('snap a photo')

    path = await camera.take_photo()
    print('take_photo', path)

    print('download_media', await camera.dowload_media(path))

    await camera.quit()

asyncio.get_event_loop().run_until_complete(run())
print("Done")
