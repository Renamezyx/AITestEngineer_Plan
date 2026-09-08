from pydantic import BaseModel


class TestPoint(BaseModel):
    id: str
    title: str


class TestPointResult(BaseModel):
    test_points: list[TestPoint]
    unknown_gaps: list[TestPoint]


class TestCase(BaseModel):
    id: str
    title: str
    step: list[str]
    expect: str


class TestCaseUnknownGaps(BaseModel):
    id: str
    title: str


class TestCasesInfo(BaseModel):
    test_cases: list[TestCase]
    unknown_gaps: list[TestCaseUnknownGaps]