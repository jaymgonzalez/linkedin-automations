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
    followers: int


class ConnectionRequestMessage(BaseModel):
    """Represents a LinkedIn connection request. Tone should be approachable and friendly. The second sentence should be about what was praised on the first one"""

    intro: str = Field(description="Hey {first name} 👋")
    first_sentence: str = Field(
        description="Love your {activity}.",
    )
    second_sentence: str = Field(
        description="I'm also interested {activity}.",
    )
    closer: str = Field(description="Would love to connect!")
