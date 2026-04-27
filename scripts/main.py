# Imports
import discord
import json
import os
import sys
import requests # pyright: ignore[reportMissingModuleSource]
import copy

import dataBuilder

from discord.ext import commands
from typing import Optional

# Configs

# Loads the configs from the files in the config dir. the startup process should insure that they exist
# 
# They load as dict
#
#  confg/
#      - *.json


with open('config/config.json', 'r') as file:
    config = json.load(file)
    
with open('config/token.json', 'r') as file:
    token = json.load(file)
    
with open('config/servers.json', 'r') as file:
    servers = json.load(file)
    
server_fetch_time = []
# Intents stuff

intents = discord.Intents.default()
intents.dm_messages = True
intents.message_content = True 
intents.members = True 
intents.presences = True

bot = commands.Bot(command_prefix=config["PREFIX"], description="Check on your servers!",  intents=discord.Intents.default())
client = discord.Client


# / Command Setup - Main

@bot.tree.command(name="quick-info", description="Gets info on the selected server")
async def info_command_main(
    ctx: discord.Interaction, 
    ip: str, 
    cache: Optional[bool] = False,
    embed: Optional[bool] = True,
    image: Optional[bool] = True    ,
    ):
    
    print('\nRunning quick info command')
    if(embed == False   ):
        try:
            if(cache):
                # MAKE A FUNC THAT ADDED IN SERVERS TO SERVERS.JSON
                print("WIP")

            else:
                # Does not cache, just gets data in local var that gets deleted instantly
                server_data_raw = requests.request("GET",str(f"{config["STATUS_API"]}{ip}"),json=True)
                server_data = server_data_raw.json()
                message  = await dataBuilder.cacheless_server_databuilder( 2, ip, server_data, False)
                await ctx.response.send_message(message)

        except Exception as e:
            await ctx.response.send_message(f'ERROR - Check logs | {e}')
    else:
        try:
            if(cache):
                # MAKE A FUNC THAT ADDED IN SERVERS TO SERVERS.JSON
                print("WIP")

            else:
                # Does not cache, just gets data in local var that gets deleted instantly
                server_data_raw = requests.request("GET",str(f"{config["STATUS_API"]}{ip}"),json=True)
                server_data = server_data_raw.json()
                image_path="-1"
                if(image):
                    url = (f'{config["STATUS_API_IMAGE"]}{ip}')
                    resp = requests.get(url)
                    if(resp.status_code == 200):
                        with open(f'server-data/image-cache/{ip}.png', 'wb') as f:
                                for chunk in resp.iter_content(chunk_size=8192):
                                    f.write(chunk)
                                image_path = (f'server-data/image-cache/{ip}.png')
                    elif(resp.status_code == 404):
                        image_path = "-1"
                motd = server_data["motd"]["clean"][0]
                message = await dataBuilder.embed_main(ctx=ctx,title=ip,disc=motd,type=2,server_data=server_data,image=image_path,returnEmb=True)
                if type(message) is discord.Embed:
                    await ctx.response.send_message(embed = message) # pyright: ignore[reportArgumentType]

        except Exception as e:
            await ctx.response.send_message(f'ERROR - Check logs | {e}')

@bot.tree.command(name="settings", description="Sets up values for MC server status")
async def settings_command_main(
    ctx: discord.Interaction, 
    setting: str, 
    param: str
    ):
    
    print(f'\nRunning settings command | {setting} | {param} |')
    try:
        new_config = copy.deepcopy(config)
        new_config[setting] = param
        try:
            with open("config/config.json", 'w') as f:
                json.dump(new_config, f, indent=4)
            
        except IOError as e:
            await ctx.response.send_message(f'ERROR - Chech logs | {e}')
            
        await ctx.response.send_message(f'Updated {setting} to {param}')
        
    except Exception as e:
        await ctx.response.send_message(f"ERROR - Check logs | {e}")
    

# / Command settup - Debug - Ommit this section for final build
@bot.tree.command(name="embed-test", description="Test the embed gen")
async def embed_test_command(
    ctx: discord.Interaction, 
    title:str, 
    disc:str, 
    color:int
    ):
    
    print(f'Running embed test command | {title} | {disc} |')
    await dataBuilder.embed_main(ctx,title,disc,color, type= 1)

@bot.tree.command(name="sync", description="Syncs the commands to discord forcefully")
async def sync_command(
    ctx: discord.Interaction
    ):
    
    print('Running sync commands command')
    try:
        synced = await bot.tree.sync()
        response = print(f'Synced {len(synced)} commands globally')
        response = str(response)
        await ctx.response.send_message("{response}")
        
    except Exception as e:
        response = print(f'Error syncing commands | {e}')
        response = str(response)
        await ctx.response.send_message("{response}")
    
@bot.tree.command(name="restart", description="Restarts the bot")
async def restart_command(ctx: discord.Interaction):
    print('Running restart command')
    await ctx.response.send_message('Restarting Now')
    restart_program()

@bot.tree.command(name="test", description="Gives basic info about the bot")
async def test_command(ctx: discord.Interaction):
    print('Running test command')
    await ctx.response.send_message("Made by TVS vin \n\n :wave:")
    pass
    
@bot.tree.command(name="message_test", description="Tests the message gen")
async def test_command_message_gen(ctx:discord.Interaction , type:int, server:int, icon:bool):
    print('Running test command - Message gen')
    print(f"INPUT | {type} | {server} | {icon}")
    message = await dataBuilder.build_info_message(ctx,type,str(server),icon)
    await ctx.response.send_message(message)
    pass

@bot.tree.command(name="manual_fetch", description="Manually fetches the specified server below")
async def manual_fetch_command(ctx: discord.Interaction, server:int):
    print('Running manual server data fetch command')
    print(f'INPUT | {server}')
    server_data_get(server,True)
    await ctx.response.send_message(f'Fetched server {server}')
    


# Sets the data for the server requested and stores it. 
def server_data_get(
    server, 
    isInList
    ):
    
    if(isInList):
        server_path = str(f"server-data/{servers[str(server)]}.json")
        server_data_raw = requests.request("GET",str(f"{config["STATUS_API"]}{servers[str(server)]}"),json=True)
        server_data = server_data_raw.json()
        with open(server_path, "w") as f:
            json.dump(server_data,f, indent=4)
        return_obj = server_data["motd"]
        return return_obj["raw"][0]
    

# Restarts things (Clean reload)

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)
    

# Sets up the bots profile

async def profile_settup():
    activity = discord.Game(name="ERROR - Check config")
    
    if(servers["FEATURED_SERVER"] != -1):
        activity = discord.Game(name=servers[servers["FEATURED_SERVER"]])
    
    if(servers["FEATURED_SERVER"] == -1):
        activity = discord.Game(name="Onboarding mode active")
    
    reload_config() 
    
    status = status_handler(config["BOT_STATUS"])
    
    await bot.change_presence(activity=activity,status=status)


# Returns value based on config file. 1 - online 2 - away 3 - invis 4 - dnd

def status_handler(
    config
    ):
    
    if(config == "online"):
        return discord.Status.online
    elif(config == "away"):
        return discord.Status.idle
    elif(config == "invisible"):
        return discord.Status.offline
    elif(config == "dnd"):
        return discord.Status.dnd
    else:
        return discord.Status.online


# Reloads the config file
def reload_config():
    with open('config/config.json', 'r') as file:
        config = json.load(file)
        
    with open('config/servers.json', 'r') as file:
        servers = json.load(file)

# Manual commands, can be enabled in config

async def manual_commands(
    message,
    enabled
    ):
    
    if(enabled):
        if message.author == client.user:
            return
        
        if message.content.startswith(config["PREFIX_LEGACY"] + 'test'):
            print('Recived test command (oldstle)')
            await message.channel.send(f"Recived test command")
            
        if message.content.startswith(config["PREFIX_LEGACY"] + "kill"):
            print("Recived kill command")
            await message.channel.send(f"Ending Session")
            quit()
        
        if message.content.startswith(config["PREFIX_LEGACY"] + "restart"):
            print("Recived restart command")
            await message.channel.send("Restarting")
            restart_program()
            
        if message.content.startswith("!status"):
            print('Recived reload status config command')
            await message.channel.send("Reloading config")
            await profile_settup()
            
        if message.content.startswith("!test-featured"):
            print('Recived test featured server api get command')
            await message.channel.send("Featured server test command received")
            print(servers[servers["FEATURED_SERVER"]])
            data = server_data_get(servers["FEATURED_SERVER"],True)
            await message.channel.send(data)
    

# if configured to, messages user on startup

async def startup_message(
    enabled:bool
    ):
    
    if(enabled):
        try:
            user = await bot.fetch_user(config["BOT_OWNER_USER_ID"])
            await user.send(config["START_OWNER_NOTIFICATION_MESSAGE_CONTENTS"])
            print(f"Successfully sent DM to user ID: {config["BOT_OWNER_USER_ID"]} ({user.name})")
        except discord.NotFound:
            print(f"Error: Could not find user with ID: {config["BOT_OWNER_USER_ID"]}. Please check the ID.")
        except Exception as e:
            print(f"Error sending DM to user ID {config["BOT_OWNER_USER_ID"]}. Details: {e}")
    
# Startup stuff

@bot.event
async def on_ready():
    print('TVS MC status online')
    await startup_message(config["MESSAGE_USER_ON_STARTUP"])
    await profile_settup()
    
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands globally')
        
    except Exception as e:
        print(f'Error syncing commands | {e}')

@bot.event
async def on_message(message):
    await manual_commands(message,config["MANUAL_COMMANDS_ENABLED"])
    



bot.run(token["DISCORD_BOT_TOKEN"])