import svg_stack as ss
import svgwrite
import drawSvg as draw
import os

TRUNC_NUM_SVG_PATH = 'exhibitions/trunc_num.svg'

def place_directory_to_canvas(directory: str) -> None:
    doc = ss.Document()
    layout_ver = ss.VBoxLayout()
    file_names = [f for f in os.listdir(f'{directory}') if f.endswith('.svg')]

    for i, file_name in enumerate(file_names):
        if i % 10 == 0 and i != 0:
            layout_ver.addLayout(layout_hor)
        if i % 10 == 0:
            layout_hor = ss.HBoxLayout()
        layout_hor.addSVG(f'{directory}/{file_name}', alignment=ss.AlignTop|ss.AlignHCenter)

    doc.setLayout(layout_ver)
    doc.save(f'exhibitions/{directory.split("/")[-1]}.svg')

def create_exhibition_of_truncs(base_path: str, trunc_ext_list: list) -> None:
    doc = ss.Document()
    layout_ver = ss.VBoxLayout()

    for trunc_ext in trunc_ext_list:
        full_path = f'{base_path}_{trunc_ext}'
        file_names = [f for f in os.listdir(full_path) if f.endswith('.svg')]

        trunc_value = f'{str(float(trunc_ext)/10)}'
        layout_hor_trunc_num = ss.HBoxLayout()
        create_trunc_num_svg(path=TRUNC_NUM_SVG_PATH, trunc_value=trunc_value)
        layout_hor_trunc_num.addSVG(TRUNC_NUM_SVG_PATH, alignment=ss.AlignTop|ss.AlignHCenter)
        layout_ver.addLayout(layout_hor_trunc_num)

        layout_hor = ss.HBoxLayout()
        for i, file_name in enumerate(file_names):
            i += 1
            layout_hor.addSVG(f'{full_path}/{file_name}', alignment=ss.AlignTop|ss.AlignHCenter)
            if i % 20 == 0:
                layout_ver.addLayout(layout_hor)
                layout_hor = ss.HBoxLayout()

    doc.setLayout(layout_ver)
    doc.save(f'exhibitions/{base_path.split("/")[-1]}.svg')

def create_trunc_num_svg(path: str, trunc_value: str) -> None:
    d = draw.Drawing(512, 128, origin='center', displayInline=False)
    d.append(draw.Text(f'Threshold = {trunc_value}', 60, -250, -15, fill='black'))
    d.saveSvg(path)

if __name__ == '__main__':
    trunc_ext_list = ['0', '3', '5', '7', '10']
    base_path = 'outputs/output_thenounproject_standing_man'
    create_exhibition_of_truncs(base_path=base_path, trunc_ext_list=trunc_ext_list)

    '''directory = 'outputs/output_thenounproject_standing_man_5'
    place_directory_to_canvas(directory=directory)'''
