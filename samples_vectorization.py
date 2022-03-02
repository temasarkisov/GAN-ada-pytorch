# python samples_vectorization_from_full.py  --output_dir=outputs/data/examples_abstract_logo_high_res 

import os
import re
import PIL.Image
import PIL.ImageOps
import argparse
import random
from svgpathtools import svg2paths
from os import listdir
from os.path import isfile, join

#--------------------------------------------------------------------------------------------------

class Samples_Vectorizator:
    def __init__(self, output_dir: str) -> None:
        self.output_dir = output_dir
        
    def vectorize_samples(self) -> None:
        try:
            os.makedirs(self.output_dir)
        except:
            print(f'Folder {self.output_dir} already exists')

        idx = 0
        IMAGES_PATH = 'data/examples_abstract_logo_high_res'
        file_paths = [join(IMAGES_PATH, f) for f in listdir(IMAGES_PATH) if isfile(join(IMAGES_PATH, f)) and (f.split(".")[1] == "png" or f.split(".")[1] == "jpg")]
        for file_name_png in file_paths:
            if self._is_bg_white(file_name_png):
                file_name_svg = self._png_to_svg(file_name_png)
                self._set_rnd_color(file_name_svg)

                if self._is_svg_not_empty(file_name_svg):
                    idx = idx + 1

            elif self._is_bg_black(file_name_png):
                image = PIL.Image.open(file_name_png).convert('RGB')
                image = PIL.ImageOps.invert(image).convert('LA')
                image.save(file_name_png)
                file_name_svg = self._png_to_svg(file_name_png)
                self._set_rnd_color(file_name_svg)

                if self._is_svg_not_empty(file_name_svg):
                    idx = idx + 1

            else:
                #os.remove(file_name_png)
                continue

    def _png_to_svg(self, file_name: str) -> None:
        pnm_name = file_name.split('.')[0] + '.pnm'
        svg_name = file_name.split('.')[0] + '.svg'

        try:
            os.system('convert %s %s' % (file_name, pnm_name))
            print(f'Convert {file_name} to {pnm_name} done')
        except:
            print(f'Convert {file_name} to {pnm_name} failed')

        try:
            os.system('potrace -s -o %s %s -u %s' % (svg_name, pnm_name, '1'))
            print(f'Potrace {pnm_name} to {svg_name} done')
        except:
            print(f'Potrace {pnm_name} to {svg_name} failed')

        os.remove(pnm_name)
        return svg_name

    def _is_svg_not_empty(self, file_name: str) -> None:
        try:
            f = open(file_name, 'r+')
            data = f.read()
        except:
            print(f'Can\'t open file - {file_name}')
            return False

        if (data.find('<path') == -1):
            return False

        return True

    def _resize_svg(self, file_name: str) -> None:
        try:
            file = open(file_name, 'r+')
            data = file.read()
        except:
            print(f'Can\'t open file - {file_name}')
            return

        data = data.replace('scale(1.000000,-1.000000)', 'scale(1.000000,1.000000)')
        file.seek(0)
        file.truncate(0)
        file.write(data)

    def _is_bg_white(self, file_name: str) -> bool:
        try:
            image = PIL.Image.open(file_name).convert('RGB')
        except:
            print(f'Can\'t open file - {file_name}')
            return False
        pixels = [i for i in image.getdata()]
        return (pixels[0] <= (255, 255, 255) and pixels[0] >= (240, 240, 240) and
                pixels[127] <= (255, 255, 255) and pixels[127] >= (240, 240, 240) and
                pixels[16256] <= (255, 255, 255) and pixels[16256] >= (240, 240, 240) and
                pixels[16383] <= (255, 255, 255) and pixels[16383] >= (240, 240, 240))

    def _is_bg_black(self, file_name: str) -> bool:
        try:
            image = PIL.Image.open(file_name).convert('RGB')
        except:
            print(f'Can\'t open file - {file_name}')
            return False
        pixels = [i for i in image.getdata()]
        return (pixels[0] >= (0, 0, 0) and pixels[0] <= (15, 15, 15) and
                pixels[127] >= (0, 0, 0) and pixels[127] <= (15, 15, 15) and
                pixels[16256] >= (0, 0, 0) and pixels[16256] <= (15, 15, 15) and
                pixels[16383] >= (0, 0, 0) and pixels[16383] <= (15, 15, 15))

    def _set_rnd_color(self, file_name: str) -> None:
        try:
            f = open(file_name, 'r+')
            data = f.read()
        except:
            print(f'Can\'t open file - {file_name}')
            return

        r = lambda: random.randint(0,255)
        fill_tag = re.search(r'fill=\S{9}', data)
        cur_color = fill_tag.group(0).split('"')[1]

        data = data.replace(f'fill="{cur_color}"', 'fill="#%02X%02X%02X"' % (r(),r(),r()))
        f.seek(0)
        f.truncate(0)
        f.write(data)

    def _get_paths_number(self, file_name: str) -> int:
        _, attributes = svg2paths(file_name)
        return len(attributes)

#--------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate samples using pretrained network pickle.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--output_dir', dest='output_dir', type=str, help='Where to save the output images', required=True, metavar='DIR')

    args = parser.parse_args()
    samples_gen = Samples_Vectorizator(**vars(args))
    samples_gen.vectorize_samples()
