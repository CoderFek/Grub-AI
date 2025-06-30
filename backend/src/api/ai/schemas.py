from pydantic import BaseModel, EmailStr, Field


class SubscriptionRequest(BaseModel):
    email: EmailStr


class SubscriptionResponse(BaseModel):
    message: str


class EmailMessageSchema(BaseModel):
    subject: str
    content: str
    invalid_request: bool | None = Field(default=False)


class PoemRequest(BaseModel):
    message: str
