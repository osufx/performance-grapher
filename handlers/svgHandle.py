from helpers import sqlHelper
from objects import glob

def handle(id, mode):
    try:
        id = int(id)
    except Exception as e:
        return False, "ID has to be an integer!\nError: " + str(e)

    path = []

    sqlHelper.execute("SELECT rank, date FROM data WHERE user_id = 1076 ORDER BY date")
    rows = glob.sqlc.fetchall()
    date_start = rows[0]["date"]
    rank_start = rows[0]["rank"]
    view_middle = round(rank_start, -len(str(rank_start)) + 1)

    rank_highest = max([o["rank"] for o in rows])
    rank_lowest = min([o["rank"] for o in rows])

    view_highest = view_middle
    view_lowest = view_middle
    
    tmp_highest = view_highest
    while view_highest <= rank_highest:
        tmp_highest += round(rank_start, -len(str(rank_start)) + 2)
        view_highest = round(tmp_highest, -len(str(rank_start)) + 1)
    
    tmp_lowest = view_lowest
    while view_lowest >= rank_lowest:
        tmp_lowest -= round(rank_start, -len(str(rank_start)) + 2)
        view_lowest = round(tmp_lowest, -len(str(rank_start)) + 1)

    view_middle = round((view_highest + view_lowest) / 2, 0)

    for row in rows:
        x = (row["date"].day - date_start.day) * 24
        y = row["rank"] - rank_lowest
        path.append(x)
        path.append(y)
        row = glob.sqlc.fetchone()
    
    print("date_start: {}".format(date_start))
    print("rank_start: {}".format(rank_start))
    print("view_middle: {}".format(view_middle))
    print("rank_highest: {}".format(rank_highest))
    print("rank_lowest: {}".format(rank_lowest))
    print("view_highest: {}".format(view_highest))
    print("view_lowest: {}".format(view_lowest))
    print("path: {}".format(path))

    data = glob.svg_template.replace("{{PATH}}", ','.join(str(x) for x in [0,0, 20,20, 80,20]))
    return True, data