Python async I/O GoPro module
=============================



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