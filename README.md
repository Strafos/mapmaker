# mapmaker
Scraps google maps to create high detail maps over a large area

## Dependencies:
Pillow (pip install Pillow)
Selenium (pip install selenium)
Google Drive python API (optional) (installation explained later)

## Run:
After downloading dependencies, run the main program `map_maker.py`
For large maps, it may be easier to run the main program in separate parts. For such cases, running
`image_maker.py` to generate map images and 
`image_stitch.py` to stitch map images together is equivalent

`image_cropper.py` and `fix_aspect_ratio.py` can be used to edit image to dimensional specifications

For large maps with IMG_COUNTER > 30, it is recommended to use image_maker_BL/BR/TL/TR to divide the image scraping into separate programs to that run concurrently.  