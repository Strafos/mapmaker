from PIL import Image
import math

img = Image.open('FULL_MAP.jpg')

ratio = input('Enter desired aspect ratio (ex. 4:3): \n')
idx = ratio.find(':')
height = float(ratio[0:idx])
width = float(ratio[idx + 1: ])

if height > width:
    width = width / height
    height = 1.0
else:
    height = height / width
    width = 1.0

img_width, img_height = img.size
half_width = img_width / 2
half_height = img_height / 2

new_width = img_width * width
new_height = img_height * height

img = img.crop(
    (
        half_width - new_width / 2,
        half_height - new_height / 2,
        half_width + new_width / 2,
        half_height + new_height / 2
    )
)

img.save('croppedMap.jpg')