import psycopg2
import logging


# 创建表
class Store:
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = '5432'
        self.user = 'postgres'
        self.password = 'tqy020107'
        self.database = 'cdms2022'
        self.init_tables()


    def fetch_all_db(self):
        conn = self.get_db_conn()
        sql = 'select current_database();'
        # 执行SQL
        conn.execute(sql)
        # SQL执行后，会将结果以元组的形式缓存在cursor中，使用下述语句输出
        for tuple in conn.fetchall():
            print(tuple)

    def get_db_conn(self):
        self.con = psycopg2.connect(host=self.host, port=self.port, user=self.user,
                                    password=self.password, database=self.database)
        autocommit = psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
        self.con.set_isolation_level(autocommit)
        return self.con.cursor()

    def init_tables(self):
        try:
            conn = self.get_db_conn()
        except psycopg2.DatabaseError as e:
            print(e)
        try:
            conn.execute(
                'CREATE TABLE IF NOT EXISTS User1('
                'user_id TEXT PRIMARY KEY,'  # 用户名
                'password TEXT ,'  # 密码
                'balance INTEGER,'  # 余额
                'token TEXT,'  # token
                'terminal TEXT'  # 端口
                ')'
            )

            conn.execute(
                'CREATE TABLE IF NOT EXISTS Book( '
                'book_id TEXT PRIMARY KEY,'  # 书本编号
                'title TEXT,'  # 书名
                'author TEXT,'  # 书本信息
                'publisher TEXT,'
                'original_title TEXT,'
                'translator TEXT,'
                'pub_year TEXT,'
                'pages INTEGER,'
                'price INTEGER,'
                'currency_unit TEXT,'
                'binding TEXT,'
                'isbn TEXT,'
                'author_intro TEXT,'
                'book_intro text,'
                'content TEXT,'
                'tags TEXT,'
                'picture BYTEA'
                ')'
            )

            conn.execute(
                'CREATE TABLE IF NOT EXISTS Store('
                'store_id INTEGER PRIMARY KEY,'  # 店铺编号
                'owner TEXT UNIQUE,'  # 卖家user_id
                'FOREIGN KEY(owner) REFERENCES User1(user_id)'
                ')'
            )

            conn.execute(
                'CREATE TABLE IF NOT EXISTS Books_in_store( '
                'store_id INTEGER,'  # 店铺编号
                'book_id TEXT,'  # 书本编号
                'book_name TEXT,'  # 书名
                'book_num INTEGER,'  # 在售数量，完成一次订单后数量-1
                'FOREIGN KEY(store_id) REFERENCES Store(store_id),'
                'FOREIGN KEY(book_id) REFERENCES Book(book_id),'
                # 'FOREIGN KEY(book_name) REFERENCES Book(title),'
                'PRIMARY KEY(store_id, book_id)'
                ')'
            )

            conn.execute(
                'CREATE TABLE IF NOT EXISTS Orders( '
                'order_id INTEGER PRIMARY KEY,'  # 订单编号
                'seller TEXT,'  # 卖家
                'buyer TEXT,'  # 买家
                'status INTEGER,'  # 0为未付款（*这里可以不要 如果我们后面写的是点击购买后直接扣款就直接进入状态1），
                # 1为以付款未发货（买家付款后，商家填入物流前），
                # 2为已发货未收货（商家填入物流后，买家确认收货前），3为已收货完成订单 
                'time TEXT,'  # 下单时间，格式为 'YYYY-MM-DD HH:MM:SS.SSS' 的日期
                'book_id TEXT,'  # 书本编号
                'price INTEGER,'  # 书本价格
                'FOREIGN KEY(seller) REFERENCES Store(owner),'
                'FOREIGN KEY(buyer) REFERENCES User1(user_id),'
                'FOREIGN KEY(book_id) REFERENCES Book(book_id)'
                ')'
            )

            conn.execute(
                'CREATE TABLE IF NOT EXISTS User_order('
                'user_id TEXT,'  # 用户名
                'order_id INTEGER PRIMARY KEY,'  # 订单号
                'FOREIGN KEY(user_id) REFERENCES User1(user_id),'
                'FOREIGN KEY(order_id) REFERENCES Orders(order_id)'
                ')'
            )

            # 插入初始数据
            sql = "select * from User1"
            conn.execute(sql)
            if not conn.fetchall():
                values = [['test_id', 'test_pwd', 100, 'test_token', 'test_terminal'],
                          ['test_id_2', 'test_pwd_2', 1000, 'test_token_2', 'test_terminal_2']]
                sql = "insert into User1 (user_id, password, balance, token, terminal) values (%s, %s, %s, %s, %s)"
                conn.executemany(sql, values)

            sql = "select * from Book"
            conn.execute(sql)
            if not conn.fetchall():
                values = [['book1', '霸王别姬', '李碧华', '新星出版社', '无', '无', '1', 235, 30, '1', '1', '1', '1', '1', '1', '1']]
                sql = "insert into Book(book_id, title, author, publisher, original_title, translator, pub_year , " \
                      "pages, price ," \
                      "currency_unit ,binding,isbn ,author_intro,book_intro ,content ,tags) values (%s,%s, %s, %s, " \
                      "%s, %s,%s, %s, %s, " \
                      "%s, %s,%s, %s, %s, %s, %s) "
                conn.executemany(sql, values)

            sql = "select * from Store"
            conn.execute(sql)
            if not conn.fetchall():
                values = [[1, 'test_id']]
                sql = "insert into Store(store_id ,owner) values (%s, %s)"
                conn.executemany(sql, values)

            sql = "select * from Books_in_store"
            conn.execute(sql)
            if not conn.fetchall():
                values = [[1, 'book1', '霸王别姬', 10]]
                sql = "insert into Books_in_store(store_id, book_id, book_name, book_num) values (%s, %s, %s, %s)"
                conn.executemany(sql, values)

            sql = "select * from Orders"
            conn.execute(sql)
            if not conn.fetchall():
                values = [[1, 'test_id', 'test_id_2', 3, '2022-11-25 23:00:50.000', 'book1', 10]]
                sql = "insert into Orders(order_id, seller, buyer, status, time, book_id, price) values (%s, %s, %s, " \
                      "%s, %s, %s, %s) "
                conn.executemany(sql, values)

            sql = "select * from User_order"
            conn.execute(sql)
            if not conn.fetchall():
                values = [['test_id', 1]]
                sql = "insert into User_order(user_id, order_id) values (%s, %s)"
                conn.executemany(sql, values)

        except psycopg2.DatabaseError as e:
            print(e)
            #conn.rollback()


database_instance: Store = None


def init_database():
    global database_instance
    database_instance = Store()


def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()

