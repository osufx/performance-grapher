from objects import glob

def handle(id, mode):
    path = [0,0, 20,20, 80,20]

    data = glob.svg_template.replace("{{PATH}}", ','.join(str(x) for x in path))
    return data