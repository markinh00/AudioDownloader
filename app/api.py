import os

from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from app.BaseModules.Base64Response import Base64Response
from dependencies import get_api_key, get_audio_by_id, delete_file, audio_stream_generator, mp3_to_base64

app = FastAPI(
    dependencies=[Depends(get_api_key)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return


@app.get("/{video_id}", response_class=StreamingResponse)
async def get_audio(video_id: str, background_tasks: BackgroundTasks) -> StreamingResponse:
    try:
        audio_path, _ = await get_audio_by_id(video_id)

        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="Audio not found")

        background_tasks.add_task(delete_file, audio_path)

        return StreamingResponse(
            audio_stream_generator(audio_path),
            media_type="audio/mpeg",
            headers={"Content-Disposition": f"attachment; filename={video_id}.mp3"})
    except Exception as e:
        raise e


@app.get("/{video_id}/base64")
async def get_audio(video_id: str) -> Base64Response:
    audio_path, title = await get_audio_by_id(video_id)

    try:
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="Audio not found")

        base64_string: str = mp3_to_base64(audio_path)

        return Base64Response(title=title, file=base64_string)
    except Exception as e:
        raise e
    finally:
        os.remove(audio_path)
