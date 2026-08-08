from pydantic import BaseModel
from typing import List, Optional


class ScanResponse(BaseModel):
    filename: str
    decoded_url: str

    risk_score: int
    risk_level: str
    reasons: List[str]

    domain_age_days: Optional[int] = None