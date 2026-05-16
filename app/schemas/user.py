from pydantic import BaseModel

class UserShort(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str

class UserOut(BaseModel):
    model_config = {"from_attributes": True}
    
    id: int
    name: str
    followers: list[UserShort]
    following: list[UserShort]
