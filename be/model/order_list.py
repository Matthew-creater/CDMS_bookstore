from be.model import db_conn
from be.model import error
import psycopg2

class Order(db_conn.DBConn):

    def cancel_order(self, order_id):
        # 从 Orders 表中移除
        self.conn.execute(
            "DELETE FROM Orders WHERE order_id = '%s' RETURNING order_id, seller, buyer, store, status, time, book_id, price" %(order_id))
        row = self.conn.fetchone()
        store_id = row[3]
        book_id = row[6]
        price = row[7]

        # 查询得到 book_num
        self.conn.execute("SELECT book_num from Books_in_store where store_id = '%s'" %(store_id))
        row = self.conn.fetchone()
        book_num = row[0]

        # 计算得到 count
        self.conn.execute("SELECT price from Book where book_id = '%s'" %(book_id))
        row = self.conn.fetchone()
        one_price = row[0]
        count = int(price/one_price)

        # 更新 Books_in_store 表库存
        self.conn.execute("UPDATE Books_in_store set book_num = '%s' WHERE store_id = '%s' and book_id = '%s'" %((book_num + count), store_id, book_id))

        return 200, "ok"

