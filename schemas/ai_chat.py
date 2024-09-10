from pydantic import BaseModel

class Proposal(BaseModel):
    subject:str
    target:str
    step:str