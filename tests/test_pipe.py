import sqlite3
import types

conn = sqlite3.connect(r"f:\ASTRA\webui_env\Lib\site-packages\open_webui\data\webui.db")
cur = conn.cursor()
code = cur.execute("SELECT content FROM function WHERE id='astra_creator'").fetchone()[0]
m = types.ModuleType("pipe_test")
exec(code, m.__dict__)
pipe = m.Pipe()
print("Pipe Name:", pipe.name)
print("Pipe ID:", pipe.id)
print("Pipes list:", pipe.pipes())
