#!/usr/bin/env python3
"""
ASTRA PDF Generation Server
Converts markdown/text to styled PDFs
Port: 8890
"""

import io, re, os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional
from fpdf import FPDF

app = FastAPI(title="ASTRA PDF Server", version="1.2.0")
BASE_DIR = os.environ.get("ASTRA_HOME") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.environ.get("ASTRA_PDF_OUTPUT", os.path.join(BASE_DIR, "pdf_output"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Unicode TrueType font candidates (Windows, Linux, macOS). Each entry maps
# a style ("", "B", "I", "BI") to a font file; the first family whose regular
# face exists is used. Core PDF fonts (Helvetica) only support Latin-1.
FONT_CANDIDATES = [
    ("Arial", {"": "C:/Windows/Fonts/arial.ttf", "B": "C:/Windows/Fonts/arialbd.ttf",
               "I": "C:/Windows/Fonts/ariali.ttf", "BI": "C:/Windows/Fonts/arialbi.ttf"}),
    ("DejaVu", {"": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "B": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "I": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
                "BI": "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf"}),
    ("ArialUnicode", {"": "/Library/Fonts/Arial Unicode.ttf"}),
]
CODE_FONT_CANDIDATES = [
    ("Consolas", "C:/Windows/Fonts/consola.ttf"),
    ("DejaVuMono", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
]


def safe_filename(filename: str) -> str:
    """Reject path traversal (e.g. '..\\..\\secret' on Windows)."""
    name = os.path.basename(filename.replace("\\", "/"))
    if not name or name != filename or name.startswith("."):
        raise HTTPException(status_code=400, detail="Invalid filename.")
    return name

# ─── Color Palette ────────────────────────────────────────────────────────────
COLORS = {
    "header_bg":  (10, 12, 30),
    "accent":     (100, 200, 255),
    "h1":         (30, 90, 180),
    "h2":         (40, 120, 200),
    "h3":         (60, 140, 180),
    "body":       (30, 30, 40),
    "code_bg":    (240, 242, 248),
    "code_text":  (160, 50, 80),
    "muted":      (120, 130, 150),
    "line":       (200, 210, 230),
}


def clean_text(text: str) -> str:
    if not text:
        return ""
    replacements = {
        "\u2014": " - ",
        "\u2013": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2026": "...",
        "\u00a0": " ",
        "\u2022": "*",
        "\u2192": "->",
        "\u2190": "<-",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def latin1_safe(text: str) -> str:
    """Core PDF fonts only cover Latin-1; replace anything else with '?'."""
    return text.encode("latin-1", errors="replace").decode("latin-1")


# ─── Custom PDF Class ─────────────────────────────────────────────────────────
class ASTRAPDF(FPDF):
    def __init__(self, title, author, template):
        super().__init__()
        self.doc_title = clean_text(title)
        self.doc_author = clean_text(author)
        self.template = template
        self.font_main = "Helvetica"
        self.font_code = "Courier"
        
        self.unicode_fonts = False

        # Load Unicode TrueType fonts if available (falls back to Latin-1 core fonts)
        for family, files in FONT_CANDIDATES:
            regular = files.get("")
            if not regular or not os.path.exists(regular):
                continue
            try:
                for style in ("", "B", "I", "BI"):
                    path = files.get(style)
                    self.add_font(family, style, path if path and os.path.exists(path) else regular)
                self.font_main = family
                self.unicode_fonts = True
                break
            except Exception:
                continue
        for family, path in CODE_FONT_CANDIDATES:
            if self.unicode_fonts and os.path.exists(path):
                try:
                    self.add_font(family, "", path)
                    self.font_code = family
                    break
                except Exception:
                    continue

        self.set_margins(20, 25, 20)
        self.set_auto_page_break(auto=True, margin=18)

    def normalize_text(self, text):
        if not self.unicode_fonts or self.font_family in ("helvetica", "courier", "times"):
            text = latin1_safe(text)
        return super().normalize_text(text)

    def header(self):
        r, g, b = COLORS["header_bg"]
        self.set_fill_color(r, g, b)
        self.rect(0, 0, 210, 16, "F")
        self.set_font(self.font_main, "B", 8)
        r, g, b = COLORS["accent"]
        self.set_text_color(r, g, b)
        self.set_xy(10, 4)
        self.cell(0, 8, f"  ASTRA AI  -  {self.doc_title}", align="L")
        r, g, b = COLORS["muted"]
        self.set_text_color(r, g, b)
        self.set_xy(10, 4)
        self.cell(0, 8, f"Generated by PANIMANIKANTA's ASTRA  ", align="R")
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def footer(self):
        self.set_y(-14)
        r, g, b = COLORS["header_bg"]
        self.set_fill_color(r, g, b)
        self.rect(0, self.get_y(), 210, 14, "F")
        self.set_font(self.font_main, "I", 7)
        r, g, b = COLORS["accent"]
        self.set_text_color(r, g, b)
        self.cell(
            0, 10,
            f"ASTRA AI Ecosystem  |  {self.doc_author}  |  Page {self.page_no()}  |  {datetime.now().strftime('%Y-%m-%d')}",
            align="C"
        )

    def cover_page(self, subtitle=None):
        self.add_page()
        # Big accent bar
        r, g, b = COLORS["h1"]
        self.set_fill_color(r, g, b)
        self.rect(0, 60, 210, 4, "F")
        # Title
        self.set_font(self.font_main, "B", 24)
        r, g, b = COLORS["body"]
        self.set_text_color(r, g, b)
        self.set_xy(20, 75)
        self.multi_cell(170, 12, self.doc_title, align="C")
        # Subtitle
        if subtitle:
            self.set_font(self.font_main, "", 13)
            r, g, b = COLORS["muted"]
            self.set_text_color(r, g, b)
            self.set_x(20)
            self.multi_cell(170, 8, clean_text(subtitle), align="C")
        # Meta
        self.set_font(self.font_main, "", 10)
        r, g, b = COLORS["muted"]
        self.set_text_color(r, g, b)
        self.set_xy(20, 160)
        self.cell(0, 8, f"Author: {self.doc_author}", align="C")
        self.ln(7)
        self.set_x(20)
        self.cell(0, 8, f"Date: {datetime.now().strftime('%B %d, %Y')}", align="C")
        self.ln(7)
        self.set_x(20)
        self.cell(0, 8, f"Template: {self.template.capitalize()}", align="C")
        self.set_text_color(0, 0, 0)


# ─── Markdown Renderer ────────────────────────────────────────────────────────
def render_markdown(pdf: ASTRAPDF, content: str):
    content = clean_text(content)
    lines = content.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]

        # Code block
        if line.strip().startswith("```"):
            i += 1
            code = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            r, g, b = COLORS["code_bg"]
            pdf.set_fill_color(r, g, b)
            pdf.set_font(pdf.font_code, "", 8)
            r, g, b = COLORS["code_text"]
            pdf.set_text_color(r, g, b)
            pdf.multi_cell(0, 5, "\n".join(code), fill=True, border=1)
            pdf.ln(3)
            pdf.set_text_color(0, 0, 0)

        # H1
        elif line.startswith("# "):
            pdf.ln(4)
            r, g, b = COLORS["h1"]
            pdf.set_text_color(r, g, b)
            pdf.set_font(pdf.font_main, "B", 18)
            pdf.multi_cell(0, 9, line[2:].strip())
            # underline
            pdf.set_draw_color(*COLORS["h1"])
            pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 170, pdf.get_y())
            pdf.ln(4)

        # H2
        elif line.startswith("## "):
            pdf.ln(3)
            r, g, b = COLORS["h2"]
            pdf.set_text_color(r, g, b)
            pdf.set_font(pdf.font_main, "B", 13)
            pdf.multi_cell(0, 8, line[3:].strip())
            pdf.ln(2)

        # H3
        elif line.startswith("### "):
            pdf.ln(2)
            r, g, b = COLORS["h3"]
            pdf.set_text_color(r, g, b)
            pdf.set_font(pdf.font_main, "BI", 10.5)
            pdf.multi_cell(0, 7, line[4:].strip())
            pdf.ln(1)

        # Bullet
        elif re.match(r"^[-*] ", line):
            pdf.set_text_color(*COLORS["body"])
            pdf.set_x(24)
            bullet_text = line[2:].strip()
            parts = re.split(r"\*\*(.*?)\*\*", bullet_text)
            pdf.set_font(pdf.font_main, "", 9.5)
            pdf.write(5, "*  ")
            for j, part in enumerate(parts):
                if j % 2 == 1:
                    pdf.set_font(pdf.font_main, "B", 9.5)
                else:
                    pdf.set_font(pdf.font_main, "", 9.5)
                if part:
                    pdf.write(5, part)
            pdf.ln(5.5)

        # Horizontal rule
        elif line.strip() == "---":
            pdf.ln(2)
            pdf.set_draw_color(*COLORS["line"])
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(4)

        # Empty line
        elif line.strip() == "":
            pdf.ln(3)

        # Regular paragraph
        else:
            pdf.set_text_color(*COLORS["body"])
            parts = re.split(r"\*\*(.*?)\*\*", line)
            pdf.set_x(20)
            for j, part in enumerate(parts):
                if j % 2 == 1:
                    pdf.set_font(pdf.font_main, "B", 9.5)
                else:
                    pdf.set_font(pdf.font_main, "", 9.5)
                if part:
                    pdf.write(5.5, part)
            pdf.ln(5.5)

        i += 1
    pdf.set_text_color(0, 0, 0)


# ─── Request Model ────────────────────────────────────────────────────────────
class PDFRequest(BaseModel):
    title: str
    content: str
    template: str = "report"
    author: str = "ASTRA AI"
    subtitle: Optional[str] = None
    direct_download: bool = False


# ─── Routes ───────────────────────────────────────────────────────────────────
@app.post("/generate")
def generate_pdf(req: PDFRequest):
    if req.template not in ["report", "resume", "technical", "notes", "proposal"]:
        raise HTTPException(status_code=400, detail="Invalid template.")
    try:
        pdf = ASTRAPDF(req.title, req.author, req.template)
        pdf.cover_page(subtitle=req.subtitle)
        pdf.add_page()
        render_markdown(pdf, req.content)

        safe_title = re.sub(r"[^\w\s-]", "", req.title).strip().replace(" ", "_") or "ASTRA_Document"
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_title}_{timestamp}.pdf"
        filepath = os.path.join(OUTPUT_DIR, filename)

        raw_bytes = pdf.output()
        with open(filepath, "wb") as f:
            f.write(raw_bytes)

        if req.direct_download:
            return StreamingResponse(
                io.BytesIO(bytes(raw_bytes)),
                media_type="application/pdf",
                headers={"Content-Disposition": f'attachment; filename="{filename}"'}
            )

        return {
            "status": "success",
            "title": req.title,
            "filename": filename,
            "filepath": filepath,
            "download_url": f"/download/{filename}",
            "template": req.template
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{filename}")
async def download_pdf(filename: str):
    filename = safe_filename(filename)
    filepath = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="PDF file not found.")
    return FileResponse(filepath, media_type="application/pdf", filename=filename)


@app.get("/list")
async def list_pdfs():
    files = sorted(f for f in os.listdir(OUTPUT_DIR) if f.endswith(".pdf"))
    return {"pdfs": files}


@app.get("/health")
async def health():
    return {"status": "online", "engine": "fpdf2", "port": 8890}


@app.get("/web", response_class=HTMLResponse)
async def web_ui():
    return r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ASTRA PDF Generator</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#050810;color:#e0e6f0;font-family:'Outfit',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:2rem}
.card{background:rgba(255,255,255,0.04);border:1px solid rgba(100,200,255,0.15);border-radius:20px;padding:2.5rem;width:100%;max-width:760px;backdrop-filter:blur(20px);box-shadow:0 0 60px rgba(0,120,255,0.07)}
h1{font-size:2rem;font-weight:700;color:#64c8ff;text-align:center;margin-bottom:.3rem}
.sub{text-align:center;color:#7a8ba0;font-size:.9rem;margin-bottom:2rem}
label{display:block;font-size:.75rem;color:#7a8ba0;text-transform:uppercase;letter-spacing:.07em;margin-bottom:.4rem}
input,select,textarea{width:100%;background:rgba(255,255,255,0.05);border:1px solid rgba(100,200,255,0.2);border-radius:12px;color:#e0e6f0;font-family:'Outfit',sans-serif;font-size:1rem;padding:.8rem 1rem;outline:none;transition:border-color .2s;margin-bottom:1.2rem}
textarea{height:300px;resize:vertical}
input:focus,select:focus,textarea:focus{border-color:#64c8ff}
select option{background:#0d1117}
.row{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.btn{width:100%;padding:.9rem;background:linear-gradient(135deg,#64c8ff,#a78bfa);border:none;border-radius:12px;color:#050810;font-family:'Outfit',sans-serif;font-size:1rem;font-weight:700;cursor:pointer;transition:opacity .2s,transform .1s}
.btn:hover{opacity:.9;transform:translateY(-1px)}
.btn:disabled{opacity:.5;cursor:not-allowed;transform:none}
</style>
</head>
<body>
<div class="card">
  <h1>📄 ASTRA PDF Generator</h1>
  <p class="sub">Generate beautifully formatted PDF documents locally</p>
  <div class="row">
    <div><label>Document Title</label><input id="title" placeholder="My ASTRA Report"></div>
    <div><label>Author</label><input id="author" value="PANIMANIKANTA"></div>
  </div>
  <div class="row">
    <div><label>Template</label>
      <select id="template">
        <option value="report">📄 Report</option>
        <option value="technical">🔧 Technical Doc</option>
        <option value="resume">👤 Resume</option>
        <option value="notes">📝 Notes</option>
        <option value="proposal">📊 Proposal</option>
      </select>
    </div>
    <div><label>Subtitle (optional)</label><input id="subtitle" placeholder="Optional subtitle..."></div>
  </div>
  <label>Content (Markdown supported: # ## ### **bold** - list ```code```)</label>
  <textarea id="content" placeholder="# Introduction&#10;Write your content here...&#10;&#10;## Section 1&#10;- Point one&#10;- Point two&#10;&#10;**Bold text** is supported."></textarea>
  <button class="btn" id="btn" onclick="generate()">⚡ Generate PDF</button>
</div>
<script>
async function generate(){
  const btn=document.getElementById('btn');
  const title=document.getElementById('title').value.trim();
  const content=document.getElementById('content').value.trim();
  if(!title||!content){alert('Title and content are required!');return;}
  btn.disabled=true;btn.textContent='⏳ Generating...';
  try{
    const r=await fetch('/generate',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({title,content,template:document.getElementById('template').value,
        author:document.getElementById('author').value||'ASTRA AI',
        subtitle:document.getElementById('subtitle').value||null,
        direct_download:true})});
    if(!r.ok)throw new Error(await r.text());
    const blob=await r.blob();
    const a=document.createElement('a');
    a.href=URL.createObjectURL(blob);
    a.download=title.replace(/\s+/g,'_')+'.pdf';
    a.click();
  }catch(e){alert('Error: '+e.message);}
  finally{btn.disabled=false;btn.textContent='⚡ Generate PDF';}
}
</script>
</body></html>"""


if __name__ == "__main__":
    import uvicorn
    print("[ASTRA PDF] Starting on port 8890...")
    uvicorn.run(app, host="0.0.0.0", port=8890, log_level="warning")
