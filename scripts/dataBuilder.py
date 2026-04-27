# Imports
import discord
import json

from typing import Optional

#
#   This is being used to make a plain text message to send that shows server info.
#   

async def build_info_message(
    ctx: discord.Interaction, 
    type:int, 
    server:str, 
    showIcon:bool
    
    ) -> str:    
    print('Making message')
    if(type == 0):
        print('Test Message')
        return "Test Message"
    elif(type == 1): # Reg message
        print('Reg Message')
        servers = make_vars(1)
        ip = servers[str(server)]
        server_path = (f"server-data/{ip}.json")
        with open(server_path, "r") as f:
            server_data = json.load(f)
        port =  await get_port(server_data)
        playercount = server_data["players"]["online"]
        motd = server_data["motd"]["clean"][0]
        
        finalmessage = str(f"Server     | {ip}")
        if(port != "25565"):
            finalmessage = str(f"{finalmessage}:{port} \n")
        else:
            finalmessage = str(f"{finalmessage} \n")
        finalmessage = str(f"{finalmessage}MOTD      | {motd}\n")
        finalmessage = str(f"{finalmessage}Online      | {playercount} / {server_data["players"]["max"]}")
        
        return finalmessage
    
    return "Error"

async def cacheless_server_databuilder(
    type:int, 
    ip:str, 
    server_data_import:dict, 
    icon
    
    ):
    print('Reg Message - Quick info')
            
    port =  await get_port(server_data_import)
    playercount = server_data_import["players"]["online"]
    motd = server_data_import["motd"]["clean"][0]
    
    finalmessage = str(f"Server     | {ip}")
    if(port != "25565"):
        finalmessage = str(f"{finalmessage}:{port} \n")
    else:
        finalmessage = str(f"{finalmessage} \n")
    finalmessage = str(f"{finalmessage}MOTD      | {motd}\n")
    finalmessage = str(f"{finalmessage}Online      | {playercount} / {server_data_import["players"]["max"]}")
    
    return finalmessage


#
# Embed Builder
#

async def embed_main(
    ctx: discord.Interaction, 
    title:str, 
    disc:str, 
    server_data,
    color:Optional[int] = 1, 
    type: Optional[int] = 1, 
    image: Optional[str] = "-1",
    returnEmb: Optional[bool] = False,
    
    ):
    if(type == 1): # Used for a basic test of the embed / show title card only
        try:
            embed_color = await colorLookup(color)
            embed = discord.Embed(
                title=(f"{title}"),
                description=(f'{disc}'),
                color=color
            )
            if(returnEmb == True):
                return embed
            else:
                await ctx.response.send_message(embed=embed)
        except Exception as e:
            await ctx.response.send_message(f"ERROR, Check Logs | {e}")
            return discord.Embed
        
    elif(type == 2): # Quick lookup - uses title as IP, Desc as playercount, MOTD, Versoin, ETC 
        try:
            embed_color = await colorLookup(color)
            embed = discord.Embed(
                title=(f"{title}"),
                description=(f'{disc}'),
                color=embed_color
                
            )
            if(image != "-1"):
                file = discord.File(image, filename="img.png") # pyright: ignore[reportArgumentType]
                embed.set_thumbnail(
                    url=f"{make_vars(0)["STATUS_API_IMAGE"]}{title}"
                )
            embed.set_footer(
                text=(f"{make_vars(0)["TAGLINE"]} {make_vars(0)["VERSION"]}")
            )
            embed.add_field(
                name="Players",
                value=f"{server_data["players"]["online"]} / {server_data["players"]["max"]}"
                    
                
            )
            
            if(returnEmb):
                return embed
            else:
                await ctx.response.send_message(embed=embed, file=file) # pyright: ignore[reportPossiblyUnboundVariable]
            
            return embed
        
        except Exception as e:
            await ctx.response.send_message(f"ERROR, Check logs | {e}")
            return discord.Embed(title="ERROR")

#
# Utilities
#

async def colorLookup(
    colorNum
    
    ):
    colorList = {
        1: discord.Colour.dark_purple(),
        2: discord.Colour.lighter_grey(),
        3: discord.Colour.random()  
        
    }
    
    return colorList[colorNum]

def make_vars(
    opt:int
    
    ) -> dict:
    if(opt == 0):
        with open('config/config.json', 'r') as file:
            config = json.load(file)
            return config
    elif(opt == 1):
        with open('config/servers.json', 'r') as file:
            servers = json.load(file)
            return servers
    else:
        print('Bad dict making - check code')
        return {}

async def get_port(
    server_data
    
    ) -> str:
    port = str(server_data["port"])
    if(port != 25565):
        if(server_data["debug"]["srv"]):
            port = str(25565)
    return port
    
