import json
import logging
import os
import re
from datetime import datetime

from pip._vendor.requests import ConnectionError

from Constants import NASA_IMAGE_URL, BING_IMAGE_URL

try:
    # for python3
    from urllib.request import urlopen, urlretrieve, HTTPError, URLError
except ImportError:
    # for python2
    from urllib import urlretrieve
    from urllib2 import urlopen, HTTPError, URLError


logging.basicConfig(level=logging.INFO, format="%(message)s")

log = logging.getLogger(__name__)

class DownloadUtils:

    def __init__(self):
        pass

    def download_image_bing(self, download_dir, image_extension="jpg"):
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


    def download_image_nasa(self, download_dir, image_extension="jpg"):
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