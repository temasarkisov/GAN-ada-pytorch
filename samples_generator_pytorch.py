# python samples_generator_pytorch.py --num_to_gen=100 --network_pkl=training-runs/00058-dataset_thenounproject_t_shirt_inverted-auto2/network-snapshot-012096.pkl --output_dir=outputs/output_t_shirt_0_7 --trunc=0.7
# python samples_generator_pytorch.py --num_to_gen=100 --network_pkl=training-runs/00054-dataset_thenounproject_envelope_inverted-auto2/network-snapshot-025000.pkl --output_dir=outputs/output_envelope_1_0 --trunc=1

# python samples_generator_pytorch.py --num_to_gen=100 --network_pkl=training-runs/00051-dataset_nude-painting-nu-auto4/network-snapshot-009600.pkl --output_dir=outputs/output_nude_painting --trunc=0.5

import os
import re
import dnnlib
import numpy as np
import PIL.Image
import PIL.ImageOps
import torch
import legacy
import argparse
import random
from svgpathtools import svg2paths

#--------------------------------------------------------------------------------------------------

MODELS_TO_CHECK_PATHS_NUM = ['../models/LLD-res128-aug-network-snapshot-015974.pkl']

MODELS_TO_ROTATE_90 = ['../models/thenounproject_hand_res128_aug_network-snapshot-025000.pkl', 
                    '../models/thenounproject_suitcase_res128_aug_network-snapshot-025000.pkl', 
                    '../models/thenounproject_wine_glass_res128_aug_network-snapshot-023788.pkl',
                    '../models/thenounproject_smile_emoji_res128_aug_network-snapshot-019958.pkl',
                    '../models/thenounproject_pistol_res128_aug_network-snapshot-025000.pkl',
                    '../models/thenounproject_moon_res128_aug_network-snapshot-025000.pkl',
                    '../models/thenounproject_paint_roller_res128_aug_network-snapshot-023385.pkl',
                    ]

MODELS_TO_ROTATE_180 = ['../models/thenounproject_standing_man_res128_aug_network-snapshot-003225.pkl',
                    '../models/thenounproject_lion_face_res128_aug_network-snapshot-011289.pkl',
                    ]

#--------------------------------------------------------------------------------------------------

class Samples_Generator:
    def __init__(self, num_to_gen: int, network_pkl: str, truncation_psi: float, class_idx: int, noise_mode: str, output_dir: str) -> None:
        self.num_to_gen = num_to_gen
        self.network_pkl = network_pkl
        self.output_dir = output_dir
        if truncation_psi is not None:
            self.truncation_psi = truncation_psi
        if class_idx is not None:
            self.class_idx = class_idx
        else:
            self.class_idx = None
        if noise_mode is not None:
            self.noise_mode = noise_mode
        else:
            self.noise_mode = 'const'

    def generate_samples(self, mode='nomode') -> None:
        print('Loading networks from "%s"...' % self.network_pkl)
        device = torch.device('cuda')
        with dnnlib.util.open_url(self.network_pkl) as f:
            G = legacy.load_network_pkl(f)['G_ema'].to(device) # type: ignore

        try:
            os.makedirs(self.output_dir)
        except:
            print(f'Folder {self.output_dir} already exists')

        label = torch.zeros([1, G.c_dim], device=device)
        if G.c_dim != 0:
            if self.class_idx is None:
                label[:, self.class_idx] = 1
        else:
            if self.class_idx is not None:
                print('warn: --class=lbl ignored when running on an unconditional network')

        idx = 0
        while idx < self.num_to_gen:
            print('Generating image for index %d (%d/%d) ...' % (idx, idx, self.num_to_gen - 1))
            file_name_png = self.output_dir + '/sample-' + str(idx) + '.png'

            rnd_seed = np.random.randint(0, 100000)
            z = torch.from_numpy(np.random.RandomState(rnd_seed).randn(1, G.z_dim)).to(device)
            img = G(z, label, truncation_psi=self.truncation_psi, noise_mode=self.noise_mode)
            img = (img.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)
            
            img = img[0].cpu().numpy()
            if img.shape[2] == 1:
                img = np.reshape(img, (128, 128))
                mode = 'L'
            elif img.shape[2] == 3:
                mode = 'RGB'

            if self.network_pkl in MODELS_TO_ROTATE_90:
                img = PIL.Image.fromarray(img, mode=mode).rotate(-90)
            elif self.network_pkl in MODELS_TO_ROTATE_180:
                img = PIL.Image.fromarray(img, mode=mode).rotate(-180)
            else:
                img = PIL.Image.fromarray(img, mode=mode)
            img = img.save(file_name_png)

            if self._is_bg_white(file_name_png):
                file_name_svg = self._png_to_svg(file_name_png)
                self._set_rnd_color(file_name_svg)

                if self._is_svg_not_empty(file_name_svg):
                    if (self.network_pkl in MODELS_TO_CHECK_PATHS_NUM and self._get_paths_number(file_name_svg) <= 1) or (self.network_pkl not in MODELS_TO_CHECK_PATHS_NUM):
                        file_name_z = file_name_png.split('.')[0] + '-z.txt'
                        z_file = open(file_name_z, 'w')
                        z_file.write(str(z))
                        idx = idx + 1

            elif self._is_bg_black(file_name_png):
                image = PIL.Image.open(file_name_png).convert('RGB')
                image = PIL.ImageOps.invert(image).convert('LA')
                image.save(file_name_png)
                file_name_svg = self._png_to_svg(file_name_png)
                self._set_rnd_color(file_name_svg)

                if self._is_svg_not_empty(file_name_svg):
                    if (self.network_pkl in MODELS_TO_CHECK_PATHS_NUM and self._get_paths_number(file_name_svg) <= 1) or (self.network_pkl not in MODELS_TO_CHECK_PATHS_NUM):
                        file_name_z = file_name_png.split('.')[0] + '-z.txt'
                        z_file = open(file_name_z, 'w')
                        z_file.write(str(z))
                        idx = idx + 1

            else:
                os.remove(file_name_png)

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

def _parse_num_range(s):
    range_re = re.compile(r'^(\d+)-(\d+)$')
    m = range_re.match(s)
    if m:
        return list(range(int(m.group(1)), int(m.group(2))+1))
    vals = s.split(',')
    return [int(x) for x in vals]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate samples using pretrained network pickle.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--num_to_gen', dest='num_to_gen', type=int, help='Number of samples to generate', required=True)
    parser.add_argument('--network_pkl', help='Network pickle filename', dest='network_pkl', required=True)
    parser.add_argument('--trunc', dest='truncation_psi', type=float, help='Truncation psi (default: %(default)s)', default=0.5, required=False)
    parser.add_argument('--class_idx', dest='class_idx', type=int, help='Class label (default: unconditional)', required=False)
    parser.add_argument('--noise_mode', dest='noise_mode', type=str, default='random', help='Noise mode (default: random)', required=False)
    parser.add_argument('--output_dir', dest='output_dir', type=str, help='Where to save the output images', required=True, metavar='DIR')

    args = parser.parse_args()
    samples_gen = Samples_Generator(**vars(args))
    samples_gen.generate_samples(mode='nomode')
