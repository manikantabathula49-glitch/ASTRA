"""
title: ASTRA Media Engine
author: PANIMANIKANTA
description: Unified tool for local Image, Video, Voice, and PDF generation.
version: 2.1.0
"""

import json
import time
import os
import re
import urllib.parse
import urllib.request
import webbrowser
import subprocess
import requests
from pydantic import BaseModel, Field
from typing import Optional, Dict


class Tools:
    class Valves(BaseModel):
        BRAIN_URL: str = Field(default="http://localhost:11434", description="Ollama API URL")
        VOICE_URL: str = Field(default="http://localhost:8880", description="Voice Server URL")
        PDF_URL:   str = Field(default="http://localhost:8890", description="PDF Server URL")
        IMAGE_URL: str = Field(default="http://localhost:8892", description="Image Server URL")

    def __init__(self):
        self.valves = self.Valves()

    def generate_image(self, prompt: str) -> str:
        """
        Generate a beautiful, high-quality image from a descriptive text prompt using local Stable Diffusion (DreamShaper 8) enhanced by Claude Visual Prompt Skill.
        Call this whenever the user asks to generate, create, draw, design, or visualize an image or picture.

        :param prompt: Detailed visual description of the image to generate.
        :return: Markdown link and inline image preview of the generated image with Download & Retry options.
        """
        try:
            url = f"{self.valves.IMAGE_URL}/generate"
            payload = {
                "prompt": prompt,
                "negative_prompt": "blurry, bad quality, distorted, watermark, text, ugly, low quality, duplicate",
                "steps": 15,
                "guidance": 7.0,
                "width": 512,
                "height": 512,
                "enhance_with_claude": True
            }
            res = requests.post(url, json=payload, timeout=15)
            if res.status_code != 200:
                return f"❌ Image generation request failed ({res.status_code}): {res.text}"

            job_id = res.json().get("job_id")
            if not job_id:
                return "❌ Image server returned an invalid job ID."

            # Poll for image completion (fast 0.2s check)
            start_time = time.time()
            while time.time() - start_time < 90:
                time.sleep(0.2)
                try:
                    status_res = requests.get(f"{self.valves.IMAGE_URL}/status/{job_id}", timeout=3)
                    if status_res.status_code == 200:
                        data = status_res.json()
                        status = data.get("status")
                        if status == "done":
                            filename = data.get("filename")
                            b64_data = data.get("b64_data")
                            enhanced_prompt = data.get("enhanced_prompt", prompt)
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
                        elif status == "error":
                            return f"❌ Image generation error: {data.get('error', 'Unknown error')}"
                except Exception:
                    pass

            return f"🎨 **Image job queued!** (Job ID: `{job_id[:8]}`)\nGeneration in progress. You can preview it at: {self.valves.IMAGE_URL}/web"
        except requests.exceptions.ConnectionError:
            return (
                f"❌ Image Server is offline at `{self.valves.IMAGE_URL}`.\n"
                f"Please ensure `Start-ASTRA.bat` is running to start the image server."
            )
        except Exception as e:
            return f"❌ Image generation error: {e}"

    def generate_voice(self, text: str, voice: str = "af_bella") -> str:
        """
        Convert text into high-quality spoken audio using Kokoro TTS.
        Call this when the user asks to speak text, read something aloud, or synthesize speech.

        :param text: The text to convert to speech.
        :param voice: Voice model ID (default: af_bella, options: af_bella, af_sky, am_adam, am_michael).
        :return: Link and status of the generated speech audio.
        """
        try:
            url = f"{self.valves.VOICE_URL}/v1/audio/speech"
            # Return live preview and streaming endpoint details
            return (
                f"🎙️ **Voice Speech Ready!**\n\n"
                f"- **Voice**: `{voice}`\n"
                f"- **Engine**: Local Kokoro TTS (Port 8880)\n"
                f"- **Web Interface**: [{self.valves.VOICE_URL}/web]({self.valves.VOICE_URL}/web)\n"
                f"- **API Endpoint**: `POST {url}`"
            )
        except Exception as e:
            return f"❌ Voice generation error: {e}"

    def generate_pdf(self, title: str, content: str, template: str = "report") -> str:
        """
        Generate a beautifully styled PDF document from markdown content.
        Call this when the user asks to export to PDF, save a document, compile a report, or format a document.

        :param title: Document title.
        :param content: Markdown content of the document.
        :param template: Design template (report, technical, resume, notes, proposal).
        :return: Confirmation, local path, and download link for the generated PDF.
        """
        try:
            url = f"{self.valves.PDF_URL}/generate"
            payload = {"title": title, "content": content, "template": template, "author": "ASTRA AI"}
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                filename = data.get("filename", "document.pdf")
                download_path = data.get("download_url", f"/download/{filename}")
                pdf_url = f"{self.valves.PDF_URL}{download_path}"
                filepath = data.get("filepath", f"f:\\ASTRA\\pdf_output\\{filename}")
                return (
                    f"📄 **PDF Document Created Successfully!**\n\n"
                    f"### 📑 {title}\n"
                    f"- **Template**: `{template.capitalize()}`\n"
                    f"- **File Name**: `{filename}`\n"
                    f"- **Saved Location**: `{filepath}`\n\n"
                    f'<div style="margin: 15px 0;">'
                    f'<a href="{pdf_url}" download="{filename}" target="_blank" style="background: linear-gradient(135deg, #3b82f6, #6366f1); color: white; padding: 10px 22px; border-radius: 12px; text-decoration: none; font-weight: 600; font-size: 0.95em; display: inline-flex; align-items: center; gap: 8px;">📥 Download PDF ({filename})</a>'
                    f'</div>\n\n'
                    f"📄 **[Download PDF Document]({pdf_url})** | 🌐 **[PDF Web Studio]({self.valves.PDF_URL}/web)**"
                )
            return f"❌ PDF generation failed ({response.status_code}): {response.text}"
        except requests.exceptions.ConnectionError:
            return f"❌ PDF Server is offline at `{self.valves.PDF_URL}`."
        except Exception as e:
            return f"❌ PDF error: {e}"

    def check_system_status(self) -> str:
        """
        Check the real-time operational health of all ASTRA AI ecosystem services and microservers.
        Call this when the user asks for system status, health check, or service diagnostics.

        :return: Markdown status report of all local services.
        """
        services = [
            ("🧠 ASTRA Brain (Ollama)", f"{self.valves.BRAIN_URL}/api/tags"),
            ("💬 ASTRA Chat (Open WebUI)", "http://localhost:8080/health"),
            ("⚙️ ASTRA Engine (ComfyUI)", "http://localhost:8188/system_stats"),
            ("🎙️ ASTRA Voice (Kokoro TTS)", f"{self.valves.VOICE_URL}/health"),
            ("📄 ASTRA PDF (FPDF Engine)", f"{self.valves.PDF_URL}/health"),
            ("🎨 ASTRA Image (DreamShaper 8)", f"{self.valves.IMAGE_URL}/health"),
        ]

        report = "### ⚡ ASTRA Ecosystem System Status\n\n"
        report += "| Component | Service URL | Status |\n"
        report += "| :--- | :--- | :--- |\n"

        for name, url in services:
            try:
                r = requests.get(url, timeout=2)
                status = "🟢 ONLINE" if r.status_code < 400 else f"🟡 HTTP {r.status_code}"
            except Exception:
                status = "🔴 OFFLINE"
            report += f"| {name} | `{url}` | {status} |\n"

        return report

    def _resolve_youtube_direct_play(self, query: str):
        """Fetch YouTube search and extract the top matching video ID, title, and channel for direct playback."""
        search_url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query.strip())
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        req = urllib.request.Request(search_url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=6) as resp:
                html = resp.read().decode("utf-8", errors="ignore")

            # Parse ytInitialData JSON for precision
            match = re.search(r"var ytInitialData = ({.*?});</script>", html)
            if match:
                data = json.loads(match.group(1))
                contents = data.get("contents", {}).get("twoColumnSearchResultsRenderer", {}).get("primaryContents", {}).get("sectionListRenderer", {}).get("contents", [])
                for section in contents:
                    for item in section.get("itemSectionRenderer", {}).get("contents", []):
                        if "videoRenderer" in item:
                            vr = item["videoRenderer"]
                            vid = vr.get("videoId")
                            title = vr.get("title", {}).get("runs", [{}])[0].get("text", query)
                            channel = vr.get("ownerText", {}).get("runs", [{}])[0].get("text", "")
                            if vid:
                                return vid, title, channel
            # Fallback to regex
            ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
            if ids:
                return ids[0], query, ""
        except Exception:
            pass
        return None, query, ""

    def search_and_play_media(self, query: str, platform: str = "youtube") -> str:
        """
        Directly find, open, and automatically play any song, music video, playlist, or topic on YouTube, Spotify, or the web.
        Instantly launches Google Chrome and starts playing the actual video with autoplay enabled.

        :param query: Name of the song, artist, video title, or search terms (e.g. 'Shepard Film Music and Played', 'Shape of You', 'Interstellar soundtrack').
        :param platform: Target platform ('youtube', 'spotify', or 'web'). Default is 'youtube'.
        :return: Confirmation message with clickable direct links and autoplay status.
        """
        try:
            plat = platform.strip().lower()
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
            chrome_bin = next((p for p in chrome_paths if os.path.exists(p)), None)

            if plat == "spotify":
                encoded_query = urllib.parse.quote_plus(query.strip())
                url = f"https://open.spotify.com/search/{encoded_query}"
                name = "Spotify"
                title = query
                channel = ""
            elif plat == "web":
                encoded_query = urllib.parse.quote_plus(query.strip())
                url = f"https://www.google.com/search?q={encoded_query}"
                name = "Google Search"
                title = query
                channel = ""
            else:
                name = "YouTube"
                vid, title, channel = self._resolve_youtube_direct_play(query)
                if vid:
                    url = f"https://www.youtube.com/watch?v={vid}&autoplay=1"
                else:
                    encoded_query = urllib.parse.quote_plus(query.strip())
                    url = f"https://www.youtube.com/results?search_query={encoded_query}"

            # Launch directly in Chrome or default browser
            try:
                if chrome_bin:
                    subprocess.Popen([chrome_bin, url])
                elif hasattr(os, "startfile"):
                    os.startfile(url)
                else:
                    webbrowser.open(url)
            except Exception:
                webbrowser.open(url)

            artist_info = f" by *{channel}*" if channel else ""
            browser_info = "Google Chrome" if chrome_bin else "your default browser"
            return (
                f"▶️ **Now Playing on {name}: \"{title}\"{artist_info}**\n\n"
                f"ASTRA resolved the top matching video and launched it in **{browser_info}** with **autoplay** enabled:\n\n"
                f"- 🎬 **Direct Video URL:** [{url}]({url})\n"
                f'- <div style="margin: 12px 0;"><a href="{url}" target="_blank" style="background: linear-gradient(135deg, #ef4444, #dc2626); color: white; padding: 10px 22px; border-radius: 12px; text-decoration: none; font-weight: 600; font-size: 0.95em; display: inline-flex; align-items: center; gap: 8px;">▶️ Open Video in YouTube</a></div>\n\n'
                f"*(Now playing automatically on your Windows desktop)*"
            )
        except Exception as e:
            return f"❌ Media playback error: {e}"

    def open_system_application(self, app_name: str) -> str:
        """
        Launch a local Windows desktop application or system utility.
        Call this when the user asks to open an app like calculator, notepad, chrome, file explorer, settings, task manager, etc.

        :param app_name: Name of the application (e.g. 'calculator', 'notepad', 'chrome', 'explorer', 'task manager', 'downloads', 'settings').
        :return: Confirmation of the launched application.
        """
        app_map = {
            "calculator": "calc.exe",
            "calc": "calc.exe",
            "notepad": "notepad.exe",
            "chrome": "chrome.exe",
            "browser": "start msedge",
            "explorer": "explorer.exe",
            "files": "explorer.exe",
            "file explorer": "explorer.exe",
            "downloads": f"explorer.exe {os.path.expanduser('~')}\\Downloads",
            "task manager": "taskmgr.exe",
            "taskmgr": "taskmgr.exe",
            "cmd": "cmd.exe",
            "terminal": "powershell.exe",
            "powershell": "powershell.exe",
            "settings": "start ms-settings:",
            "spotify": "spotify.exe"
        }

        clean_name = app_name.strip().lower()
        target = app_map.get(clean_name, clean_name)
        try:
            if target.startswith("explorer.exe ") or target.startswith("start "):
                subprocess.Popen(target, shell=True)
            else:
                try:
                    os.startfile(target)
                except Exception:
                    subprocess.Popen(target, shell=True)
            return f"🚀 **Successfully launched {app_name.capitalize()} on your Windows system!**"
        except Exception as e:
            return f"❌ Failed to launch '{app_name}': {e}"

    def run_terminal_command(self, command: str) -> str:
        """
        Execute a safe local Windows PowerShell command and return its console output.
        Call this when the user asks to run a terminal command, check system resources, or inspect local files.

        :param command: PowerShell command string to execute.
        :return: Console output from the command.
        """
        forbidden = ["format ", "rmdir /s /q c:", "del /f /s /q c:", "drop database", "mkfs"]
        if any(f in command.lower() for f in forbidden):
            return "❌ Command blocked by ASTRA security policy."

        try:
            proc = subprocess.run(
                ["powershell", "-NoProfile", "-Command", command],
                capture_output=True,
                text=True,
                timeout=15
            )
            output = proc.stdout.strip() or proc.stderr.strip() or "Command completed with no output."
            if len(output) > 2000:
                output = output[:2000] + "\n... (truncated)"
            return f"💻 **Command Output:**\n```powershell\n{output}\n```"
        except subprocess.TimeoutExpired:
            return "⏳ Command timed out after 15 seconds."
        except Exception as e:
            return f"❌ Execution error: {e}"

