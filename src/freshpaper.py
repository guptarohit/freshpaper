import os
import re
import sys
import click
import json
import logging
from random import choice
from datetime import datetime
from subprocess import check_call, CalledProcessError
from PIL import Image
from pip._vendor.requests import ConnectionError

from constants import NASA_IMAGE_URL, BING_IMAGE_URL, BING_IMAGE_DESCRIPTION, NASA_IMAGE_DESCRIPTION
from src.wallpaperUtils import wallpaperUtils

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

def get_saved_wallpaper(wall_dir):
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


def get_wallpaper_directory():
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


def download_image_bing(download_dir, image_extension="jpg"):
    """
    Download & save the image
    :param download_dir: directory where to download the image
    :param image_extension: directory where to download the image
    :return: downloaded image path
    """
    # mkt(s) HIN, EN-IN


    try:
        image_data = json.loads(urlopen(BING_IMAGE_URL).read().decode("utf-8"))

        image_url = "http://www.bing.com" + image_data["images"][0]["url"]

        image_name = re.search(r"OHR\.(.*?)_", image_url).group(1)

        image_url_hd = "http://www.bing.com/hpwp/" + image_data["images"][0]["hsh"]
        date_time = datetime.now().strftime("%d_%m_%Y")
        image_file_name = "{image_name}_{date_stamp}.{extention}".format(
            image_name=image_name, date_stamp=date_time, extention=image_extension
        )

        image_path = os.path.join(os.sep, download_dir, image_file_name)
        log.debug("download_dir: {}".format(download_dir))
        log.debug("image_file_name: {}".format(image_file_name))
        log.debug("image_path: {}".format(image_path))

        if os.path.isfile(image_path):
            log.info("No new wallpaper yet..updating to latest one.\n")
            return image_path

        try:
            log.info("Downloading..")
            urlretrieve(image_url_hd, filename=image_path)
        except HTTPError:
            log.info("Downloading...")
            urlretrieve(image_url, filename=image_path)
        return image_path
    except URLError:
        log.error("Something went wrong..\nMaybe Internet is not working...")
        raise ConnectionError


def download_image_nasa(download_dir, image_extension="jpg"):
    """
    Download & save the image
    :param download_dir: directory where to download the image
    :param image_extension: directory where to download the image
    :return: downloaded image path
    """

    try:
        image_data = json.loads(urlopen(NASA_IMAGE_URL).read().decode("utf-8"))

        image_url = image_data.get("url")

        image_name = image_data.get("title").split(" ")[0]

        image_url_hd = image_data.get("hdurl")
        date_time = datetime.now().strftime("%d_%m_%Y")
        image_file_name = "{image_name}_{date_stamp}.{extention}".format(
            image_name=image_name, date_stamp=date_time, extention=image_extension
        )

        image_path = os.path.join(os.sep, download_dir, image_file_name)
        log.debug("download_dir: {}".format(download_dir))
        log.debug("image_file_name: {}".format(image_file_name))
        log.debug("image_path: {}".format(image_path))

        if os.path.isfile(image_path):
            log.info("No new wallpaper yet..updating to latest one.\n")
            return image_path

        try:
            log.info("Downloading..")
            urlretrieve(image_url_hd, filename=image_path)
        except HTTPError:
            log.info("Downloading...")
            urlretrieve(image_url, filename=image_path)
        return image_path
    except URLError:
        log.error("Something went wrong..\nMaybe Internet is not working...")
        raise ConnectionError


freshpaperSources = {
    "bing": {"download": download_image_bing, "description": BING_IMAGE_DESCRIPTION},
    "nasa": {"download": download_image_nasa, "description": NASA_IMAGE_DESCRIPTION},
}


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--source",
    default="bing",
    type=click.Choice(freshpaperSources.keys()),
    help="Source for setting the wallpaper.",
)
def main(context, source):
    if context.invoked_subcommand is None:
        directory_name = get_wallpaper_directory()  # Wallpaper directory name
        wallpaper = wallpaperUtils()
        try:
            download_image = freshpaperSources.get(source)["download"]
            image_path = download_image(directory_name)

            wallpaper.set_wallpaper(image_path)
        except ConnectionError:
            image_path = get_saved_wallpaper(directory_name)
            wallpaper.set_wallpaper(image_path)
        except Exception as e:
            log.error(e)


if __name__ == "__main__":
    main()
