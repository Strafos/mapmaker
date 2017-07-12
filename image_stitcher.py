from PIL import Image
import math
import os

PIXEL_LENGTH = 800 #Length and width of each cropped screenshot.
IMG_COUNTER = 2 # 2n - 1 = Number of rows and columns of images

# Create blank canvas for stitched image
total_widths = int((2 * IMG_COUNTER - 1) * PIXEL_LENGTH)
total_heights = int((2 * IMG_COUNTER - 1) * PIXEL_LENGTH)
final_img = Image.new('RGB', (total_widths, total_heights))

# Paste individual images onto canvas and delete
for i in range(-IMG_COUNTER+1, IMG_COUNTER):
    for j in range(-IMG_COUNTER+1, IMG_COUNTER):
        x = int(PIXEL_LENGTH * (i + IMG_COUNTER - 1))
        y = int(PIXEL_LENGTH * (j + IMG_COUNTER - 1))
        picstr = str(i) + ',' + str(j) + '.jpg'
        image = Image.open(picstr) 
        final_img.paste(image, (x, y))
        os.remove(picstr)

final_img.save('FULL_MAP.jpg')
