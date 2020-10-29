import MySQLdb

# 多分大丈夫ですが、一応sql injectionとxssを気をつけながらsqlを設置
class MySQL:

    def _open(self):
        self.conn = MySQLdb.connect(user='root', passwd='pass', host='db_server', db='attendance', charset='utf8')
        self.cur = self.conn.cursor()

    # event登録
    def event_insert(self, request, event_id):
        self._open()
        try:
            event_name = request.form['event_name']
            pswd = request.form['pswd']
            ticket_num = request.form['ticket_num']
            event_date = request.form['event_date']
            public_date = request.form['public_date']

            res = self.cur.execute("""
            INSERT INTO `event` (    event_id,     event_name,     pswd,     ticket_num,     event_date,     public_date)
                        VALUES  (%(event_id)s, %(event_name)s, MD5(%(pswd)s), %(ticket_num)s, %(event_date)s, %(public_date)s);
            """, {'event_id': event_id, 'event_name': event_name, 'pswd': pswd, 'ticket_num': ticket_num, 'event_date': event_date, 'public_date': public_date})
        except MySQLdb.Error as e:            
            print('MySQLdb.Error: ', e)
            return False


        self.conn.commit()
        self.conn.close()

        return True

    # チケット登録
    def ticket_insert(self, request, family_id):        
        # TODO: event_idに対するfamily_idが既に存在してるのであれば、失敗して返す
        namelist = request.form.getlist('name')
        event_id = request.form['event_id']
        phone_number = request.form['phone_number']
        email = request.form['email']
        comment = request.form['comment']

        self._open()
        for name in namelist:
            try:
                res = self.cur.execute("""
                    INSERT INTO `ticket` (ticket_id, event_id, name, phone_number, email, family_id, comment, memo)
                    VALUES
                    (
                        /***** (last ticket_id) + 1 *****/
                        (select ifnull(lst_id, 0) + 1 
                            from
                        (select max(ticket_id) as lst_id from ticket where event_id = %(event_id)s) TB ),
                        /********************************/   
                        %(event_id)s, %(name)s, %(phone_number)s, %(email)s, %(family_id)s, %(comment)s, '');
                """, {'event_id': event_id, 'name': name, 'phone_number': phone_number, 'email': email, 'family_id': family_id, 'comment': comment})
            except MySQLdb.Error as e:
                print('MySQLdb.Error: ', e)
                return False
        
        self.conn.commit()
        self.conn.close()

        return True

    def ticket_update(self, request):
        event_id = request.get_json()['event_id']
        json_list = request.get_json()['ticket_memo_list']

        self._open()
        for json in json_list:
            try:
                memo = json['memo']
                ticket_id = json['ticket_id']

                res = self.cur.execute("""
                UPDATE ticket SET memo = %(memo)s WHERE event_id = %(event_id)s AND ticket_id = %(ticket_id)s;
                """, {'event_id': event_id, 'ticket_id': ticket_id, 'memo': memo})
            except MySQLdb.Error as e:
                print('Mysqldb.Error: ', e)
                return False

        self.conn.commit()
        self.conn.close()

        return True

    
    # injection対策のため、全部データ取って、サーバーで検索条件を実施
    # とりあえずリクエスト数多くないので。。
    def data_getter(self, sql):
        self._open()
        self.cur.execute(sql)
        return self.cur.fetchall()

    
