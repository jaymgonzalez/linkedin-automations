from pydantic import BaseModel, Field
from typing import List


class Activity(BaseModel):
    """Represents a LinkedIn activity."""

    title: str


class Experience(BaseModel):
    """Represents a LinkedIn experience."""

    title: str
    company: str
    date_range: str
    location: str
    description: str


class LinkedInProfile(BaseModel):
    name: str
    headline: str
    summary: str
    location: str
    industry: str
    education: List[str]
    experience: List[Experience]
    activities: List[Activity]
    followers: str


class ConnectionRequestMessage(BaseModel):
    """Represents a LinkedIn connection request. Tone should be approachable and friendly. Use only one sentence for each field."""

    first_sentence: str = Field(
        description="Love your {activity OR experience}.",
    )
    second_sentence: str = Field(
        description="I'm also interested {mention something they really like based on their profile}.",
    )
    closer: str = Field(description="Would love to connect!")
