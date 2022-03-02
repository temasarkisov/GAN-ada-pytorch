import numpy as np
import PIL.Image
import os


def l1_compare_images(img1, img2):
    return np.mean(np.abs(img1 - img2))

if __name__ == '__main__':
    PATH_TO_REAL_IMGS = '/raid/asarkisov/MyProjects/stylegan2-ada/data/thenounproject_kettle'
    real_img_file_names = [f for f in os.listdir(PATH_TO_REAL_IMGS) if os.path.isfile(os.path.join(PATH_TO_REAL_IMGS, f)) and f.split(".")[1] == "png"]
    
    img2_path = '/raid/asarkisov/MyProjects/stylegan2-ada-pytorch/outputs/output_thenounprojec_gamepad/sample-16.png'
    img2 = np.asarray([pixel for pixel in PIL.Image.open(img2_path).convert('RGB').getdata()])

    l1_min = float('inf')
    result_file_name = ''

    for i, real_img_file_name in enumerate(real_img_file_names):
        img1_path = f'{PATH_TO_REAL_IMGS}/{real_img_file_name}'    
        img1 = np.asarray([pixel for pixel in PIL.Image.open(img1_path).convert('RGB').getdata()])
        
        l1_cur = l1_compare_images(img1, img2)
        if l1_cur < l1_min:
            l1_min = l1_cur
            result_file_name = real_img_file_name
        
        print(f'{i}/{len(real_img_file_names)}')

    print(f'{result_file_name} with l1 value = {l1_min}')
