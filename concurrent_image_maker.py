#!/usr/bin/env python3
import _thread
import time
import os
import errno
import hashlib
import sys

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from PIL import Image

# Look in constants.py to change map settings
from constants import *

# Change upload to true to set up google drive upload capabiltiies
if UPLOAD:
    import upload_image

def main(frame):
    y_center = 42.352819  # Latitude (y_center is not a mistake!)
    x_center = -71.100256 # Longitude

    # Create a URL for specific latitude, longitude and zoom
    # 
    # Each google maps image is composed of latitude, longitude, zoom
    # latitude and longitude are the y and x coordinates respectively,
    # and zoom determines how far the map is zoomed in. Higher value of
    # zoom means more detail on the map
    def createURL(MAP_URL, long, lat, zoom = '13'): 
        URL = MAP_URL + str(lat) + ',' + str(long) + ',' + str(zoom) + 'z'
        return URL

    # Crop the maps image at the center to remove logos and watermarks to
    #   create a 800 x 800 pixel image
    def crop(img):
        half_the_width = img.size[0] // 2
        half_the_height = img.size[1] // 2
        img = img.crop(
            (
                half_the_width - PIXEL_LENGTH // 2,
                half_the_height - PIXEL_LENGTH // 2,
                half_the_width + PIXEL_LENGTH // 2,
                half_the_height + PIXEL_LENGTH // 2
            )
        )
        return img

    # Convert to positive indices
    def pos_indices(int):
        return int + IMG_COUNTER - 1

    # Save data necessary to replicate program run
    def write_data():
        file = open('./map/FULL_MAP_DATA.txt', 'w')
        file.write('Center coordinate: (%s, %s) \n' %(y_center, x_center))
        file.write('Zoom: ' + DESIRED_ZOOM + '\n')
        file.write('Picture format: ' + pic_format + '\n')
        file.write('IMG_COUNTER: ' + str(IMG_COUNTER) + '\n')
        if UPLOAD:
            upload_image.main('./map/FULL_MAP_DATA.txt', folder_id)
            file.write('Folder ID: %s' %(folder_id))
        file.write('hash_tag: ' + hash_tag + '\n')
        file.close()

    # Make directory with dir_name
    def make_dir(dir_name):
        try:
            os.makedirs(dir_name)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    # Adjust from base zoom level of 19 and recalibrate for large monitor
    ZOOM_SCALING = pow(2, int(DESIRED_ZOOM) - int(CALIBRATED_ZOOM))

    # Make directories for storage
    make_dir('./map')

    # There are some bugs with chromedriver maximizing
    def keeptrying():
        try:
            browser.maximize_window()
        except:
            keeptrying()

    # Initialize browser and get DPI and resolution of the monitor 
    browser = webdriver.Chrome()
    # browser.maximize_window()
    keeptrying()
    browser.get('https://www.infobyip.com/detectmonitordpi.php')
    DPI = browser.find_element_by_xpath('//*[@id="text"]').text
    idx = DPI.find(' ')
    DPI_X = CALIBRATED_DPI / float(DPI[0 : idx])
    DPI_Y = CALIBRATED_DPI / float(DPI[idx + 3:])

    # Get aspect ratio of monitor to calculate coordinate equivalent of 800 pixels 
    browser.get('https://www.infobyip.com/detectscreenresolution.php')
    ratio_str = browser.find_element_by_xpath('//*[@id="aspect_ratio"]').text
    ratio = float(ratio_str[ratio_str.index('=')+1:])
    ASPECT_RATIO_SCALING = ratio / CALIBRATED_ASPECT_RATIO
    CALIBRATED_UNIT_Y = 0.00171849462 - .0004516129 * ASPECT_RATIO_SCALING

    #Get google maps main page and extract present coordinates
    if not ENTER_COOR:
        browser.get(MAP_URL)
        time.sleep(5) # Wait for Google maps URL to update by finding IP address coordinates
        URL = browser.current_url
        idx = URL.find(',')
        y_center = float(URL[URL.find('@') + 1:idx]) #Note latitude is Y and longitude is X
        x_center = float(URL[idx + 1:URL.rfind(',')])

    # Hash coordinates to get unique tag
    hash_tag = hashlib.sha256(str(x_center + y_center).encode('utf-8')).hexdigest()[:3]
    if UPLOAD:
        folder_id = upload_image.create_folder(hash_tag)
    else:
        folder_id = 'null'
    write_data() 

    indices = {
        'T': (0, IMG_COUNTER),
        'B': (-IMG_COUNTER + 1, 0),
        'L': (-IMG_COUNTER + 1, 0),
        'R': (0, IMG_COUNTER),
    }
    x_frame = indices[frame[1]]
    y_frame = indices[frame[0]]

    count = 0
    # Iterate through coordinates and save a cropped screenshot
    for i in range(x_frame[0],x_frame[1]):
        for j in range(y_frame[0], y_frame[1]):
            x = pos_indices(i)
            y = pos_indices(j)
            picstr = str(x) + ',' + str(y) + pic_format
            count += 1 
            if not os.path.isfile(picstr):
                newX = x_center + CALIBRATED_UNIT_X * DPI_X / ZOOM_SCALING * i
                newY = y_center - CALIBRATED_UNIT_Y * DPI_Y / ZOOM_SCALING * j 
                URL = createURL(MAP_URL, newX, newY, DESIRED_ZOOM)
                browser.get(URL)
                browser.save_screenshot(picstr)
                img = Image.open(picstr)
                img = crop(img)
                img.save(picstr)
                if UPLOAD:
                    upload_image.main(picstr, folder_id)
            else:
                print('%s exists, skipping' %(picstr))
            print('%s out of %s' %(count,total_images/len(indices)))
    browser.quit()

_thread.start_new_thread(main, ('BR',))
_thread.start_new_thread(main, ('TR',))
_thread.start_new_thread(main, ('TL',))
_thread.start_new_thread(main, ('BL',))

while 1:
    pass