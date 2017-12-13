import pymysql
from objects import glob

def execute(sql, args=None):
    try:
        glob.sqlc.execute(sql, args) if args is not None else glob.sqlc.execute(sql)
        return glob.sqlc
    except pymysql.err.OperationalError:
        print ("Something went wrong with mysql connection.... trying to reconnect.")
        glob.sql.connect()
        return execute(sql, args)