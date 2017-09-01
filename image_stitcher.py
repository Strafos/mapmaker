from PIL import Image
import math
import os
import upload_image

### VARIABLES
# MAKE SURE THESE MATCH THE ONES IN image_maker.py 
PIXEL_LENGTH = 800 #Length and width of each cropped screenshot.
IMG_COUNTER = 10 # 2n - 1 = Number of rows and columns of images
pic_format = '.png' # Use png for 65500 pixel+ images

# Convert to positive indices
def pos_indices(int):
    return int + IMG_COUNTER - 1

# Create blank canvas for stitched image
total_widths = int((2 * IMG_COUNTER - 1) * PIXEL_LENGTH)
total_heights = int((2 * IMG_COUNTER - 1) * PIXEL_LENGTH)
final_img = Image.new('RGB', (total_widths, total_heights))

# Paste individual images onto canvas and delete
for i in range(-IMG_COUNTER+1, IMG_COUNTER):
    for j in range(-IMG_COUNTER+1, IMG_COUNTER):
        x = pos_indices(i)
        y = pos_indices(j)
        x_coord = int(PIXEL_LENGTH * x)
        y_coord = int(PIXEL_LENGTH * y)
        picstr = str(x) + ',' + str(y) + pic_format
        image = Image.open(picstr) 
        final_img.paste(image, (x_coord, y_coord))
        # os.remove(picstr)

final_img.save('./map/FULL_MAP' + pic_format)
upload_image.main('./map/FULL_MAP' + pic_format, '')