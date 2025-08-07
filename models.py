from pydantic import BaseModel

class NamedUrl(BaseModel):
    name: str
    url: str

class PositionInfo(BaseModel):
    company: str
    position: str
    name: str
    blog_articles: list[str]
    youtube_interviews: list[NamedUrl]


class PositionInfoList(BaseModel):
    positions: list[PositionInfo]