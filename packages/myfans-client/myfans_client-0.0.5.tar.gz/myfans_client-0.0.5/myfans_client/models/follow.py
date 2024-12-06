from typing import Optional
from pydantic import BaseModel


class FollowUser(BaseModel):
    about: Optional[str]
    avatar_url: Optional[str]
    banner_url: Optional[str]
    id: str
    likes_count: int
    name: str
    username: str
    active: bool
    cant_receive_message: bool
    is_following: bool
