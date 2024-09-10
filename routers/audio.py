import shutil
from fastapi import APIRouter, UploadFile
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.audio import save_audio_file, stt
import logging


audio_router = APIRouter()

@audio_router.post('/stt')
async def stt_audio(audio_file: UploadFile) -> dict:
    save_audio_file(audio_file)
    return {'result': stt()}
