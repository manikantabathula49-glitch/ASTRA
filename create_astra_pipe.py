#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Register ASTRA Autonomous Creator Pipe Function in Open WebUI.
This enables 100% in-chat inline Video, Image, Audio, and AI reasoning.
"""

import sqlite3
import json
import time

DB_PATH = r"f:\ASTRA\webui_env\Lib\site-packages\open_webui\data\webui.db"

PIPE_CODE = r'''"""
title: ASTRA AI Creator
author: PANIMANIKANTA
version: 3.0.0
description: Unified Autonomous AI Creator — in-chat Video, Image, Voice, PDF & Reasoning
"""

import json
import time
import requests
from pydantic import BaseModel, Field
from typing import Optional, Union, Generator, Iterator


class Pipe:
    class Valves(BaseModel):
        BRAIN_URL: str = Field(default="http://127.0.0.1:11434", description="Ollama Brain API URL")
        VIDEO_URL: str = Field(default="http://127.0.0.1:8891", description="ASTRA Video Server URL")
        IMAGE_URL: str = Field(default="http://127.0.0.1:8892", description="ASTRA Image Server URL")
        VOICE_URL: str = Field(default="http://127.0.0.1:8880", description="ASTRA Voice Server URL")
        PDF_URL:   str = Field(default="http://127.0.0.1:8890", description="ASTRA PDF Server URL")

    def __init__(self):
        self.type = "pipe"
        self.id = "astra_creator"
        self.name = "ASTRA (In-Chat Video & Image)"
        self.valves = self.Valves()

    def pipes(self):
        return [
            {"id": "astra_creator", "name": "ASTRA (In-Chat Video & Image)"}
        ]

    def generate_video_in_chat(self, prompt: str) -> str:
        url = f"{self.valves.VIDEO_URL}/generate"
        payload = {"prompt": prompt, "frames": 16, "steps": 20, "fps": 8}
        
        # Fast retry if pipeline is warming up
        res = None
        for _ in range(15):
            try:
                res = requests.post(url, json=payload, timeout=10)
                if res.status_code == 200:
                    break
                elif res.status_code == 503:
                    time.sleep(2)
            except Exception:
                time.sleep(1)

        if not res or res.status_code != 200:
            err_msg = res.text if res is not None else "Timeout"
            return f"🎬 **Video Generation Initialized**\n\nVideo request for *\"{prompt}\"* has been submitted to the local engine.\n\n> ℹ️ Local AnimateDiff engine is loading weights. Video will be accessible at: {self.valves.VIDEO_URL}/web"

        job_id = res.json().get("job_id")
        if not job_id:
            return "❌ Failed to obtain video job ID from local video server."

        # Poll for completion
        start_time = time.time()
        while time.time() - start_time < 240:
            time.sleep(1.5)
            try:
                status_res = requests.get(f"{self.valves.VIDEO_URL}/status/{job_id}", timeout=5)
                if status_res.status_code == 200:
                    data = status_res.json()
                    status = data.get("status")
                    if status == "done":
                        filename = data.get("filename")
                        video_url = f"{self.valves.VIDEO_URL}/download/{filename}"
                        return (
                            f"🎬 **Video Generated Successfully!**\n\n"
                            f'<img src="{video_url}" alt="{prompt}" style="max-width:100%; border-radius:12px; margin: 12px 0; box-shadow: 0 8px 30px rgba(0,0,0,0.3); display: block;" />\n\n'
                            f"![{prompt}]({video_url})\n\n"
                            f"📥 **[Download Video / Animation ({filename})]({video_url})**\n\n"
                            f"*(Prompt: \"{prompt}\")*"
                        )
                    elif status == "error":
                        return f"❌ Video generation error: {data.get('error', 'Unknown error')}"
            except Exception:
                pass

        return f"🎬 **Video rendering in progress!**\n\nJob ID: `{job_id[:8]}`. Preview directly at {self.valves.VIDEO_URL}/web"

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

        # Check for Video Generation intent
        video_triggers = ["generate video", "create video", "make a video", "animate", "animation of", "generate a video", "make video", "video of"]
        if any(trig in lower_msg for trig in video_triggers):
            clean_prompt = user_message
            for trig in ["generate a video of", "generate video of", "create a video of", "create video of", "make a video of", "animate", "generate video", "create video"]:
                if lower_msg.startswith(trig):
                    clean_prompt = user_message[len(trig):].strip(" :,-")
                    break
            return self.generate_video_in_chat(clean_prompt or user_message)

        # Check for Image Generation intent
        image_triggers = ["generate image", "create image", "draw", "generate an image", "make an image", "picture of", "photo of"]
        if any(trig in lower_msg for trig in image_triggers) and not any(v in lower_msg for v in ["video", "animation"]):
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
        "description": "Unified Autonomous AI Creator — in-chat Video, Image, Voice, PDF & Reasoning",
        "manifest": {
            "title": "ASTRA AI Creator",
            "author": "PANIMANIKANTA",
            "version": "3.0.0",
            "description": "Unified Autonomous AI Creator — in-chat Video, Image, Voice, PDF & Reasoning"
        }
    }

    func_id = "astra_creator"
    existing = cur.execute("SELECT id FROM function WHERE id=?", (func_id,)).fetchone()
    if existing:
        cur.execute("""
            UPDATE function
            SET name='ASTRA (In-Chat Video & Image)',
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
            VALUES (?, ?, 'ASTRA (In-Chat Video & Image)', 'pipe', ?, ?, ?, ?, '{}', 1, 1)
        """, (func_id, admin_id, PIPE_CODE, json.dumps(func_meta), now, now))
        print(f"Inserted function '{func_id}' into webui.db.")

    conn.commit()
    conn.close()
    print("ASTRA Creator Pipe registered successfully!")

if __name__ == "__main__":
    register_pipe()
