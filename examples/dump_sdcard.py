import asyncio

from aiogopro import Camera
camera = Camera()


async def run():
    print('connecting')
    print(await camera.connect())

    print('download_all', await camera.download_all(destination='tmp/'))
    print('delete', await camera.delete("all"))

    await camera.quit()


asyncio.get_event_loop().run_until_complete(run())
print("Done")