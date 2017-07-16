# For running program concurrently, BOTTOM LEFT

from selenium import webdriver
from PIL import Image
import time
import os
import errno
import upload_image
import hashlib

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
    half_the_width = img.size[0] / 2
    half_the_height = img.size[1] / 2
    img = img.crop(
        (
            half_the_width - PIXEL_LENGTH / 2,
            half_the_height - PIXEL_LENGTH / 2,
            half_the_width + PIXEL_LENGTH / 2,
            half_the_height + PIXEL_LENGTH / 2
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
    file.write('Folder ID: %s' %(folder_id))
    file.write('hash_tag: ' + hash_tag + '\n')
    file.close()
    upload_image.main('./map/FULL_MAP_DATA.txt', folder_id)

# Make directory with dir_name
def make_dir(dir_name):
    try:
        os.makedirs(dir_name)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

#VARIABLES
DESIRED_ZOOM = '21' # Zoom level of map. 2x zoom for each integer increment  
                    # No significant detail increase after zoom = 19
                    # Max zoom is 21
pic_format = '.png' # '.jpg' Use png for large images (pixel dimension > 65500)
IMG_COUNTER = 70 #2n - 1 = Number of rows and columns of images

total_images = pow(2 * IMG_COUNTER - 1, 2)

#CONSTANTS
#
# All constants were calibrated simultaneously. DON'T CHANGE THESE VALUES 
CALIBRATED_DPI = 120 # Base DPI, later scaled for current monitor
CALIBRATED_ZOOM = '19' #Zoom level for clear building outlines and street names
CALIBRATED_UNIT_X = 0.00171849462 #Coordinate equivalent of 800 x pixels at 19 zoom
CALIBRATED_ASPECT_RATIO = 1920 / 1080.0 #Resolution of computer
MAP_URL = 'https://www.google.com/maps/@' #Base URL for google maps
PIXEL_LENGTH = 800 #Length and width of each cropped screenshot.

# Adjust from base zoom level of 19 and recalibrate for large monitor
ZOOM_SCALING = pow(2, int(DESIRED_ZOOM) - int(CALIBRATED_ZOOM))

# Make directories for storage
make_dir('./map')
# make_dir('./map_data')

#Ask for coordinates
user_coord_bool = 'y' == raw_input('Enter in your coordinates? (IP address location by default) [y/n] \n')
if user_coord_bool:
    valid = False
    while not valid: 
        y_center = float(input('Enter latitude between [-90, 90]: \n'))
        valid =  y_center < 90.0 and y_center > -90.0
    valid = False
    while not valid:
        x_center = float(input('Enter longitude between [-180, 180]: \n'))
        valid = x_center < 180.0 and x_center > -180.0

# Initialize browser and get DPI and resolution of the monitor 
browser = webdriver.Chrome()
browser.maximize_window()
browser.get('https://www.infobyip.com/detectmonitordpi.php')
DPI = browser.find_element_by_xpath('//*[@id="text"]').text
idx = DPI.find(' ')
DPI_X = CALIBRATED_DPI / float(DPI[0 : idx])
DPI_Y = CALIBRATED_DPI / float(DPI[idx + 3:])

# Get aspect ratio of monitor to calculate coordinate equivalent of 800 pixels 
browser.get('https://www.infobyip.com/detectscreenresolution.php')
ratio = float(browser.find_element_by_xpath('//*[@id="aspect_ratio"]').text)
ASPECT_RATIO_SCALING = ratio / CALIBRATED_ASPECT_RATIO
CALIBRATED_UNIT_Y = 0.00171849462 - .0004516129 * ASPECT_RATIO_SCALING

#Get google maps main page and extract present coordinates
if not user_coord_bool:
    browser.get(MAP_URL)
    time.sleep(8) # Wait for Google maps URL to update by finding IP address coordinates
    URL = browser.current_url
    idx = URL.find(',')
    y_center = float(URL[URL.find('@') + 1:idx]) #Note latitude is Y and longitude is X
    x_center = float(URL[idx + 1:URL.rfind(',')])

# Hash coordinates to get unique tag
hash_tag = hashlib.sha256(str(x_center + y_center)).hexdigest()[:3]
folder_id = upload_image.create_folder(hash_tag)
write_data() 

count = 0
# Iterate through coordinates and save a cropped screenshot
for i in range(-IMG_COUNTER+1,0):
    for j in range(-IMG_COUNTER + 1, 0):
        x = pos_indices(i)
        y = pos_indices(j)
        picstr = str(x) + ',' + str(y) + pic_format
        count += 1 
        if not os.path.isfile(picstr):
            newX = x_center + CALIBRATED_UNIT_X * DPI_X / ZOOM_SCALING * i
            newY = y_center - CALIBRATED_UNIT_Y * DPI_Y / ZOOM_SCALING * j 
            URL = createURL(MAP_URL, newX, newY, DESIRED_ZOOM)
            browser.get(URL)
            # time.sleep(.5)
            browser.save_screenshot(picstr)
            img = Image.open(picstr)
            img = crop(img)
            img.save(picstr)
            upload_image.main(picstr, folder_id)
        else:
            print picstr + ' exists, skipping'
        print '%s out of %s' %(count,total_images)
browser.quit()

