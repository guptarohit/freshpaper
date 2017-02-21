#!/usr/bin/python
# -*- coding: utf-8 -*-

# Program to set bing image of the day as desktop wallpaper.

__author__ = 'Rohit Gupta'
__copyright__ = 'Copyright (C) 2017 Rohit Gupta'

import win32api
import win32con
import win32gui
import json
import re
from urllib.request import urlopen, urlretrieve
from os import path, system, remove, listdir
from datetime import datetime
from PIL import Image
from random import choice

now = datetime.now()

def _GetchWindows():
    # This reads only one character.
    from msvcrt import getch
    return getch()

def setWallPaperFromBmp(bmp):
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, 'Control Panel\\Desktop', 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, 'WallpaperStyle', 0, win32con.REG_SZ,'0')
    win32api.RegSetValueEx(key, 'TileWallpaper', 0, win32con.REG_SZ, '0')
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, bmp, 1+2)


def setWallPaper(pathToImage):
    """ Given a path to an image, convert it to .bmp format and set it as the wallpaper"""
    print("Changing wallpaper..")

    bmpImage = Image.open(pathToImage)
    tempPath = path.expanduser('~') + '\\Bing_Pic_of_the_Day\\'
    tempPath = path.join(tempPath, 'wallpaper_of_the_day.bmp')
    bmpImage.save(tempPath, 'BMP')
    setWallPaperFromBmp(tempPath)
    remove(tempPath)
    print('\nWallpaper successfully updated. :)')


def setWallPaperFromFileList(pathToDir):
    """ Given a directory choose an image from it and set it as a wallpaper """

    # files or directories, try a few times to set a wallpaper, and then just give up.

    print('\nIf old wallpapers available, changing from those...')

    tries = 0
    done = False

    while not done and tries < 3:
        try:
            files = listdir(pathToDir)
            if files:
                image = choice(files)
                setWallPaper(path.join(pathToDir, image))
                done = True
            else:
                print('\nThere is no wallpaper available offline.')
                done = True
        except:
            tries += 1


def main():

    # mkt(s) HIN, EN-IN

    url = 'http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=EN-IN'

    dir_name = path.expanduser('~') + '\\Bing_Pic_of_the_Day\\'  # Wallpaper directory name

    try:
        print("Checking if your Internet is working.. ;)")
        image_data = json.loads(urlopen(url).read().decode('utf-8'))

        image_url = 'http://www.bing.com' + image_data['images'][0]['url']

        image_download_url = 'http://www.bing.com/hpwp/' + image_data['images'][0]['hsh']
        date_time = '_' + str(now.day) + '_' + str(now.month) + '_' + str(now.year)
        image_name = image_url[re.search('rb/', image_url).end():re.search('_EN', image_url).start()] + date_time + '.jpg'

        # image description
        # image_desc = image_data['images'][0]['copyright']

        if not path.isdir(dir_name):
            print("Creating a directory at this location:\n"+dir_name+"\nhere all wallpapers will be downloaded in future.. :)")
            system('mkdir ' + dir_name)

        file_path = dir_name + image_name

        try:
            # Trying for a better quality image ;)
            if path.isfile(file_path):
                print("No new wallpaper yet.. ;)")
                setWallPaper(file_path)
            else:
                print("Downloading..")
                urlretrieve(image_download_url, filename=file_path)
                setWallPaper(file_path)
        except:
            if path.isfile(file_path):
                print("No new wallpaper yet.. ;)")
                setWallPaper(file_path)
            else:
                print("Downloading...")
                urlretrieve(image_url, filename=file_path)
                setWallPaper(file_path)
    except:

        # if no Internet connection or something went wrong..anything..just pass ;)
        print('Something went wrong..\nMaybe Internet is not working...')
        setWallPaperFromFileList(dir_name)


if __name__ == '__main__':
    main()    
    print("\nPress any key to exit.")
    _GetchWindows()
