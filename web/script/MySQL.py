import MySQLdb

# 多分大丈夫ですが、一応sql injectionとxssを気をつけながらsqlを設置
class MySQL:

    def _open(self):
        self.conn = MySQLdb.connect(user='root', passwd='pass', host='db_server', db='attendance', charset='utf8')
        self.cur = self.conn.cursor()

    # event登録
    def event_insert(self, request):
        self._open()
        success_flag = True
        try:
            event_id = request.form['event_id']
            event_name = request.form['event_name']
            pswd = request.form['pswd']
            ticket_num = request.form['ticket_num']
            event_date = request.form['event_date']
            public_date = request.form['public_date']

            res = self.cur.execute("""
            INSERT INTO `event` (    event_id,     event_name,     pswd,     ticket_num,     event_date,     public_date)
                        VALUES  (%(event_id)s, %(event_name)s, %(pswd)s, %(ticket_num)s, %(event_date)s, %(public_date)s)
            """, {'event_id': event_id, 'event_name': event_name, 'pswd': pswd, 'ticket_num': ticket_num, 'event_date': event_date, 'public_date': public_date})
        except MySQLdb.Error as e:
            success_flag = False
            print('MySQLdb.Error: ', e)


        self.conn.commit()
        self.conn.close()

        return success_flag
    
    # injection対策のため、全部データ取って、サーバーで検索条件を実施
    # とりあえずリクエスト数多くないので。。
    def data_getter(self, sql):
        self._open()
        self.cur.execute(sql)
        return self.cur.fetchall()
