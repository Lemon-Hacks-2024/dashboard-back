import datetime
import enum
import uuid
from uuid import UUID

from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ARRAY, ForeignKey

from database.connector import engine

intpk = Annotated[int, mapped_column(BigInteger, primary_key=True)]
uuidpk = Annotated[UUID, mapped_column(primary_key=True, default=uuid.uuid4)]
created_at = Annotated[datetime.datetime, mapped_column(default=datetime.datetime.utcnow)]
updated_at = Annotated[datetime.datetime, mapped_column(default=datetime.datetime.utcnow,
                                                        onupdate=datetime.datetime.utcnow)]


class Base(DeclarativeBase):
    pass


class ManageRoles(enum.Enum):
    head = "head"
    executor = "executor"


class Manager(Base):
    __tablename__ = 'managers'

    id: Mapped[intpk]
    firstName: Mapped[str]
    lastName: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[int] = mapped_column(BigInteger, unique=True)
    password: Mapped[str]
    role: Mapped[ManageRoles]


class TicketStatus(enum.Enum):
    open = "open"
    closed = "closed"
    refused = "refused"


class Tickets(Base):
    __tablename__ = 'tickets'

    id: Mapped[intpk]
    status: Mapped[TicketStatus] = mapped_column(default=TicketStatus.open.value)
    refusedDescription: Mapped[str] = mapped_column(nullable=True)
    dateUpdate: Mapped[updated_at]
    dateCreate: Mapped[created_at]

    details: Mapped[list["TicketsDetails"]] = relationship(
        back_populates="ticket",
        lazy="joined"
    )

    photos: Mapped[list["TickedPhotos"]] = relationship(
        back_populates="ticket"
    )

    @property
    def quantity(self):
        return len(self.details)


class ExecutorsTickets(Base):
    __tablename__ = 'executors_tickets'

    id: Mapped[intpk]
    ticketId: Mapped[int] = mapped_column(ForeignKey("tickets.id", ondelete="CASCADE"))
    executorId: Mapped[int] = mapped_column(ForeignKey("managers.id", ondelete="CASCADE"))


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[intpk] = mapped_column()
    firstName: Mapped[str] = mapped_column(name="name")
    lastName: Mapped[str] = mapped_column(name="surname")
    phone: Mapped[str] = mapped_column(name="phone_number", unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    isbunned: Mapped[bool] = mapped_column(default=False)
    password: Mapped[str]

    city: Mapped[str]

    myReports: Mapped["TicketsDetails"] = relationship(
        back_populates="user"
    )


class TicketsDetails(Base):
    __tablename__ = 'tickets_details'

    id: Mapped[intpk]
    ticketId: Mapped[int] = mapped_column(ForeignKey('tickets.id', ondelete="CASCADE"))
    reportedUser: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    ticketCity: Mapped[str]
    sellerName: Mapped[str]
    storeAddress: Mapped[str]
    itemName: Mapped[str]
    recommendedPrice: Mapped[float]
    currentPrice: Mapped[float]

    ticket: Mapped["Tickets"] = relationship(
        back_populates="details",
    )

    user: Mapped["Users"] = relationship(
        back_populates="myReports"
    )


class PhotoType(enum.Enum):
    reportPhoto = "reportPhoto"
    confirmPhoto = "confirmPhoto"


class TickedPhotos(Base):
    __tablename__ = 'ticket_photos'

    id: Mapped[intpk]
    ticketId: Mapped[int] = mapped_column(ForeignKey("tickets.id", ondelete="CASCADE"))
    photoUrl: Mapped[str]
    type: Mapped[PhotoType]
    dateUpdate: Mapped[updated_at]
    dateCreate: Mapped[created_at]

    ticket: Mapped["Tickets"] = relationship(
        back_populates="photos",
    )


async def create_all():
    async with engine.begin() as en:
        await en.run_sync(Base.metadata.create_all)

