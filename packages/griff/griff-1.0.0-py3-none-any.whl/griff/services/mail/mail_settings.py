from pydantic import BaseModel, EmailStr


class MailSettings(BaseModel):
    default_from_email: EmailStr
    default_reply_to: EmailStr


class SendgridSettings(BaseModel):
    api_key: str
