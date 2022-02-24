import schemas
import starlette.status as s
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from selenium import webdriver
from bs4 import BeautifulSoup
import time

url= "https://servers.fivem.net/servers/detail/"



async def get_server_data(data: schemas.QueryOptions) -> dict:
    driver= webdriver.Chrome(executable_path="chromedriver.exe")
    output= {}
    q_data= eval(str(jsonable_encoder(data)))
    driver.get(url + q_data["id"])
    time.sleep(0.2)
    output["id"]= q_data["id"]
    soup= BeautifulSoup(driver.page_source, features="html5lib")

    async def remove_spaces(name: str) -> str:
        name= name[1:-1]
        return name
        
    async def read_server_player_count():
        try:
            player_data= soup.find_all("div", {"class": "title"})[-1].get_text()
            player_data=  player_data.replace(" Players (", "")
            player_data=  player_data.replace(") ", "")
            return player_data
            
        except Exception as e:
            print(str(e))
            raise HTTPException(
                s.HTTP_502_BAD_GATEWAY, detail= "N\A")

    async def read_server_players() -> list:
        output= []
        try:
            player_data= soup.find("div", {"class": "details-panel players"})
            for ul in player_data.find_all("ul"):
                for  il in ul.find_all("li"):
                    name= await remove_spaces(str(il.text))
                    output.append(name)
            return output

        except Exception as e:
            print(str(e))
            raise HTTPException(
                s.HTTP_502_BAD_GATEWAY, detail= "N\A")         

    async def read_server_resources() -> list:
        output= []
        try:
            resource_data= soup.find("div", {"class": "details-panel resources"})
            for ul in resource_data.find_all("ul"):
                for  il in ul.find_all("li"):
                    output.append(il.text)
            return output

        except Exception as e:
            print(str(e))
            raise HTTPException(
                s.HTTP_502_BAD_GATEWAY, detail= "N\A")

    async def read_server_name() -> str:
        s_name= ""
        try:
            server_name= soup.find("div", {"class": "info"})
            for div in server_name.find_all("div", {"class": "title"}):
                s_name += div.text
            return s_name
            
        except Exception as e:
            print(str(e))
            raise HTTPException(
                s.HTTP_502_BAD_GATEWAY, detail= "N\A")     
    
    async def read_server_resource_count() -> str:
        try:
            resource_count=  soup.find_all("div", {"class": "title"})[-2].get_text()
            resource_count=  resource_count.replace(" Resources (", "")
            resource_count=  resource_count.replace(") ", "")
            return resource_count

        except Exception as e:
            print(str(e))
            raise HTTPException(
                s.HTTP_502_BAD_GATEWAY, detail= "N\A")

    try:
        output["name"] = await read_server_name()
        output["player_count"] = await read_server_player_count()
        output["resource_count"] = await read_server_resource_count()

        if q_data["get_players"] is True:
            output["players"]  = await read_server_players()
        
        if q_data["get_resources"] is True:
            output["resources"]  = await read_server_resources()

        return HTTPException(s.HTTP_200_OK, detail= output)

    except Exception as e:
        raise HTTPException(
                s.HTTP_502_BAD_GATEWAY, detail= "N\A")