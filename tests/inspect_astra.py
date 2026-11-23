import os
import glob
import sqlite3

BASE_DIR = os.environ.get("ASTRA_HOME") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def find_webui_db():
    """Locate Open WebUI's webui.db (DATA_DIR env, Windows venv, Linux venv, or installed package)."""
    candidates = []
    if os.environ.get("DATA_DIR"):
        candidates.append(os.path.join(os.environ["DATA_DIR"], "webui.db"))
    candidates.append(os.path.join(BASE_DIR, "webui_env", "Lib", "site-packages", "open_webui", "data", "webui.db"))
    candidates += glob.glob(os.path.join(BASE_DIR, "webui_env", "lib", "python*", "site-packages", "open_webui", "data", "webui.db"))
    try:
        import open_webui
        candidates.append(os.path.join(os.path.dirname(open_webui.__file__), "data", "webui.db"))
    except Exception:
        pass
    for path in candidates:
        if os.path.exists(path):
            return path
    return candidates[0]

import json

db_path = find_webui_db()
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
