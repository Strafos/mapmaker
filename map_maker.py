from selenium import webdriver
from PIL import Image
import time
import upload_image
import os
import errno
 
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

#VARIABLES
DESIRED_ZOOM = '19' # Zoom level of map. 2x zoom for each integer increment  
                    # No significant detail increase after zoom = 19
                    # Max zoom is 21
pic_format = '.png' # '.jpg' Use png for large images (pixel dimension > 65500)
IMG_COUNTER = 1 #2n - 1 = Number of rows and columns of images

total_images = pow(2 * IMG_COUNTER - 1, 2)

#CONSTANTS
#
#All constants were calibrated simultaneously. DON'T CHANGE THESE VALUES 
CALIBRATED_DPI = 120 # Base DPI, later scaled for current monitor
CALIBRATED_ZOOM = '19' #Zoom level for clear building outlines and street names
CALIBRATED_UNIT_X = 0.00171849462 #Coordinate equivalent of 800 x pixels at 19 zoom
CALIBRATED_ASPECT_RATIO = 1920 / 1080.0 #Resolution of computer
MAP_URL = 'https://www.google.com/maps/@' #Base URL for google maps
PIXEL_LENGTH = 800 #Length and width of each cropped screenshot.

# Adjust from base zoom level of 19 and recalibrate for large monitor
ZOOM_SCALING = pow(2, int(DESIRED_ZOOM) - int(CALIBRATED_ZOOM))

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
# user_coord_bool = False

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

# Iterate through coordinates and save a cropped screenshot
count = 0
for i in range(-IMG_COUNTER+1,IMG_COUNTER):
    for j in range(-IMG_COUNTER+1, IMG_COUNTER):
        newX = x_center + CALIBRATED_UNIT_X * DPI_X / ZOOM_SCALING * i
        newY = y_center - CALIBRATED_UNIT_Y * DPI_Y / ZOOM_SCALING * j 
        URL = createURL(MAP_URL, newX, newY, DESIRED_ZOOM)
        browser.get(URL)
        # time.sleep(.5)
        picstr = str(i) + ',' + str(j) + pic_format
        browser.save_screenshot(picstr)
        crop(Image.open(picstr)).save(picstr) #open, crop, and save image
        count += 1 
        print '%s out of %s' %(count,total_images)
browser.quit()

# Create blank canvas for stitched image
total_widths = int((2 * IMG_COUNTER - 1) * PIXEL_LENGTH)
total_heights = int((2 * IMG_COUNTER - 1) * PIXEL_LENGTH)
final_img = Image.new('RGB', (total_widths, total_heights))

# Paste individual images onto canvas and delete
for i in range(-IMG_COUNTER+1, IMG_COUNTER):
    for j in range(-IMG_COUNTER+1, IMG_COUNTER):
        x = int(PIXEL_LENGTH * (i + IMG_COUNTER - 1))
        y = int(PIXEL_LENGTH * (j + IMG_COUNTER - 1))
        picstr = str(i) + ',' + str(j) + pic_format
        image = Image.open(picstr) 
        final_img.paste(image, (x, y))
        os.remove(picstr)


try:
    os.makedirs('./map')
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise

final_img.save('./map/FULL_MAP' + pic_format)

top = y_center + (IMG_COUNTER - 1) * CALIBRATED_UNIT_Y * DPI_Y / ZOOM_SCALING
bot = y_center - (IMG_COUNTER - 1) * CALIBRATED_UNIT_Y * DPI_Y / ZOOM_SCALING
right = x_center + (IMG_COUNTER - 1) * CALIBRATED_UNIT_X * DPI_X / ZOOM_SCALING
left = x_center - (IMG_COUNTER - 1) * CALIBRATED_UNIT_X * DPI_X / ZOOM_SCALING

file = open('./map/FULL_MAP_DATA.txt', 'w')
file.write('Center coordinate: (%s, %s) \n' %(y_center, x_center))
file.write('Zoom: ' + DESIRED_ZOOM + '\n')
file.write('Picture format: ' + pic_format + '\n')
file.write('IMG_COUNTER: ' + str(IMG_COUNTER) + '\n')
file.write('top, bot, right, left: %s %s %s %s' %(top,bot,right,left))
file.close()

upload_image.main()
