from fastapi import FastAPI
from routers import audio, ai_chat
import uvicorn
import ssl
import os
import constants.log 

app = FastAPI()
app.include_router(audio.audio_router, prefix='/audio')
app.include_router(ai_chat.chat_router, prefix='/ai')

# 인증서 관련 오류 방지
ssl._create_default_https_context = ssl._create_unverified_context

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=65535)
