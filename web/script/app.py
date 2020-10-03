# coding=utf-8
import os
from flask import Flask, Blueprint, jsonify, request, Response, render_template
import MySQLdb
import random, string

from MySQL import MySQL

db = MySQL()
app = Flask(__name__)

flask_conf_file = os.path.join(os.getcwd(), 'conf', 'flask_conf.cfg')
app.config.from_pyfile(flask_conf_file)
mail_file = os.path.join(os.getcwd(), 'data', 'personal_info.csv')

@app.route('/')
@app.route('/top')
def top():
    page_title = 'Top'
    return render_template('top.html', page_title = page_title)

@app.route('/event/create', methods=['GET'])
def event_create_get():
    return render_template('event_create.html', page_title = 'イベント登録')

@app.route('/event/create', methods=['POST'])
def event_create_post():
    # TODO: validation: 
    res = db.event_insert(request)
    if res:
        return "TODO: なんかのresultページ"

    # 失敗した時
    return error("イベント生成に失敗しました。")

@app.route('/event/entry', methods=['GET'])
def event_entry_get():
    sql = """
    SELECT 
        E.event_id, 
        E.event_name, 
        (E.ticket_num - count(*)) as rest_seats
    FROM event E 
    JOIN ticket T
    ON E.event_id = T.event_id 
    WHERE T.deleted = 0 AND CURRENT_TIMESTAMP() >= public_date
    GROUP BY event_id;
    """
    rows = db.data_getter(sql)

    event_id = request.args.get('event_id')
    event_name = ""
    rest_seats = 0
    for row in rows:
        id, name, num =  row
        if id == event_id:
            event_name = name
            rest_seats = num

    if rest_seats <= 0:
        return error('イベント登録前orチケット在庫なし')
    
    return render_template('event_entry.html', page_title = event_name, rest_seats=rest_seats, event_id=event_id)

@app.route('/event/entry', methods=['POST'])
def event_entry_post():
    # TODO: validation: 

    family_id = randomToken(32)
    res = db.ticket_insert(request, family_id)
    if res:
        return "TODO: なんかのresultページ"

    # 失敗した時
    return error("チケット取得に失敗しました。再度登録してみてくださいmm")

@app.route('/event/result', methods=['GET'])
def event_result():
    event_id = request.args.get('event_id')
    famali_id = request.args.get('famali_id')
    return '詳細ページ表示、QRコードがここで表示する'

@app.route('/event/result/edit', methods=['GET'])
def event_result_edit():
    return 'memo欄に登録する'

@app.route('/event/info', methods=['GET'])
def event_info():
    event_id = request.args.get('event_id')
    event_pswd = request.args.get('pswd')

    return 'event_idとpswdで、予約人間リストを表示する、セットがなければ404に飛ばす'

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html', page_title = '404')

def error(msg):
    return render_template('error.html', page_title = 'unknown', msg = msg)

def search_query(sql):
    conn = MySQLdb.connect(user='root', passwd='pass', host='db_server', db='attendance')
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

# ランダム文字列
def randomToken(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # 最終的にはここは消す。以下の手順でアプリケーションを起動する。
    # export FLASK_APP=app.py
    # flask run --host=0.0.0.0 --port=3000
