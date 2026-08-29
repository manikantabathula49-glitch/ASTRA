#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Register ASTRA Autonomous Creator Pipe Function in Open WebUI.
This enables 100% in-chat inline Image, Voice, PDF generation, and AI reasoning.
"""

import sqlite3
import json
import time

DB_PATH = r"f:\ASTRA\webui_env\Lib\site-packages\open_webui\data\webui.db"

PIPE_CODE = r'''"""
title: ASTRA AI Creator
author: PANIMANIKANTA
version: 3.1.0
description: Unified Autonomous AI Creator — in-chat Image, Voice, PDF & Reasoning
"""

import json
import time
import requests
from pydantic import BaseModel, Field
from typing import Optional, Union, Generator, Iterator


class Pipe:
    class Valves(BaseModel):
        BRAIN_URL: str = Field(default="http://127.0.0.1:11434", description="Ollama Brain API URL")
        IMAGE_URL: str = Field(default="http://127.0.0.1:8892", description="ASTRA Image Server URL")
        VOICE_URL: str = Field(default="http://127.0.0.1:8880", description="ASTRA Voice Server URL")
        PDF_URL:   str = Field(default="http://127.0.0.1:8890", description="ASTRA PDF Server URL")

    def __init__(self):
        self.type = "pipe"
        self.id = "astra_creator"
        self.name = "ASTRA (In-Chat Creator)"
        self.valves = self.Valves()

    def pipes(self):
        return [
            {"id": "astra_creator", "name": "ASTRA (In-Chat Creator)"}
        ]

    def generate_pdf_in_chat(self, title: str, content: str) -> str:
        url = f"{self.valves.PDF_URL}/generate"
        payload = {"title": title or "ASTRA Report", "content": content, "template": "report", "author": "ASTRA AI"}
        try:
            res = requests.post(url, json=payload, timeout=30)
            if res.status_code == 200:
                data = res.json()
                filename = data.get("filename", "document.pdf")
                download_path = data.get("download_url", f"/download/{filename}")
                pdf_url = f"{self.valves.PDF_URL}{download_path}"
                filepath = data.get("filepath", f"f:\\ASTRA\\pdf_output\\{filename}")
                return (
                    f"📄 **PDF Created Successfully!**\n\n"
                    f"### 📑 {title}\n"
                    f"- **File Name**: `{filename}`\n"
                    f"- **Saved Location**: `{filepath}`\n\n"
                    f'<div style="margin: 12px 0;">'
                    f'<a href="{pdf_url}" download="{filename}" target="_blank" style="background: linear-gradient(135deg, #3b82f6, #6366f1); color: white; padding: 10px 22px; border-radius: 12px; text-decoration: none; font-weight: 600; font-size: 0.95em; display: inline-flex; align-items: center; gap: 8px;">📥 Download PDF Document</a>'
                    f'</div>\n\n'
                    f"📄 **[Download PDF File]({pdf_url})**"
                )
            return f"❌ PDF generation failed ({res.status_code}): {res.text}"
        except Exception as e:
            return f"❌ PDF error: {e}"

    def generate_image_in_chat(self, prompt: str) -> str:
        url = f"{self.valves.IMAGE_URL}/generate"
        payload = {"prompt": prompt, "steps": 15, "guidance": 7.0, "width": 512, "height": 512, "enhance_with_claude": True}
        try:
            res = requests.post(url, json=payload, timeout=15)
            if res.status_code != 200:
                return f"❌ Image generation request failed: {res.text}"
            job_id = res.json().get("job_id")
            if not job_id:
                return "❌ Invalid image job ID."
            
            start_time = time.time()
            while time.time() - start_time < 90:
                time.sleep(0.2)
                try:
                    s_res = requests.get(f"{self.valves.IMAGE_URL}/status/{job_id}", timeout=3)
                    if s_res.status_code == 200:
                        data = s_res.json()
                        if data.get("status") == "done":
                            filename = data.get("filename")
                            b64_data = data.get("b64_data")
                            img_url = f"{self.valves.IMAGE_URL}/download/{filename}"
                            img_src = f"data:image/png;base64,{b64_data}" if b64_data else img_url
                            return (
                                f"🎨 **Image Generated Successfully!**\n\n"
                                f'<div style="text-align: center; margin: 15px 0;">'
                                f'<img src="{img_src}" alt="{prompt}" style="max-width:100%; border-radius:16px; box-shadow: 0 12px 35px rgba(0,0,0,0.5); display: inline-block;" />'
                                f'<div style="margin-top: 14px; display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">'
                                f'<a href="{img_url}" download="{filename}" style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 10px 20px; border-radius: 12px; text-decoration: none; font-weight: 600; font-size: 0.95em; display: inline-flex; align-items: center; gap: 6px;">📥 Download PNG</a>'
                                f'<a href="{self.valves.IMAGE_URL}/web" target="_blank" style="background: linear-gradient(135deg, #8b5cf6, #6366f1); color: white; padding: 10px 20px; border-radius: 12px; text-decoration: none; font-weight: 600; font-size: 0.95em; display: inline-flex; align-items: center; gap: 6px;">🔄 Retry / Modify Image</a>'
                                f'</div>'
                                f'</div>\n\n'
                                f"📥 **[Download High-Res Image ({filename})]({img_url})** | 🔄 *To retry with prompt, reply: \"generate image: {prompt}\"*"
                            )
                        elif data.get("status") == "error":
                            return f"❌ Image generation error: {data.get('error')}"
                except Exception:
                    pass
            return f"🎨 Image job queued. Preview at: {self.valves.IMAGE_URL}/web"
        except Exception as e:
            return f"❌ Image error: {e}"

    def pipe(self, body: dict, __user__: Optional[dict] = None) -> Union[str, Generator, Iterator]:
        messages = body.get("messages", [])
        if not messages:
            return "No prompt provided."

        user_message = messages[-1].get("content", "").strip()
        lower_msg = user_message.lower()

        # Check for PDF Generation intent
        pdf_triggers = ["generate pdf", "create pdf", "make pdf", "make a pdf", "convert to pdf", "pdf report", "download pdf", "pdf document"]
        if any(trig in lower_msg for trig in pdf_triggers):
            clean_title = "ASTRA Document"
            clean_content = user_message
            for trig in ["generate a pdf of", "generate pdf of", "create a pdf of", "create pdf of", "generate pdf", "create pdf", "make a pdf", "make pdf", "pdf report"]:
                if lower_msg.startswith(trig):
                    clean_content = user_message[len(trig):].strip(" :,-")
                    break
            lines = clean_content.split("\n")
            if lines:
                clean_title = lines[0].lstrip("# ").strip() or "ASTRA Report"
            return self.generate_pdf_in_chat(clean_title, clean_content)

        # Check for Image Generation intent
        image_triggers = ["generate image", "create image", "draw", "generate an image", "make an image", "picture of", "photo of"]
        if any(trig in lower_msg for trig in image_triggers):
            clean_prompt = user_message
            for trig in ["generate an image of", "generate image of", "create an image of", "create image of", "draw a", "draw an", "draw", "generate image", "create image"]:
                if lower_msg.startswith(trig):
                    clean_prompt = user_message[len(trig):].strip(" :,-")
                    break
            return self.generate_image_in_chat(clean_prompt or user_message)

        # Standard Ultra-Fast LLM Chat Stream via Ollama ASTRA
        ollama_url = f"{self.valves.BRAIN_URL}/api/chat"
        ollama_payload = {
            "model": "astra:latest",
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": 0.6,
                "top_p": 0.9,
                "num_ctx": 2048
            }
        }

        try:
            r = requests.post(ollama_url, json=ollama_payload, stream=True, timeout=60)
            if r.status_code == 200:
                def stream_gen():
                    for line in r.iter_lines():
                        if line:
                            try:
                                chunk = json.loads(line.decode("utf-8"))
                                delta = chunk.get("message", {}).get("content", "")
                                if delta:
                                    yield delta
                            except Exception:
                                pass
                return stream_gen()
            else:
                return f"Error communicating with brain ({r.status_code}): {r.text}"
        except Exception as e:
            return f"Brain connection error: {e}"
'''

def register_pipe():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    admin_row = cur.execute("SELECT id FROM user WHERE role='admin' LIMIT 1").fetchone()
    admin_id = admin_row[0] if admin_row else "b0dac253-9aa2-4f71-9186-9cd8c10d386c"
    now = int(time.time())

    func_meta = {
        "description": "Unified Autonomous AI Creator — in-chat Image, Voice, PDF & Reasoning",
        "manifest": {
            "title": "ASTRA AI Creator",
            "author": "PANIMANIKANTA",
            "version": "3.1.0",
            "description": "Unified Autonomous AI Creator — in-chat Image, Voice, PDF & Reasoning"
        }
    }

    func_id = "astra_creator"
    existing = cur.execute("SELECT id FROM function WHERE id=?", (func_id,)).fetchone()
    if existing:
        cur.execute("""
            UPDATE function
            SET name='ASTRA (In-Chat Creator)',
                type='pipe',
                content=?,
                meta=?,
                updated_at=?,
                is_active=1,
                is_global=1
            WHERE id=?
        """, (PIPE_CODE, json.dumps(func_meta), now, func_id))
        print(f"Updated function '{func_id}' in webui.db.")
    else:
        cur.execute("""
            INSERT INTO function (id, user_id, name, type, content, meta, created_at, updated_at, valves, is_active, is_global)
            VALUES (?, ?, 'ASTRA (In-Chat Creator)', 'pipe', ?, ?, ?, ?, '{}', 1, 1)
        """, (func_id, admin_id, PIPE_CODE, json.dumps(func_meta), now, now))
        print(f"Inserted function '{func_id}' into webui.db.")

    conn.commit()
    conn.close()
    print("ASTRA Creator Pipe registered successfully!")

if __name__ == "__main__":
    register_pipe()
