from helpers import sqlHelper
from objects import glob

def handle(id, mode):
    try:
        id = int(id)
    except Exception as e:
        return False, "ID has to be an integer!\nError: " + str(e)

    path = []

    #sqlHelper.execute("SELECT rank, date FROM data WHERE user_id = {} AND date BETWEEN DATE_SUB(NOW(), INTERVAL 30 DAY) AND NOW() ORDER BY date".format(id))
    sqlHelper.execute("SELECT rank, date FROM data WHERE user_id = {} ORDER BY date".format(id))
    rows = glob.sqlc.fetchall()

    if len(rows) == 0:
        return False, "No data found for {}".format(id)

    date_start = rows[0]["date"]
    rank_start = rows[0]["rank"]
    view_middle = round(rank_start, -len(str(rank_start)) + 1)

    rank_highest = max([o["rank"] for o in rows])
    rank_lowest = min([o["rank"] for o in rows])

    view_highest = view_middle
    view_lowest = view_middle
    
    tmp_highest = view_highest
    while view_highest <= rank_highest:
        tmp_highest += round(rank_start, -len(str(rank_start)) + 2)/10
        view_highest = round(tmp_highest, -len(str(rank_start)) + 1)
    
    tmp_lowest = view_lowest
    while view_lowest >= rank_lowest:
        tmp_lowest -= round(rank_start, -len(str(rank_start)) + 2)/10
        view_lowest = round(tmp_lowest, -len(str(rank_start)) + 1)

    view_middle = round((view_highest + view_lowest) / 2, 0)

    #Make into ints
    view_highest = int(view_highest)
    view_middle = int(view_middle)
    view_lowest = int(view_lowest)

    for row in rows:
        x = (row["date"].timestamp() - date_start.timestamp()) * 0.000141
        y = (row["rank"] - view_lowest) * 0.1
        path.append(x)
        path.append(y)

    #Shift path X axis
    count = int(len(path) / 2)
    shift = 30 - count
    x = 0

    #while x < len(path):
    #    path[x] += (720 - shift * 6)
    #    x += 2
    
    print("date_start: {}".format(date_start))
    print("rank_start: {}".format(rank_start))
    print("view_middle: {}".format(view_middle))
    print("rank_highest: {}".format(rank_highest))
    print("rank_lowest: {}".format(rank_lowest))
    print("view_highest: {}".format(view_highest))
    print("view_lowest: {}".format(view_lowest))
    print("path: {}".format(path))


    svg_path = []
    svg_path.append("M0")
    svg_path.append(str(path[1]))
    if len(path) <= 4:
        #We dont have enough points to start curving
        svg_path.append(str(path[0]))
        svg_path.append(str(path[1]))
        if len(path) == 4:
            svg_path.append(str(path[2]))
            svg_path.append(str(path[3]))
    else:
        #We can start curving paths
        i = 2
        while i < len(path) - 3:
            x = "C" + str(path[i])
            y = str(path[i + 1])

            svg_path.append(x)
            svg_path.append(y)

            #X axis
            xQ1 = (path[i] + path[i + 2]) / 2
            xQ0 = (xQ1 + path[i]) / 2
            xQ2 = (xQ1 + path[i + 2]) / 2

            #Y axis
            yQ1 = (path[i + 1] + path[i + 3]) / 2
            #yQ0 = (yQ1 + path[i + 1]) / 2
            #yQ2 = (yQ1 + path[i + 3]) / 2

            svg_path += [str(xQ0), y, str(xQ1), str(yQ1), str(xQ1), str(yQ1), str(xQ2), str(path[i + 3])] + [str(path[i + 2]), str(path[i + 3])]

            i += 2

    print("svg_path: {}".format(svg_path))
    
    data = glob.svg_template.replace("{{PATH}}", ','.join(svg_path))
    data = data.replace("{{VIEW_LOWEST}}", str(view_lowest)).replace("{{VIEW_MIDDLE}}", str(view_middle)).replace("{{VIEW_HIGHEST}}", str(view_highest))
    return True, data