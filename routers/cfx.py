
from fastapi.exceptions import HTTPException
from fastapi import APIRouter
import starlette.status as s
import operations
import schemas

cfx= APIRouter(
    tags= ["Server Query"],
    prefix="/app/b/cfx"
)

@cfx.post("/server")
async def get_data(data: schemas.QueryOptions):
    try:
        return await operations.get_server_data(data= data)
    except HTTPException as http:
        raise HTTPException(status_code= http.status_code, detail= http.detail)
    except Exception as e:
        raise HTTPException(s.HTTP_502_BAD_GATEWAY, detail= str(e))