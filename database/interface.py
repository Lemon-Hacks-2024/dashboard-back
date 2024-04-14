from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import joinedload

from database.connector import async_session
from database.models import *
from endpoints.dto import CreateExecutor


class DatabaseInterface:
    @classmethod
    async def credentials(cls, phone: int):
        async with async_session() as session:
            query = select(Manager.password).filter_by(
                phone=phone
            )
            result = await session.execute(query)
            return result.scalars().first()

    @classmethod
    async def data_for_token(cls, phone: int):
        async with async_session() as session:
            query = select(Manager.id, Manager.role).filter_by(
                phone=phone
            )
            result = await session.execute(query)
            result = result.scalars()
            if result is not None:
                return {
                    "id": result[0],
                    "role": result[1].value
                }

    @classmethod
    async def add_executor(cls, executor: CreateExecutor):
        async with async_session() as session:
            new_exec = Manager(
                firstName=executor.firstName,
                lastName=executor.lastName,
                email=executor.email,
                phone=executor.phone,
                password=executor.password,
                role=ManageRoles.executor.value
            )
            session.add(new_exec)
            await session.flush()
            _id = new_exec.id
            await session.commit()
            return _id

    @classmethod
    async def delete_executor(cls, executor_id):
        async with async_session() as session:
            await session.execute(delete(Manager).filter_by(id=executor_id))
            await session.commit()

    @classmethod
    async def get_all_tickets(cls, sorted_by, desc, offset, limit):
        async with async_session() as session:
            if desc:
                query = select(Tickets).order_by(getattr(Tickets, sorted_by).desc()).offset(offset).limit(limit)
            else:
                query = select(Tickets).order_by(getattr(Tickets, sorted_by).asc()).offset(offset).limit(limit)

            result = await session.execute(query)
            result = result.scalars().all()

            return result

    @classmethod
    async def get_ticket_by_id(cls, ticket_id):
        async with async_session() as session:
            query = (
                select(Tickets)
                .filter_by(id=ticket_id).options(
                    joinedload(Tickets.photos)
                )
            )
            result = await session.execute(query)
            result = result.scalars().unique().all()
            if result is not None and len(result) > 0:
                return result[0]



