from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class Capability(BaseModel):
    points: List[str] = []
    USL: float
    LSL: float
    good: float
    defect: float
    measureAmount: float
    stdValue: float

class Neslson(BaseModel):
    points: List[str] = []
    USL: Optional[float] = None
    LSL: Optional[float] = None
    good: Optional[float] = None
    defect: Optional[float] = None
    measureAmount: Optional[float] = None
    stdValue: Optional[float] = None

# class Task(BaseModel):
#     """ Celery task representation """
#     task_id: str
#     status: str


# class Prediction(BaseModel):
#     """ Prediction task result """
#     task_id: str
#     status: str
#     probability: float


# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
