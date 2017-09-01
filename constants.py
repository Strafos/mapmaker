# VARIABLES 
# These values affect the view of the map
DESIRED_ZOOM = '21' # Zoom level of map. 2x zoom for each integer increment  
                    # No significant detail increase after zoom = 19
                    # Max zoom is 21
pic_format = '.png' # Use png for large images (pixel dimension > 65500)
IMG_COUNTER = 5 # Size of the map. Values < 5 will take less than a minute. 
                # For anything > 20, use concurrent_image_maker    
                

#CONSTANTS
# These values are needed for the program to work
# All constants were calibrated simultaneously. DON'T CHANGE THESE VALUES 
CALIBRATED_DPI = 120 # Base DPI, later scaled for current monitor
CALIBRATED_ZOOM = '19' #Zoom level for clear building outlines and street names
CALIBRATED_UNIT_X = 0.00171849462 #Coordinate equivalent of 800 x pixels at 19 zoom
CALIBRATED_ASPECT_RATIO = 1920 / 1080.0 #Resolution of computer (DO NOT CHANGE EVEN IF YOUR RESOLUTION DOES NOT MATCH)
MAP_URL = 'https://www.google.com/maps/@' #Base URL for google maps
PIXEL_LENGTH = 800 #Length and width of each cropped screenshot.