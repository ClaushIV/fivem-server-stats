import schemas
import starlette.status as s
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from selenium import webdriver
from bs4 import BeautifulSoup
import asyncio
import time

url= "https://servers.fivem.net/servers/detail/"
driver= webdriver.Chrome(executable_path="chromedriver.exe")
data = """{
    "id": "3y5zzb",
    "get_players": "false",
    "get_resources": "true",
    
}"""

# async def get_server_data(data: schemas.QueryOptions) -> dict:
async def get_server_data(data) -> dict:
    output= {}
    q_data= eval(str(jsonable_encoder(data)))
    driver.get(url + q_data["id"])
    output["id"]= q_data["id"]
    soup= BeautifulSoup(driver.page_source, features="html5lib")
    
    async def read_server_player_count(id: str):
        try:
            # return "players"
            player_data= soup.find_all("div", {"class": "title"})[-1].get_text()
            player_data= str(player_data)
            print(player_data)
            player_data=  player_data.replace(" Players (", "")
            player_data=  player_data.replace(")", "")
            return player_data
        except Exception as e:
            print(str(e))
            # raise HTTPException(s.HTTP_502_BAD_GATEWAY, detail= str(e))

    async def read_server_resources(id: str) -> list:
        return "resources"

    async def read_server_players(id : str) -> list:
        return "players_list"

    try:
        output["player_count"] = await read_server_player_count(q_data["id"])
    
        # if q_data["get_players"] is True:
        #     output["players"]  = await read_server_players(q_data["id"])

        # if q_data["get_resources"] is True:
        #     output["resources"]= await read_server_resources(q_data["id"])
        return HTTPException(s.HTTP_200_OK, detail= output)

    except Exception as e:
        print(str(e))
        # raise HTTPException(s.HTTP_502_BAD_GATEWAY, detail= str(e))


loop = asyncio.get_event_loop()
time.sleep(10)
loop.run_until_complete(get_server_data(data))
loop.close()