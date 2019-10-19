import os
import re
import sys
from subprocess import check_call, CalledProcessError
import logging

from PIL import Image

try:
    # for python3
    from urllib.request import urlopen, urlretrieve, HTTPError, URLError
except ImportError:
    # for python2
    from urllib import urlretrieve
    from urllib2 import urlopen, HTTPError, URLError

if sys.platform.startswith("win32"):
    import win32api
    import win32con
    import win32gui

logging.basicConfig(level=logging.INFO, format="%(message)s")

log = logging.getLogger(__name__)


class WallpaperUtils:
    def __init__(self):
        pass

    def set_wallpaper(self, image_path):
        """ Given a path to an image, set it as the wallpaper """
        if not os.path.exists(image_path):
            log.error("Image does not exist.")
            sys.exit(1)

        log.info("Updating wallpaper..")
        log.info(
            "Name of wallpaper: {}".format(
                re.sub("([a-z])([A-Z])", r"\1 \2", image_path.split("/")[-1].split("_")[0])
            )
        )

        self.setWallpaperForWindows(image_path)
        self.setWallpaperForMacOS(image_path)
        self.setWallpaperForLinux(image_path)

        log.info("Wallpaper successfully updated. :)")

    def setWallpaperForLinux(self, image_path):
        if sys.platform.startswith("linux"):
            check_call(
                [
                    "gsettings",
                    "set",
                    "org.gnome.desktop.background",
                    "picture-uri",
                    "file://{}".format(image_path),
                ]
            )

    def setWallpaperForMacOS(self, image_path):
        if sys.platform.startswith("darwin"):
            try:
                command = """
                    osascript -e 'tell application "System Events"
                        set desktopCount to count of desktops
                        repeat with desktopNumber from 1 to desktopCount
                            tell desktop desktopNumber
                                set picture to "{image_path}"
                            end tell
                        end repeat
                    end tell'
                    """.format(
                    image_path=image_path
                )

                check_call([command], shell=True)
            except CalledProcessError or FileNotFoundError:
                log.error("Setting wallpaper failed.")
                sys.exit(1)

    def setWallpaperForWindows(self, image_path):
        if sys.platform.startswith("win32"):
            bmp_image = Image.open(image_path)
            bmp_img_path = os.path.splitext(image_path)[0] + ".bmp"
            bmp_image.save(bmp_img_path, "BMP")
            key = win32api.RegOpenKeyEx(
                win32con.HKEY_CURRENT_USER,
                "Control Panel\\Desktop",
                0,
                win32con.KEY_SET_VALUE,
            )
            win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
            win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
            win32gui.SystemParametersInfo(
                win32con.SPI_SETDESKWALLPAPER, bmp_img_path, 1 + 2
            )
            os.remove(bmp_img_path)
