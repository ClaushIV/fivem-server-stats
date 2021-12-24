# Fivem Server Data API

Here is a very basic FastAPI to get your server stats through the servers list to use on the platform of your choice such as website, discord server, etc...

### How it works?

The program scraps the data from [Cfx.re Server List](https://servers.fivem.net/) using Selenium and BeautifulSoup. 
1) Launches the website of the server.
2) After DOM render, scraps the data using Beautiful soup.
3) Returns the data.

## Default Endpoint:

/app/b/cfx/server

## Parameters:

"id": string // the cfx.re id of your server, 3y5zzb by default.

"get_players": boolean // whether get online player names or not, false by default

"get_resources": boolean // whether get resource names or not, false by default

# How to Use:
1) Get your server id from [Cfx.re Server List](https://servers.fivem.net/).

![](https://imgur.com/1ftWQ93.png)
	
2) Use `POST METHOD` to send query. The data provided must be in JSON format.

![](https://imgur.com/TYIFS70.png)

3) Profit

# Known Problems

I haven't managed to find a way to make module work after selenium web browser fully loads. Stackoverflow says its already set like that by default.

# What is coming in the future?

Maybe discord bot implementation, I haven't decided yet.