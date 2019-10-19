import os
import re
import json
from datetime import datetime
import constants as CT

import logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

log = logging.getLogger(__name__)

try:
    # for python3
    from urllib.request import urlopen, urlretrieve, HTTPError, URLError
except ImportError:
    # for python2
    from urllib import urlretrieve
    from urllib2 import urlopen, HTTPError, URLError


def download_image_bing_():
    url = CT.BING_URL
    image_data = json.loads(urlopen(url).read().decode(CT.DECODE_METHOD))
    image_url = "http://www.bing.com" + image_data["images"][0]["url"]
    image_name = re.search(r"OHR\.(.*?)_", image_url).group(1)
    image_url_hd = "http://www.bing.com/hpwp/" + image_data["images"][0]["hsh"]
    return image_data, image_name, image_url_hd, image_url


def download_image_nasa_():
    url = CT.NASA_URL
    image_data = json.loads(urlopen(url).read().decode(CT.DECODE_METHOD))
    image_url = image_data.get("url")
    image_name = image_data.get("title").split(" ")[0]
    image_url_hd = image_data.get("hdurl")
    return image_data, image_name, image_url_hd, image_url


def download_image(source, download_dir, image_extension):

    """
    Download & save the image
    :param download_dir: directory where to download the image
    :param image_extension: directory where to download the image
    :return: downloaded image path
    """

    if source == CT.NASA:
        image_data, image_name, image_url_hd, image_url = download_image_bing_()
    else:
        image_data, image_name, image_url_hd, image_url = download_image_nasa_()
    try:
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