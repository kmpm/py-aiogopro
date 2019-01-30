Python async I/O GoPro module
=============================

__Requires Python >= 3.6__
Only tested with Hero 4 Black and above

# Develop
```bash
clone py-aiogopro
cd py-aiogopro
python3 -m venv venv
source venv\bin\activate
pip install -e .
```

## Download json spec from camera
```bash
curl http://10.5.5.9/gp/gpControl -o gpcontrol.json
# optionally, make it pretty
python ./tools/prettygp.py --replace gpcontrol.json
```

## Refresh constants.py from spec
```bash
python ./tools/generate_constants.py ./doc/HD7_01_01_70_00.json
```