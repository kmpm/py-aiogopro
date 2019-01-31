
# FS object in gpMediaList
- n : filename
- cre : created timestamp
- mod : modified timestamp
- s : size in bytes


## Photo
```json
{
    "n": "GOPR0256.JPG",
    "cre": "1548846642",
    "mod": "1548846642",
    "s": "3792523"
}
```
## Mutlishot Photo
- b : lower bound
- l : upper bound
- g : group? if n = G001 then g=1 and so on
- t : ? b could be burst. Seen on burst and multishot photo
- m : ?

```json
{
    "n": "G0010299.JPG",
    "g": "1",
    "b": "299",
    "l": "319",
    "cre": "1548866956",
    "mod": "1548866956",
    "s": "50530483",
    "t": "b",
    "m": []
}
```

## Video
- glrv : ?
- ls : ?
```json
{
    "n": "GH010368.MP4",
    "cre": "1548868378",
    "mod": "1548868378",
    "glrv": "280888",
    "ls": "-1",
    "s": "20478993"
}
```