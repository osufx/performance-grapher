from flask import Flask, render_template, make_response, redirect, request
import ssl
import json
import pymysql

from objects import glob
from handlers import svgHandle

with open("config.json", "r") as f:
    config = json.load(f)

app = Flask(__name__)

@app.route('/svg/<id>')
@app.route('/svg/<id>/<mode>')
def svg(id, mode=0):
    if not isinstance(mode, int):
        mode = 0
    else:
        if mode > 3 or mode < 0:
            mode = 0

    is_valid, data = svgHandle.handle(id, mode)

    if is_valid:
        headers = {'Content-type': 'image/svg+xml'}
    else:
        headers = {'Content-type': 'raw'}
    return data, 200, headers

if __name__ == "__main__":
    with open("template.svg", "r") as f:
        glob.svg_template = f.read()

    glob.sql = pymysql.connect(host=config['sql_host'], user=config['sql_usr'], passwd=config['sql_psw'], db=config['sql_db'], charset='utf8')
    glob.sql.autocommit(True)
    glob.sqlc = glob.sql.cursor(pymysql.cursors.DictCursor)

    if config["ssl"]:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain('host.crt', 'host.key')
        app.run(debug=config["debug"], port=config["port"], ssl_context=context, threaded=True, host='0.0.0.0')
    else:
        app.run(debug=config["debug"], port=config["port"], threaded=True, host='0.0.0.0')