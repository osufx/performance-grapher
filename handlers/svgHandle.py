from objects import glob

def handle(id, mode):
    try:
        id = int(id)
    except Exception as e:
        return False, "ID has to be an integer!\nError: " + str(e)

    path = [0,0, 20,20, 80,20]

    data = glob.svg_template.replace("{{PATH}}", ','.join(str(x) for x in path))
    return True, data