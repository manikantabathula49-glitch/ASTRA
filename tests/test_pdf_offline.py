"""
Offline regression tests for the ASTRA PDF server (no running services needed).
Run:  python -m pytest tests/test_pdf_offline.py   (or: python tests/test_pdf_offline.py)
"""

import os
import sys
import tempfile

os.environ.setdefault("ASTRA_PDF_OUTPUT", tempfile.mkdtemp(prefix="astra_pdf_test_"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "services"))

from fastapi.testclient import TestClient  # noqa: E402
import pdf_server  # noqa: E402

client = TestClient(pdf_server.app)
MARKDOWN = "# Title ✓\n## Section\n- **bold** item — résumé 🚀\n```\nprint('hi')\n```\n---\nPlain **text**."


def test_unicode_content_renders():
    r = client.post("/generate", json={"title": "Unicode ✓", "content": MARKDOWN, "direct_download": True})
    assert r.status_code == 200, r.text
    assert r.headers["content-type"] == "application/pdf"
    assert r.content.startswith(b"%PDF-")


def test_json_response_and_download():
    r = client.post("/generate", json={"title": "Report", "content": MARKDOWN})
    assert r.status_code == 200, r.text
    filename = r.json()["filename"]
    assert client.get(f"/download/{filename}").status_code == 200
    assert filename in client.get("/list").json()["pdfs"]


def test_download_rejects_path_traversal():
    assert client.get("/download/..%5C..%5Csecret.pdf").status_code == 400
    assert client.get("/download/.hidden.pdf").status_code == 400


def test_invalid_template():
    r = client.post("/generate", json={"title": "x", "content": "y", "template": "nope"})
    assert r.status_code == 400


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"[OK] {name}")
