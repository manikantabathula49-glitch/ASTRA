import sqlite3
import json

db_path = r"f:\ASTRA\webui_env\Lib\site-packages\open_webui\data\webui.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()

for t in ["config", "tool", "function"]:
    print(f"\n=================== Table: {t} ===================")
    try:
        rows = cur.execute(f"SELECT * FROM {t}").fetchall()
        col_names = [d[0] for d in cur.description]
        print("Columns:", col_names)
        for r in rows:
            print("Row:", r)
    except Exception as e:
        print("Error:", e)

conn.close()
