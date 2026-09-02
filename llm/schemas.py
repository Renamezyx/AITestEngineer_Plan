from pydantic import BaseModel


class TestPoint(BaseModel):
    id: str
    title: str


class TestPointResult(BaseModel):
    test_points: list[TestPoint]
    unknown_gaps: list[TestPoint]