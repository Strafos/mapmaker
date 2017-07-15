# mapMaker
Scraps google maps to create high detail maps over a large area

map_maker is main the main function. For large maps, run image_maker then image_stitcher (equivalent of running map_maker)

Use image_cropper and fix_aspect_ratio to scale map to desired dimensions/area

For large maps with IMG_COUNTER > 30, it is recommended to use image_maker_BL/BR/TL/TR to divide the image scraping into separate programs to that run concurrently.  

Dependencies:
Pillow
Selenium
Google Drive python API 