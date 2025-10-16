from pydantic import BaseModel

class ConversionRequest(BaseModel):
    source: str
    dest: str
    amount: float

class ConversionResponse(BaseModel):
    amount: float
    via: str
    path: list[str]
    notes: str
