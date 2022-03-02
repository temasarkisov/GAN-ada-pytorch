import os
from svgpathtools import svg2paths
from os import listdir
from os.path import isfile, join
import PIL.Image

#--------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    IMAGES_PATH = 'data/examples_abstract_logo_high_res'
    file_paths = [join(IMAGES_PATH, f) for f in listdir(IMAGES_PATH) if isfile(join(IMAGES_PATH, f)) and (f.split(".")[1] == "png" or f.split(".")[1] == "jpg")]
    for file_path_png in file_paths:
        image = PIL.Image.open(file_path_png)
        image.save(file_path_png.replace(' ', '_'))
        os.remove(file_path_png)
    
