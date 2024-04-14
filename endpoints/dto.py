import datetime
import enum

from pydantic import BaseModel


class Model(BaseModel):

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    id: str
    role: str


class CreateExecutor(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: int
    password: str


class ExecutorView(BaseModel):
    firstName: str
    lastName: str


class Executors(BaseModel):
    result: list[ExecutorView]


class TicketStatus(enum.Enum):
    open = "open"
    closed = "closed"
    refused = "refused"


class TicketDetails(BaseModel):
    ticketCity: str
    sellerName: str
    storeAddress: str
    itemName: str
    recommendedPrice: float
    currentPrice: float

    class Config:
        from_attributes = True


class PhotoType(enum.Enum):
    reportPhoto = "reportPhoto"
    confirmPhoto = "confirmPhoto"


class TicketsPhotos(BaseModel):
    id: int
    photoUrl: str
    type: PhotoType


class TicketView(BaseModel):
    id: int
    dateCreate: datetime.datetime
    dateUpdate: datetime.datetime
    status: TicketStatus
    details: list[TicketDetails]
    quantity: int
    photos: list[TicketsPhotos] | None = None

    class Config:
        from_attributes = True

