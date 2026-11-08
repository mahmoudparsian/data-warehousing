#!/usr/bin/env python
import os
import pymysql

conn = pymysql.connect(host="localhost", port=3306, user="root", passwd=os.environ.get("MYSQL_PASSWORD", ""), db="mysql")

cur = conn.cursor()

cur.execute("SELECT Host,User FROM user")

print(cur.description)
print()

for row in cur:
    print(row)

cur.close()
conn.close()
