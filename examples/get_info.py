import asyncio
import json
from aiogopro import Camera, constants
camera = Camera()


async def run():
    print('connecting')
    print(await camera.connect())

    print('info', json.dumps((await camera.get_info()).__dict__))

    print('status', await camera.get_status())
    await camera.quit()

asyncio.get_event_loop().run_until_complete(run())
print("Done")
