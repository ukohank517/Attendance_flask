# coding=utf-8
import os
from flask import Flask, Blueprint, jsonify, request, render_template
import MySQLdb

app = Flask(__name__)
flask_conf_file = os.path.join(os.getcwd(), 'conf', 'flask_conf.cfg')
app.config.from_pyfile(flask_conf_file)
mail_file = os.path.join(os.getcwd(), 'data', 'personal_info.csv')


@app.route('/event/info', methods=['GET'])
def info():
    event_id = request.args.get('event_id')
    event_pswd = request.args.get('pswd')

    return 'event_idとpswdで、予約人間リストを表示する、セットがなければ404に飛ばす'

@app.route('/event/entry', methods=['GET'])
def test():
    target_organization = request.args.get('organization_id')
    event_name = '常年期第x回弥撒'
    rest_seats = 10
    return render_template('entry.html', rest_seats=rest_seats, event_name = event_name)

@app.route('/event/result', methods=['GET'])
def result():
    event_id = request.args.get('event_id')
    famali_id = request.args.get('famali_id')
    return '詳細ページ表示、QRコードがここで表示する'

@app.route('/event/result/edit', methods=['GET'])
def result_edit():
    return 'memo欄に登録する'

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
