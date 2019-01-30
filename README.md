Python async I/O GoPro module
=============================

__Requires Python >= 3.6__
Only tested with Hero 4 Black and above


# Example

```python
import asyncio
from aiogopro import Camera, constants
camera = Camera()

async def run():
    print('connecting')
    print(await camera.connect())
    print('internal_battery_level:', await camera.getStatus(constants.Status.System.internal_battery_level))
    print('ap_ssid:', await camera.getStatus(constants.Status.Wireless.ap_ssid))
    print('date_time:', await camera.timeGet())
    print('time sync:', await camera.timeSync())
    await asyncio.sleep(1)
    print('date_time:', await camera.timeGet())
    await camera.quit()

asyncio.get_event_loop().run_until_complete(run())
print("Done")
```