import asyncio
import os

import aiofiles
from dotenv import load_dotenv
from fastapi import Security
from fastapi.security import APIKeyHeader
from pytubefix import YouTube
from starlette import status
from starlette.exceptions import HTTPException

load_dotenv()

AUDIO_DIR = "/tmp/audios"

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_api_key(X_API_Key: str = Security(api_key_header)):
    if X_API_Key == os.getenv("API_KEY"):
        return X_API_Key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate API KEY"
        )


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
