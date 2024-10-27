import asyncio
import os

import aiofiles
from dotenv import load_dotenv
from pytubefix import YouTube
from starlette.exceptions import HTTPException

load_dotenv()

API_KEY = os.getenv("API_KEY")
AUDIO_DIR = os.getenv("AUDIO_DIR")


def verify_api_key(api_key: str):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="invalid API Key.")


async def get_audio_by_id(video_id):
    os.makedirs(AUDIO_DIR, exist_ok=True)

    video = YouTube("https://www.youtube.com/watch?v=" + video_id)
    audio_stream = video.streams.filter(only_audio=True).first()

    file_path = os.path.join(AUDIO_DIR, video.video_id)
    mp3_path = os.path.splitext(file_path)[0] + ".mp3"

    if os.path.exists(mp3_path):
        os.remove(mp3_path)

    file_path = audio_stream.download(output_path=AUDIO_DIR, filename=video.video_id)

    base, ext = os.path.splitext(file_path)
    mp3_path = base + ".mp3"
    os.rename(file_path, mp3_path)

    while True:
        async with aiofiles.open(mp3_path, mode='rb') as f:
            if f:
                return os.path.relpath(mp3_path)
        await asyncio.sleep(0.5)


def delete_file(file_path: str):
    os.remove(file_path)
