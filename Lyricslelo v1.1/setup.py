from distutils.core import setup
import py2exe

windows = [{"script": "Lyricslelo.py",
        "icon_resources": [(1, "icon4.ico")],
            },]
setup(
    version = "1.1",
    description = "Lyricslelo",
    name = "Lyricslelo",
    # targets to build
    windows = windows,
    )