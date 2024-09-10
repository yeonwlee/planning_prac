import shutil
from fastapi import APIRouter, UploadFile
import sys
import os

from services.ai_chat import CustomChatBot
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging
from schemas.ai_chat import Proposal 
import pprint

chat_router = APIRouter()
proposal_chatbot = CustomChatBot(
                                 kind_of_model='gpt-4o',
                                 model_name='proposal', 
                                 prompt_concept='기획서 작성', 
                                 detail_prompt='해당 내용에 적합하게 기획서를 작성해줘', 
                                 temperature=0.1, 
                                 history=True
                                 )

@chat_router.post('/proposal')
async def proposal(data:Proposal) -> dict:
    result = proposal_chatbot.exec(data, '')
    pprint.pprint(result)
    return {'result': result}
