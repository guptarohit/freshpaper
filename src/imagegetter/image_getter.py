import json
import os
import re
import sys
from datetime import datetime
from random import choice
from subprocess import check_call, CalledProcessError
from typing import  Dict
from common.logger import get_common_logger

try:
    # for python3
    from urllib.request import urlopen, urlretrieve, HTTPError, URLError
except ImportError:
    # for python2
    from urllib import urlretrieve
    from urllib2 import urlopen, HTTPError, URLError
from PIL import Image
if sys.platform.startswith("win32"):
    import win32api
    import win32con
    import win32gui


class ImageGetter:
    def __init__(self, logger=None)-> None:
        if logger is None:
            self.logger = get_common_logger()
        self.logger = logger
        self.bing_image_url = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=EN-IN"
        self.nasa_image_url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"

    def set_wallpaper(self, image_path: str):
        """ Given a path to an image, set it as the wallpaper """
        if not os.path.exists(image_path):
            self.logger.error("Image does not exist.")
            sys.exit(1)

        self.logger.info("Updating wallpaper..")
        self.logger.info(
            "Name of wallpaper: {}".format(
                re.sub("([a-z])([A-Z])", r"\1 \2", image_path.split("/")[-1].split("_")[0])
            )
        )

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
        elif sys.platform.startswith("darwin"):
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
                self.logger.error("Setting wallpaper failed.")
                sys.exit(1)
        elif sys.platform.startswith("linux"):
            check_call(
                [
                    "gsettings",
                    "set",
                    "org.gnome.desktop.background",
                    "picture-uri",
                    "file://{}".format(image_path),
                ]
            )

        self.logger.info("Wallpaper successfully updated. :)")

    def get_saved_wallpaper(self, wall_dir):
        """ returns random saved wallpaper's path """

        files = os.listdir(wall_dir)
        if files:
            self.logger.info("\nRandomly picking from saved wallpapers.")
            image_name = choice(files)
            image_path = os.path.join(os.sep, wall_dir, image_name)
            return image_path
        else:
            self.logger.error("There is no wallpaper available offline.")
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
            self.logger.error("wallpaper directory does not exist.")
            os.makedirs(wall_dir)
            self.logger.info("created wallpaper directory at: {}".format(wall_dir))

        return wall_dir

    def __get_bing_image(self, image_extension: str):
        """
        get bing image data
        :param image_extension:
        :return:
        """
        # mkt(s) HIN, EN-IN
        image_data = json.loads(urlopen(self.bing_image_url).read().decode("utf-8"))

        image_url = "http://www.bing.com" + image_data["images"][0]["url"]

        image_name = re.search(r"OHR\.(.*?)_", image_url).group(1)

        image_url_hd = "http://www.bing.com/hpwp/" + image_data["images"][0]["hsh"]
        date_time = datetime.now().strftime("%d_%m_%Y")
        image_file_name = "{image_name}_{date_stamp}.{extention}".format(
            image_name=image_name, date_stamp=date_time, extention=image_extension
        )
        return image_file_name, image_url_hd, image_url

    def __get_nasa_image(self, image_extension: str):
        """
        get nasa image data
        :param image_extension:
        :return:
        """
        image_data = json.loads(urlopen(self.nasa_image_url).read().decode("utf-8"))

        image_url = image_data.get("url")

        image_name = image_data.get("title").split(" ")[0]

        image_url_hd = image_data.get("hdurl")
        date_time = datetime.now().strftime("%d_%m_%Y")
        image_file_name = "{image_name}_{date_stamp}.{extention}".format(
            image_name=image_name, date_stamp=date_time, extention=image_extension
        )
        return image_file_name, image_url_hd, image_url

    def download_image(self, download_dir, image_file_name, image_url_hd, image_url):
        """
        download image from website
        :param download_dir:
        :param image_file_name:
        :param image_url_hd:
        :param image_url:
        :return:
        """
        image_path = os.path.join(os.sep, download_dir, image_file_name)
        self.logger.debug("download_dir: {}".format(download_dir))
        self.logger.debug("image_file_name: {}".format(image_file_name))
        self.logger.debug("image_path: {}".format(image_path))

        if os.path.isfile(image_path):
            self.logger.info("No new wallpaper yet..updating to latest one.\n")
            return image_path

        try:
            self.logger.info("Downloading..")
            urlretrieve(image_url_hd, filename=image_path)
        except HTTPError:
            self.logger.info("Downloading...")
            urlretrieve(image_url, filename=image_path)
        return image_path

    def download_image_bing(self, download_dir, image_extension="jpg"):
        """
        Download & save the image
        :param download_dir: directory where to download the image
        :param image_extension: directory where to download the image
        :return: downloaded image path
        """
        try:
            image_file_name, image_url_hd, image_url = self.__get_bing_image(image_extension)
            return self.download_image(download_dir, image_file_name, image_url_hd, image_url)
        except URLError:
            self.logger.error("Something went wrong..\nMaybe Internet is not working...")
            raise ConnectionError

    def download_image_nasa(self, download_dir, image_extension="jpg"):
        """
        Download & save the image
        :param download_dir: directory where to download the image
        :param image_extension: directory where to download the image
        :return: downloaded image path
        """
        image_file_name, image_url_hd, image_url = self.__get_nasa_image(image_extension)
        try:
            return self.download_image(download_dir, image_file_name, image_url_hd, image_url)
        except URLError:
            self.logger.error("Something went wrong..\nMaybe Internet is not working...")
            raise ConnectionError

    def get_freshpaper_sources(self) -> Dict:
        """
        get fresh_paper source
        :return:
        """
        return {
            "bing": {"download": self.download_image_bing, "description": "Bing photo of the day"},
            "nasa": {"download": self.download_image_nasa, "description": "NASA photo of the day"},
        }
