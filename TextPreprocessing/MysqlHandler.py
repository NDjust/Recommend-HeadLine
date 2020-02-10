from pymysql.err import Error

import pymysql
import pandas as pd


class MysqlHandler:

    def __init__(self, host, user, password, port) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.session = None

    def __enter__(self) -> object:
        try:
            conn = pymysql.connect(host=self.host, user=self.user,
                                   password=self.password,
                                   port=self.port, charset="utf8")
            print(conn.get_server_info() + "\n")

            print(f"Connected DB = {self.host}")
            self.session = conn

        except Error as e:
            print(f"Error ={e}")

        return self

    def mysql_to_csv(self, sql: str, file_path: str) -> pd.DataFrame:
        if self.session is not None:
            conn = self.session

            df = pd.read_sql(sql, conn)
            df.to_csv(file_path, encoding='utf-8-sig', header=True, \
                      doublequote=True, sep=',', index=False)
            print('File, {}, has been created successfully'.format(file_path))

            return df
        else:
            print("DB is Not Connected")

    def view_data(self, sql: str, db_table: str) -> None:
        if self.session is not None:
            conn = self.session

            cursor = conn.cursour()
            cursor.execute(f"SHOW columns FROM {db_table}")
            column_names = [col[0] for col in cursor.fetchall()]

            cursor.execute(sql)

            record = cursor.fetchall()

            for row in record:
                for i in range(len(column_names)):
                    print(f"{column_names[i]} = {row[i]}")

            return record

        else:
            print("DB is not Connected")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()