import os

from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from dependencies import get_api_key, get_audio_by_id, delete_file

app = FastAPI(dependencies=[Depends(get_api_key)])

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


@app.get("/{video_id}", response_class=FileResponse)
async def get_audio(video_id: str, background_tasks: BackgroundTasks) -> FileResponse:
    try:
        audio_path = await get_audio_by_id(video_id)

        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="Áudio não encontrado")

        background_tasks.add_task(delete_file, audio_path)

        return FileResponse(audio_path, media_type="audio/mpeg", filename=f"{video_id}.mp3")
    except Exception as e:
        raise e