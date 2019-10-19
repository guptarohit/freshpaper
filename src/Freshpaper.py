import logging
import sys

import click

from Constants import BING_IMAGE_DESCRIPTION, NASA_IMAGE_DESCRIPTION, IMAGE_SOURCES
from src.DownloadUtils import DownloadUtils
from src.SystemUtils import SystemUtils
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
        wallpaper = WallpaperUtils()
        downloadUtils = DownloadUtils()
        systemUtils = SystemUtils()
        directory_name = systemUtils.get_wallpaper_directory()  # Wallpaper directory name
        freshpaperSources = construct_freshpaper_sources(downloadUtils.download_image_bing,
                                                         downloadUtils.download_image_nasa)
        try:
            download_image = freshpaperSources.get(source)["download"]
            image_path = download_image(directory_name)

            wallpaper.set_wallpaper(image_path)
        except ConnectionError:
            image_path = systemUtils.get_saved_wallpaper(directory_name)
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
