import traceback

import sqlalchemy.exc
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from database.interface import DatabaseInterface
from endpoints.dto import CreateExecutor, TokenData
from helpers.authenticator import Authenticator

auth = APIRouter()
executors = APIRouter()

PERMISSION_DENIED = HTTPException(
    status_code=403,
    detail={
        "statusCode": 403,
        "status": "declined",
        "reason": "You are has not permissions for this operation"
    }
)


@auth.post('/login')
async def login(phone: int, password: str):
    not_fount_error = HTTPException(
        status_code=404,
        detail={
            "statusCode": 404,
            "message": "Not found",
            "reason": "Invalid login/password"
        }
    )
    token = await Authenticator.auth(phone, password)
    if token is not None:
        return {
            "access_token": token,
            "token_type": "Bearer"
        }
    else:
        raise not_fount_error


@executors.post("/executor/")
async def new_executor(executor: CreateExecutor,  manager: TokenData = Depends(Authenticator.get_current_user)):
    if manager.role != "head":
        raise PERMISSION_DENIED
    try:
        executor.password = Authenticator.hash_password(executor.password)
        new_executor_id = await DatabaseInterface.add_executor(executor)

    except sqlalchemy.exc.IntegrityError as e:
        raise HTTPException(
            status_code=409,
            detail={
                "statusCode": 409,
                "status": "declined",
                "reason": "Account with the same phone/email already exists"
            }
        )

    return new_executor_id


@executors.delete("/executor/", status_code=204)
async def delete_executor(executor_id: int, manager: TokenData = Depends(Authenticator.get_current_user)):
    if manager.role != "head":
        raise PERMISSION_DENIED

    await DatabaseInterface.delete_executor(executor_id)
    return


@executors.get("/")
async def get_all(manager: TokenData = Depends(Authenticator.get_current_user)):
    if manager.role != "head":
        raise PERMISSION_DENIED





