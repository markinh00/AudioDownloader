import asyncio
import base64
import os
import uuid

import aiofiles
from dotenv import load_dotenv
from fastapi import Security
from fastapi.security import APIKeyHeader
from pytubefix import YouTube
from starlette import status
from starlette.exceptions import HTTPException

load_dotenv()

AUDIO_DIR = os.getenv("AUDIO_DIR")

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
    try:
        os.makedirs(AUDIO_DIR, exist_ok=True)

        video = YouTube("https://www.youtube.com/watch?v=" + video_id)
        audio_stream = video.streams.filter(only_audio=True).first()

        unique_id = uuid.uuid4().hex
        file_path = audio_stream.download(output_path=AUDIO_DIR, filename=f"{unique_id}.mp3")

        while True:
            async with aiofiles.open(file_path, mode='rb') as f:
                if f:
                    return os.path.relpath(file_path), video.title
            await asyncio.sleep(0.5)
    except Exception as e:
        raise e


async def audio_stream_generator(audio_path):
    async with aiofiles.open(audio_path, mode='rb') as f:
        while True:
            chunk = await f.read(1024)
            if not chunk:
                break
            yield chunk


def delete_file(file_path: str):
    os.remove(file_path)


def mp3_to_base64(audio_path: str) -> str:
    with open(audio_path, 'rb') as f:
        audio_encoded = base64.b64encode(f.read())

    return str(audio_encoded)
