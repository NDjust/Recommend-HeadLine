import pymysql
from pymysql.err import Error


try:
    conn = pymysql.connect(host="", user="",
                           password="", db="",
                           charset="utf8")
    print(conn.get_server_info())

    cursor = conn.cursor()

    sql = "create table chosun_news(" \
          "title varchar(100)," \
          "created_date varchar(100)," \
          "content text," \
          "views int," \
          "link varchar(150)," \
          "primary key (title))"

    cursor.execute(sql)
    conn.commit()
    sql = "insert into chosun_news values('test', 'test_contest', 10, 'https://lms.sch.ac.kr')"
    cursor.execute(sql)
    conn.commit()
    sql = "select * from chosun_news"

    num = cursor.execute(sql)
    print(num)
    result = cursor.fetchall()

    for v in result:
        print(f"title = {v[0]} content = {v[1]} views = {v[2]} link = {v[3]}")
    sql = "delete from chosun_news"
    cursor.execute(sql)
    conn.commit()
    conn.close()

except Error as e:
    print(e)

