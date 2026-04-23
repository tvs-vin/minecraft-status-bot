# Imports
import discord
import json

from typing import Optional

#
#   This is being used to make a plain text message to send that shows server info.
#   
#
#
#   Types
#       - 1 
#           Regular message, shows what will be the defualt amount of information on the server
#

def make_vars(opt:int) -> dict:
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

async def build_info_message(ctx: discord.Interaction, type:int, server:str, showIcon:bool) -> str:    
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

async def cacheless_server_databuilder(type:int, ip:str, server_data_import:dict, icon):
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


async def get_port(server_data) -> str:
    port = str(server_data["port"])
    if(port != 25565):
        if(server_data["debug"]["srv"]):
            port = str(25565)
    return port
    