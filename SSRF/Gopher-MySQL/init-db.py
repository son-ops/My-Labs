import os
import time

import mysql.connector


CFG = dict(
    host=os.getenv("DB_HOST", "db"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_ROOT_USER", "root"),
    password=os.getenv("DB_ROOT_PASSWORD", "rootpassword"),
    charset="utf8mb4",
)
ARCHIVE, USER, FLAG = (
    os.getenv("ARCHIVE_DB", "archive"),
    os.getenv("LEGACY_USER", "legacy_export"),
    os.getenv("FLAG_VALUE", "SSS{mysql_gopher_curl_lab}"),
)

err = None
for _ in range(60):
    try:
        conn = mysql.connector.connect(**CFG)
        break
    except mysql.connector.Error as err:
        time.sleep(2)
else:
    raise err

cur = conn.cursor()
for sql in (
    f"CREATE DATABASE IF NOT EXISTS `{ARCHIVE}`",
    f"CREATE TABLE IF NOT EXISTS `{ARCHIVE}`.recovery_flags (id INT PRIMARY KEY AUTO_INCREMENT, note VARCHAR(255) UNIQUE, flag VARCHAR(255) NOT NULL)",
    f"CREATE USER IF NOT EXISTS '{USER}'@'%' IDENTIFIED WITH mysql_native_password BY ''",
):
    cur.execute(sql)

cur.execute(
    f"INSERT IGNORE INTO `{ARCHIVE}`.recovery_flags (note, flag) VALUES (%s, %s)",
    ("Recovery markers copied from export.", FLAG),
)
cur.execute(f"GRANT SELECT ON `{ARCHIVE}`.* TO '{USER}'@'%'")
cur.execute("FLUSH PRIVILEGES")

conn.commit()
cur.close()
conn.close()
