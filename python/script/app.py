# coding=utf-8
import os
from flask import Flask, jsonify, request
import MySQLdb

app = Flask(__name__)
flask_conf_file = os.path.join(os.getcwd(), 'conf', 'flask_conf.cfg')
app.config.from_pyfile(flask_conf_file)
mail_file = os.path.join(os.getcwd(), 'data', 'personal_info.csv')


@app.route('/', methods=['GET'])
def hello():
    target_prefecture = request.args.get('pref')

    conn = MySQLdb.connect(user='root', passwd='pass', host='db_server', db='testdb')
    cur = conn.cursor()
    sql = "select * from personal_info;"
    cur.execute(sql)
    rows = cur.fetchall()

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # 最終的にはここは消す。以下の手順でアプリケーションを起動する。
    # export FLASK_APP=app.py
    # flask run --host=0.0.0.0 --port=3000
