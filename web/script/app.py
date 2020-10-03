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

# イベントのチケットを発行するフォーム
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
        id, name, num = row
        if id == event_id:
            event_name = name
            rest_seats = num

    if rest_seats <= 0:
        return error('イベント登録前orチケット在庫なし')
    
    return render_template('event_entry.html', page_title = event_name, rest_seats=rest_seats, event_id=event_id)

# イベントのチケットを発行する処理を行う
@app.route('/event/entry', methods=['POST'])
def event_entry_post():
    # TODO: validation: 

    family_id = randomToken(32)
    res = db.ticket_insert(request, family_id)
    if res:
        return "TODO: チケットのresultページ"

    # 失敗した時
    return error("チケット取得に失敗しました。再度登録してみてくださいmm")

# 取得チケットの情報を表示する
@app.route('/ticket/result', methods=['GET'])
def ticket_result():
    aim_event_id = request.args.get('event_id')
    aim_family_id = request.args.get('family_id')

    sql="""
        SELECT
            event_id,
            family_id,
            ticket_id,
            CONCAT('**', right(name, 1)) as name,
            CONCAT( left(phone_number, 3),  '****', RIGHT(phone_number, 4)) as tel,
            CONCAT( left(email, 4), '****' ) as email,
            comment,
            memo
        FROM ticket WHERE deleted = FALSE;
    """
    rows = db.data_getter(sql)

    info = {}
    info['tel'] = ''
    info['email'] = ''
    info['comment'] = ''
    info['user_list'] = []

    for row in rows:
        _event_id, _family_id, _ticket_id, _name, _tel, _email, _comment, _memo = row
        if (_event_id == aim_event_id) and (_family_id == aim_family_id):
            info['tel'] = _tel
            info['email'] = _email
            info['comment'] = _comment
            user = {}
            user['name'] = _name
            user['memo'] = _memo
            user['ticket_id'] = _ticket_id
            info['user_list'].append(user)

    if len(info['user_list']) <= 0 :
        return error('該当する情報が見つかりませんでした')
    
    return render_template('ticket_detail.html', page_title = 'Ticket', info=info)

# 取得するチケットの情報を修正する(memo欄のみが修正できる)
@app.route('/ticket/result/edit', methods=['GET'])
def ticket_result_edit():
    aim_event_id = request.args.get('event_id')
    aim_family_id = request.args.get('family_id')
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
