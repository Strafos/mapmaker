# mapmaker
Scraps google maps to create high detail maps over a large area

## Dependencies:
Pillow (pip install Pillow)

Selenium (pip install selenium)

Google Drive python API (optional) (https://developers.google.com/drive/v3/web/quickstart/python)

## Run:
After downloading dependencies, run the main program `map_maker.py`

For large maps, it may be easier to run the main program in separate parts. For such cases, running
`image_maker.py` to generate map images and 
`image_stitch.py` to stitch map images together is equivalent

`image_cropper.py` and `fix_aspect_ratio.py` can be used to edit image to dimensional specifications

Another feature for large maps is `concurrent_image_maker.py` which splits the map up and generates constituant images faster. After images are generated, `image_sticher.py` can be used to create the full map.

## Examples:
