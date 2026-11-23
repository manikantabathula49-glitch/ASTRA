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

import types

conn = sqlite3.connect(find_webui_db())
cur = conn.cursor()
code = cur.execute("SELECT content FROM function WHERE id='astra_creator'").fetchone()[0]
m = types.ModuleType("pipe_test")
exec(code, m.__dict__)
pipe = m.Pipe()
print("Pipe Name:", pipe.name)
print("Pipe ID:", pipe.id)
print("Pipes list:", pipe.pipes())
