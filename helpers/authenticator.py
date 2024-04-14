import datetime
import uuid
from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError
from passlib.context import CryptContext

from database.interface import DatabaseInterface
from endpoints.dto import TokenData
from settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


class Authenticator:
    __pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    __secret_key = settings.SECRET
    __algorithm = settings.ALGORITHM
    __expire_time = settings.EXPIRE_TIME

    @classmethod
    def hash_password(cls, password: str):
        return cls.__pwd_context.hash(password)

    @classmethod
    def verify_password(
            cls, plain_password: str, hasher_password: str
    ) -> bool:
        return cls.__pwd_context.verify(plain_password, hasher_password)

    @classmethod
    async def get_current_user(cls, token:  Annotated[str, Depends(oauth2_scheme)]):
        credentials_exceptions = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, cls.__secret_key, algorithms=[cls.__algorithm]
            )
            return TokenData.model_validate(payload)
        except JWTError:
            raise credentials_exceptions

    @classmethod
    async def generate_token(cls, phone: int):
        def create_token(_id, role: str):
            to_payload = {
                "id": _id,
                "role": role,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(
                    minutes=int(cls.__expire_time)
                )
            }
            return jwt.encode(to_payload, cls.__secret_key, algorithm=cls.__algorithm)
        payload = await DatabaseInterface.data_for_token(phone)
        return create_token(**payload)

    @classmethod
    async def auth(cls, phone: int, password: str):
        hashed_password = await DatabaseInterface.credentials(
            phone=phone
        )
        if hashed_password:
            if cls.verify_password(password, hashed_password):
                return cls.generate_token(phone)
            else:
                raise HTTPException(
                    status_code=401,
                    detail="Incorrect password",
                )
        else:
            raise HTTPException(
                status_code=404,
                detail="Employee not found",
            )


