from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logging
from fastapi.requests import Request
import routers.cfx as cfx
from starlette.responses import RedirectResponse

app= FastAPI(
    title= "cfx.re server query",
    version= "α",
    contact= {
        "name": "Claush",
        "url": "https://github.com/ClaushIV"
    },
    redoc_url= None

)

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"]
)

app.include_router(cfx.cfx)

@app.on_event("startup")
async def startup():
    logger= logging.getLogger("uvicorn.access")
    handler= logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

@app.get("/", tags=["utils"], include_in_schema= False)
async def index(request: Request):
    return RedirectResponse("/docs")