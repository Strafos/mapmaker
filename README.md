# mapmaker
Scraps google maps to create high detail maps over a large area

## Intro:
Ever since middle school, I've done a lot of exploring. By senior year of high school, I knew my town really well. In fact, as I had realized, I knew it better than google maps, or any map for that matter - I knew all these shortcuts and hidden paths that you wouldn't find on a conventional map. But, I knew that when I went off to college, I would invariably forget all this. Thus began my first map project - I took screenshots of Google maps and stitched them together manually. A painstaking process that wasn't particularly accurate, but it worked! I had to do the last few operations on my friend's gaming computer because mine couldn't handle the image sizes. I printed out my map on a large 4'x4' poster and annotated it with the culmination of everything I discovered in my years in Plainsboro. It remains my most prized possession.

mapmaker is a revisit to the same problem. I decided to build a program so I could create a map for where ever my life would lead me. When zoomed out, google maps provides a map over a large area with low detail. Zoomed in, the map is high detail over small area. To create a large map with high detail, the program iterates through thousands of zoomed in map pieces and stitches them together into one giant map.

## Examples:
Ithaca map (Low quality, had to be resized to upload to imgur)
![map](https://i.imgur.com/2yYDQFh.jpg)

Map of Ithaca printed out on 4'x8' banner
![Ithaca Map](https://i.imgur.com/xKy0zNT.jpg)

Full map file: https://drive.google.com/open?id=0B0lHgBCriwW_bWlSaXY2NmZxME0

This file is very large and may crash your computer (it crashes mine) Please be careful when you open it. 

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

