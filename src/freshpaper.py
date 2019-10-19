import logging
import os
import sys
from random import choice

import click
from pip._vendor.requests import ConnectionError

from Constants import BING_IMAGE_DESCRIPTION, NASA_IMAGE_DESCRIPTION, IMAGE_SOURCES
from src.DownloadUtils import DownloadUtils
from src.WallpaperUtils import WallpaperUtils

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


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--source",
    default="bing",
    type=click.Choice(IMAGE_SOURCES),
    help="Source for setting the wallpaper.",
)
def main(context, source):
    if context.invoked_subcommand is None:
        directory_name = get_wallpaper_directory()  # Wallpaper directory name
        wallpaper = WallpaperUtils()
        downloadUtils = DownloadUtils()
        freshpaperSources = construct_freshpaper_sources(downloadUtils.download_image_bing,
                                     downloadUtils.download_image_nasa)
        try:
            download_image = freshpaperSources.get(source)["download"]
            image_path = download_image(directory_name)

            wallpaper.set_wallpaper(image_path)
        except ConnectionError:
            image_path = get_saved_wallpaper(directory_name)
            wallpaper.set_wallpaper(image_path)
        except Exception as e:
            log.error(e)


def construct_freshpaper_sources(source1, source2):
    return {
        "bing": {"download": source1, "description": BING_IMAGE_DESCRIPTION},
        "nasa": {"download": source2, "description": NASA_IMAGE_DESCRIPTION},
    }


if __name__ == "__main__":
    main()
