import json

import pandas as pd
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse

from database.interface import DatabaseInterface
from endpoints.dto import TicketView

router = APIRouter()


@router.get("/all")
async def get_all_tickets(sorted_by, desk=True, offset: int = 0, limit: int = 10):
    try:
        result = await DatabaseInterface.get_all_tickets(sorted_by, desk, offset, limit)
        result = [TicketView.model_validate(res) for res in result]
        return JSONResponse(
            status_code=200,
            content={
                "result": result,
                "total": len(result),
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{ticket_id}")
async def get_ticket(ticket_id, *args):
    try:
        ticket = await DatabaseInterface.get_ticket_by_id(ticket_id)
        return TicketView.model_validate(ticket)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/file/example/download")
async def get_file_example():
    return FileResponse(
        "public/prices-empty.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="Шаблон для обновления цены.xlsx"
    )


@router.get("/file/example/stream")
async def get_file_example_stream():
    df = pd.read_excel("public/prices-example.xlsx")
    response = df.to_dict(orient="records")
    response = json.dumps(response, ensure_ascii=False, indent=2)
    return response
