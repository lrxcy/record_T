# -*- coding: UTF-8 -*-

import os, sys
import pymysql
import logging
import argparse
sys.path.append(os.getcwd())
from p_table import print_table
from PrettyTable import PrettyTable


def execQuery(host, user, password, database, sql):
    db = pymysql.connect(host=host, user=user, password=password, database=database, port=3306, charset='utf8')
    cursor = db.cursor()
    if not cursor:
        raise (NameError, "连接数据库失败")
    else:
        try:
            cursor.execute(sql)
        except pymysql.err.ProgrammingError:
            logging.error('You have an error in your SQL syntax')
            db.rollback()
            return False
        else:
            ret = cursor.fetchall()
            cols = cursor.description  # 类似 desc table_name 返回结果
            col = []
            for v in cols:
                col.append(v[0])
            db.commit()
            cursor.close()
            db.close()
            return col, ret


def table_P(col, ret):
    p = []
    p.append(col)
    for rs in ret:
        t = [str(i) for i in list(rs)]
        p.append(t)
    return print_table(p)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="mysql execQuery")
    parser.add_argument('-r', '--host', help="host", type=str, required=True)
    parser.add_argument('-u', '--user', help="user", type=str, required=True)
    parser.add_argument('-p', '--password', help="password", type=str, required=True)
    parser.add_argument('-d', '--database', help="database", type=str, required=True)
    parser.add_argument('-s', '--sql', help="sql", type=str, required=False)

    args = parser.parse_args()
    if args.sql != None:
        sql = args.sql
    else:
#         sql = "show databases;"
        sql = "show tables;"
    c, r = execQuery(args.host, args.user, args.password, args.database, sql)
    # p_table methods
    table_P(c, r)

    # PrettyTable methods
    x = PrettyTable(c)
    for n in c:
        x.align[n] = 'l'
    for i in r:
        t = [str(v) for v in list(i)]
        x.add_row(t)
    print(x)
