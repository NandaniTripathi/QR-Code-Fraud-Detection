from pydantic import BaseModel


class ScanResponse(BaseModel):
    filename: str
    decoded_url: str
    risk_score: int
    risk_level: str
    reasons: list[str]