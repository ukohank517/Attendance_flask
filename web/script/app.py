# coding=utf-8
import os
from flask import Flask, Blueprint, jsonify, request, Response, render_template
import MySQLdb

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
    return error("msg")

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
    
    return render_template('event_entry.html', page_title = event_name, rest_seats=rest_seats)

@app.route('/event/entry', methods=['POST'])
def event_entry_post():
    namelist = request.form.getlist('name')
    tel = request.form['tel']
    email = request.form['email']
    comment = request.form['email']

    return "TODO: なんかのresultページ"

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

@app.route('/sample', methods=['GET'])
def hello():
    target_prefecture = request.args.get('pref')

    sql = "select * from personal_info;"
    rows = search_query(sql)

    result_dict = {}
    mail_address_list = []

    for row in rows:
        mail_add, sex, age, name, prefecture, insert_date, update_date = row
        if target_prefecture:
            if prefecture == target_prefecture:
                mail_address_list.append(mail_add)
        else:
            mail_address_list.append(mail_add)

    result_dict['mail_address_list'] = mail_address_list
    return jsonify(result_dict)

def error(msg):
    return render_template('error.html', page_title = 'unknown', msg = msg)

def search_query(sql):
    conn = MySQLdb.connect(user='root', passwd='pass', host='db_server', db='attendance')
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # 最終的にはここは消す。以下の手順でアプリケーションを起動する。
    # export FLASK_APP=app.py
    # flask run --host=0.0.0.0 --port=3000
