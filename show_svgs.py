import svg_stack as ss
from os import listdir
from os.path import isfile, join

#--------------------------------------------------------------------------------------------------

def place_directory_to_canvas(directory: str) -> None:
    doc = ss.Document()
    layout_ver = ss.VBoxLayout()
    file_names = [f for f in listdir(directory) if isfile(join(directory, f)) and (f.split('.')[1] == 'svg')] 

    for i, file_name in enumerate(file_names):
        if i % 20 == 0 and i != 0:
            #doc.setLayout(layout_hor)
            #doc.save(f"exhibitions/{i}_{directory.split('/')[-1]}.svg")
            layout_ver.addLayout(layout_hor)
        if i % 20 == 0:
            layout_hor = ss.HBoxLayout()
        layout_hor.addSVG(f"{directory}/{file_name}", alignment=ss.AlignTop|ss.AlignHCenter)

    doc.setLayout(layout_ver)
    doc.save(f'{directory.split("/")[-1]}.svg')

#--------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    place_directory_to_canvas(directory='../Ironov-Vectorizer-unit/data/abstract_logos')
