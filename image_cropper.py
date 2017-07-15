from PIL import Image
import math

img = Image.open('croppedMap.8.jpg')

img_width, img_height = img.size
half_width = img_width / 2
half_height = img_height / 2

new_width = img_width * .6
new_height = img_height * .6

img = img.crop(
    (
        half_width - new_width / 2,
        half_height - new_height / 2,
        half_width + new_width / 2,
        half_height + new_height / 2
    )
)

img.save('croppedMap.jpg')