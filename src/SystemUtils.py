import logging
import os
import sys
from random import choice

try:
    # for python3
    from urllib.request import urlopen, urlretrieve, HTTPError, URLError
except ImportError:
    # for python2

    from urllib import urlretrieve
    from urllib2 import urlopen, HTTPError, URLError

if sys.platform.startswith("win32"):
    pass

logging.basicConfig(level=logging.INFO, format="%(message)s")

log = logging.getLogger(__name__)


class SystemUtils:
    def __init__(self):
        pass

    def get_saved_wallpaper(self, wall_dir):
        """ returns random saved wallpaper's path """

        files = os.listdir(wall_dir)
        if files:
            log.info("\nRandomly picking from saved wallpapers.")
            image_name = choice(files)
            image_path = os.path.join(os.sep, wall_dir, image_name)
            return image_path
        else:
            log.error("There is no wallpaper available offline.")
            sys.exit(1)

    def get_wallpaper_directory(self):
        """ check if `default` wallpaper download directory exists or not, create if doesn't exist """
        pictures_dir = ""
        wall_dir_name = "freshpaper"
        os.path.join(os.sep, os.path.expanduser("~"), "a", "freshpaper")
        if sys.platform.startswith("win32"):
            pictures_dir = "My Pictures"
        elif sys.platform.startswith("darwin"):
            pictures_dir = "Pictures"
        elif sys.platform.startswith("linux"):
            pictures_dir = "Pictures"
        wall_dir = os.path.join(
            os.sep, os.path.expanduser("~"), pictures_dir, wall_dir_name
        )

        if not os.path.isdir(wall_dir):
            log.error("wallpaper directory does not exist.")
            os.makedirs(wall_dir)
            log.info("created wallpaper directory at: {}".format(wall_dir))

        return wall_dir
