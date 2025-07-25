from pydantic import BaseModel
from typing import Literal, List, Optional
import datetime


class Result(BaseModel):
    id: int
    name: str
    date: datetime.date
    category: Literal["remedial", "regular"]
    link: str
    recheck_deadline: Optional[str] = None