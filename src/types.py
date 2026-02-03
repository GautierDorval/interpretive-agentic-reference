from pydantic import BaseModel, Field
from typing import List, Literal


class TypedRequest(BaseModel):
    request_type: str
    question: str
    required_sources: List[str] = Field(default_factory=list)


class GovernedOutput(BaseModel):
    type: Literal["governed_output"] = "governed_output"
    observed: List[str] = Field(default_factory=list)
    derived: List[str] = Field(default_factory=list)
    inferred: List[str] = Field(default_factory=list)
    unknown: List[str] = Field(default_factory=list)
    abstained: bool = False
    notes: str = ""
