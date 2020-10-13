# coding=utf-8
import os
import MySQLdb
import random, string, textwrap, qrcode, hashlib
from flask import Flask, Blueprint, jsonify, request, Response, render_template
from MySQL import MySQL
from Mail import Mail
from environs import Env
from os import environ as osenv


db = MySQL()
mail = Mail()
env = Env()
app = Flask(__name__)
app.config['QRPATH'] = './script/static/img/qrcode/'

# from api import api

# flask_conf_file = os.path.join(os.getcwd(), 'conf', 'flask_conf.cfg')
# app.config.from_pyfile(flask_conf_file)
# mail_file = os.path.join(os.getcwd(), 'data', 'personal_info.csv')

@app.route('/')
def _top():
    return "カレンダー、イベント"

@app.route('/top')
def top():
    page_title = 'Top'
    return render_template('top.html', page_title = page_title)

@app.route('/event/list', methods=['GET'])
def event_list():
    # TODO: 自分が開催するイベントのみ表示
    sql = """
    SELECT
    event_id,
    event_name,
    DATE(event_date),
    (CASE WHEN CURRENT_TIMESTAMP() < public_date THEN '0'
          WHEN CURRENT_TIMESTAMP() < public_date THEN '2'
          ELSE '1'
    END) as public_status
    FROM
        event
    WHERE
        deleted = 0
    ORDER BY created_at DESC;
    """
    events = db.data_getter(sql)

    return render_template('event_list.html', page_title = 'イベント一覧', events = events)

@app.route('/event/detail', methods=['POST'])
def event_detail():
    rows = None

    event_id = request.form['event_id']
    token = request.form['token']
    hash_token = hashlib.md5(token.encode('utf-8')).hexdigest()
    sql = textwrap.dedent("""
            SELECT
                event_name
            FROM event
            WHERE
                event_id = '{event_id}'
                AND
                pswd = '{pswd}';
            """).format(event_id = event_id, pswd = hash_token)

    event_name = db.data_getter(sql)
    print(len(event_name))

    page_title = '参加者リスト'
    if len(event_name) == 1:
        sql = textwrap.dedent("""
                SELECT
                    ticket_id,
                    name,
                    memo
                FROM ticket
                WHERE event_id = '{event_id}'
                    AND deleted = 0
                ;
                """).format(event_id = event_id)
        rows = db.data_getter(sql)
        page_title = event_name[0][0]

    return render_template('event_detail.html', page_title = page_title, members = rows)

@app.route('/event/create', methods=['GET'])
def event_create_get():
    return render_template('event_create.html', page_title = 'イベント登録')

@app.route('/event/create', methods=['POST'])
def event_create_post():
    # TODO: validation: 
    event_id = randomToken(32)

    res = db.event_insert(request, event_id)
    if res:
        url = request.host_url + 'event/entry?event_id=' + event_id
        msg = textwrap.dedent("""
                <h1>!!!!!!!!!このページをメモってください!!!!!!!!!<h1>
                <br>
                イベントが作成されました： <br>
                下記のURLをコピーしてシェアしてください： <br>
                <h1> <a href= "{url}" >{url}</a> </h1>
            """).format(url = url)
        return result_page(msg)

    # 失敗した時
    return error_page("イベント生成に失敗しました。")

# イベントのチケットを発行するフォーム
@app.route('/event/entry', methods=['GET'])
def event_entry_get():
    sql = """
    SELECT
        E.event_id,
        E.event_name,
        E.ticket_num - ifnull(T.ticket_num, 0)
    FROM event E
    LEFT JOIN (
        SELECT
            event_id,
            count(*) AS ticket_num
        FROM ticket
        WHERE deleted = 0 
        GROUP BY event_id
    ) T    
    ON E.event_id = T.event_id
    WHERE CURRENT_TIMESTAMP() >= E.public_date;
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
        return error_page('イベント登録前orチケット在庫なし')
    
    return render_template('event_entry.html', page_title = event_name, rest_seats=rest_seats, event_id=event_id)

# イベントのチケットを発行する処理を行う
@app.route('/event/entry', methods=['POST'])
def event_entry_post():
    # TODO: validation: 

    family_id = randomToken(32)
    res = db.ticket_insert(request, family_id)

    # QRcode用
    event_id = request.form['event_id']
    data = request.host_url + 'ticket/result/edit?event_id=' + event_id + '&family_id=' + family_id
    foldername = event_id + '/'
    filename = family_id + '.png'

    qr_maker(data, foldername, filename)

    if res:
        msg = textwrap.dedent("""
                チケットがx枚予約しました<br>
                QRコードがこちら::<br>
                <p>
                <img src="/static/img/qrcode/{event_id}/{family_id}.png" alt="pic01">
                </p>
                予約内容がメールに送信しました。<br>
                受信が確認できない場合は開発者まで連絡してみてくださいね。<br>
            """).format(event_id = event_id ,family_id = family_id)
        HOST = osenv.get('GMAIL_HOST', default='none')
        USER = osenv.get('GMAIL_USER', default='none')
        PASS = osenv.get('GMAIL_PASS', default='none')
        from_addr = USER + '@gmail.com'
        to_addr = request.form['email']
        mail.send_mail(HOST, USER, PASS, from_addr, to_addr, "hello")
        return result_page(msg)

    # 失敗した時
    return error_page("チケット取得に失敗しました。再度登録してみてくださいmm")

# 取得チケットの情報を表示する
@app.route('/ticket/result/view', methods=['GET'])
def ticket_result_view():
    return ticket_detail(request, "view")

# 取得するチケットの情報を修正する(memo欄のみが修正できる)
@app.route('/ticket/result/edit', methods=['GET'])
def ticket_result_edit():
    return ticket_detail(request, "edit")

@app.route('/event/info', methods=['GET'])
def event_info():
    event_id = request.args.get('event_id')
    event_pswd = request.args.get('pswd')

    return 'event_idとpswdで、予約人間リストを表示する、セットがなければ404に飛ばす'

@app.route('/sendmail', methods=['GET'])
def sendmail():
    HOST = osenv.get('GMAIL_HOST', default='none')
    USER = osenv.get('GMAIL_USER', default='none')
    PASS = osenv.get('GMAIL_PASS', default='none')
    from_addr = USER + '@gmail.com'
    to_addr = 'ukohank517@gmail.com'
    mail.send_mail(HOST, USER, PASS, from_addr, to_addr, 'hello')
    return "success"

@app.errorhandler(404)
def error_404(er):
    return render_template('404.html', page_title = '404')

# @app.errorhandler(400)
# def error_400(e):
#     return error_page('必須パラメータが足りませんでしたね。')

# @app.errorhandler(500)
# def error_500(e):
#     return error_page('Internal Server Error')


def qr_maker(data, folder, filename):
    path = os.path.join(app.config['QRPATH'], folder)
    if not os.path.exists(path):
        os.makedirs(path)

    qr = qrcode.QRCode(box_size=5)
    qr.add_data(data)
    qr.make_image().save(os.path.join(path, filename)) 

def ticket_detail(request, action_type):
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
        return error_page('該当する情報が見つかりませんでした')
    
    return render_template('ticket_detail.html', page_title = 'Ticket', info=info, action_type=action_type)

def result_page(msg):
    return render_template('result.html', page_title = 'result', msg = msg)

def error_page(msg):
    return render_template('error.html', page_title = 'unknown', msg = msg)

# ランダム文字列
def randomToken(n):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

# API
@app.route('/ticket/result/update', methods=['POST'])
def ticket_result_update():    
    db.ticket_update(request)
    return jsonify(success=True)

# app.register_blueprint(api)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # 最終的にはここは消す。以下の手順でアプリケーションを起動する。
    # export FLASK_APP=app.py
    # flask run --host=0.0.0.0 --port=3000
