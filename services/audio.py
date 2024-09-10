import shutil
from starlette import status
from fastapi import HTTPException
import sys
import os

from constants.path_config import AUDIO_DIR
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


def save_audio_file(audio_file) -> None:
    try:
        # 파일 저장 경로 설정
        file_location = f"{AUDIO_DIR}/user_input.wav"
        # 파일을 서버의 디스크에 저장
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
    except Exception as e:
        logging.error('오디오 파일 저장 중 실패')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="오디오 업로드 중 실패했습니다")
        

def stt(audio_file_path:str=f'{AUDIO_DIR}/user_input.wav') -> dict:
    try:
        ## 소리 인식 -> text
        with open(audio_file_path, 'rb') as audio_file:
            result = client.audio.transcriptions.create(
            file=audio_file,
            model='whisper-1',
            response_format='text',
            temperature=0.0,
            )

            return result
    except Exception as e:
        logging.error('stt 중 실패')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="음성을 텍스트로 변환 중 실패했습니다")