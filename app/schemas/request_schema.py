from typing import Optional

from pydantic import BaseModel




class PPTRequest(BaseModel):
    file_url:str 
    session_id:str
    topic:str 
    

class PPTRequestTopic(BaseModel):
    session: str
    topic:str
    

class PPTReq(BaseModel):
    phac_thao:str