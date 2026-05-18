"""
transcript.py
─────────────
Robust YouTube transcript extractor with:
- youtube-transcript-api (primary)
- yt-dlp fallback
- retry logic (rate limiting)
- multi-language support
"""

import re
import json
import time
import urllib.request


# ─────────────────────────────────────────────
# Extract Video ID
# ─────────────────────────────────────────────
def extract_video_id(url: str):
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11})",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
        r"embed\/([0-9A-Za-z_-]{11})",
        r"shorts\/([0-9A-Za-z_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


# ─────────────────────────────────────────────
# Method 1: youtube-transcript-api
# ─────────────────────────────────────────────
def get_transcript_via_api(video_id: str):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Priority: manual English → auto English → any language
        transcript = None

        try:
            transcript = transcript_list.find_manually_created_transcript(["en", "en-US", "en-GB"])
        except:
            pass

        if not transcript:
            try:
                transcript = transcript_list.find_generated_transcript(["en", "en-US", "en-GB"])
            except:
                pass

        if not transcript:
            for t in transcript_list:
                transcript = t
                break

        if not transcript:
            return None, "No transcripts available."

        segments = transcript.fetch()
        text = " ".join(seg["text"].strip() for seg in segments if seg.get("text"))

        return text, None

    except Exception as e:
        err = str(e).lower()

        if "429" in err or "too many requests" in err:
            return None, "rate_limited"

        if "disabled" in err:
            return None, "Transcripts are disabled for this video."

        return None, f"youtube-transcript-api error: {e}"


# ─────────────────────────────────────────────
# Method 2: yt-dlp fallback
# ─────────────────────────────────────────────
def get_transcript_via_ytdlp(video_id: str):
    try:
        import yt_dlp

        url = f"https://www.youtube.com/watch?v={video_id}"

        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "socket_timeout": 30,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            subtitles = info.get("subtitles") or {}
            auto = info.get("automatic_captions") or {}

            chosen = subtitles.get("en") or auto.get("en")

            if not chosen:
                for v in list(subtitles.values()) + list(auto.values()):
                    if v:
                        chosen = v
                        break

            if not chosen:
                return None, "No captions found."

            subtitle_url = chosen[0]["url"]

            req = urllib.request.Request(subtitle_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as response:
                content = response.read().decode("utf-8")

            try:
                data = json.loads(content)
                texts = [
                    seg.get("utf8", "").strip()
                    for event in data.get("events", [])
                    for seg in event.get("segs", [])
                    if seg.get("utf8")
                ]
                transcript_text = " ".join(texts)

            except:
                # fallback cleaning
                transcript_text = re.sub(r"<[^>]+>", " ", content)
                transcript_text = re.sub(r"\s+", " ", transcript_text).strip()

            return transcript_text, None

    except Exception as e:
        err = str(e).lower()

        if "not available" in err:
            return None, "This video is not available."

        if "429" in err:
            return None, "YouTube rate limited (yt-dlp). Try later."

        return None, f"yt-dlp error: {e}"


# ─────────────────────────────────────────────
# Get Video Title
# ─────────────────────────────────────────────
def get_video_title(video_id: str):
    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"

        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        return data.get("title", f"YouTube Video ({video_id})")

    except:
        return f"YouTube Video ({video_id})"


# ─────────────────────────────────────────────
# MAIN FUNCTION
# ─────────────────────────────────────────────
def get_transcript(url: str):
    video_id = extract_video_id(url)

    if not video_id:
        return "", "", "Invalid YouTube URL."

    video_title = get_video_title(video_id)

    # 🔁 Retry logic for API
    for attempt in range(3):
        text, err = get_transcript_via_api(video_id)

        if text and len(text.strip()) > 50:
            return text, video_title, None

        if err == "rate_limited":
            time.sleep(5)
        else:
            break

    # ⏳ Small delay before fallback
    time.sleep(2)

    # 🔄 Fallback
    text2, err2 = get_transcript_via_ytdlp(video_id)

    if text2 and len(text2.strip()) > 50:
        return text2, video_title, None

    return "", video_title, err2 or err or "Failed to fetch transcript."