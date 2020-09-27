# coding=utf-8
import os
from flask import Flask, Blueprint, jsonify, request, render_template
import MySQLdb

app = Flask(__name__)
flask_conf_file = os.path.join(os.getcwd(), 'conf', 'flask_conf.cfg')
app.config.from_pyfile(flask_conf_file)
mail_file = os.path.join(os.getcwd(), 'data', 'personal_info.csv')


@app.route('/event/entry', methods=['GET'])
def test():
    target_organization = request.args.get('organization_id')
    rest_seats = 10
    return render_template('entry.html', rest_seats=rest_seats)

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
