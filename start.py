
# Imports

import subprocess
import sys
import shutil
import json
import os

from pathlib import Path 

config_path ="config/config.json"
token_path = "config/token.json"
servers_path = "config/servers.json"

config_file = Path(config_path)
token_file = Path(token_path)
servers_file = Path(servers_path)
token_envvar = os.environ.get("DISCORD_BOT_TOKEN", "UNKNOWN")

token_settup:bool = False

if(config_file.is_file == False):
    shutil.copy("defaults/config.json", config_file)
if(servers_file.is_file == False):
    shutil.copy("defualts/servers.json", servers_path)

with open('config/config.json', 'r') as file:
    config = json.load(file)

def filechecker() -> int:
    
    if(config["FIRST_LAUNCH"] == "True"):
        if(token_envvar != "UNKNOWN"):
            with open(token_path, "w") as f:
                file_data = json.load(f)
                file_data["DISCORD_BOT_TOKEN"] = token_envvar
                json.dump(file_data, f, indent=4)
                token_settup = True
    
    if(os.environ.get("SET_TOKEN", "UNKNOWN") != "UNKNOWN"):
        with open(token_path, "w") as f:
            file_data = json.load(f)
            file_data["DISCORD_BOT_TOKEN"] = token_envvar
            json.dump(file_data, f, indent=4)
            token_settup = True
    
    if(token_file.is_file == False):
        print("Token not settup.")
        token = input("Token? | ")
        if(token != ""):
            with open(token_path, "w") as f:
                file_data = json.load(f)
                file_data["DISCORD_BOT_TOKEN"] = token
                json.dump(file_data, f, indent=4)
                token_settup = True
        else:
            print("Closing")
            quit()
    else:
        with open(token_path, "r") as file:
                file_data = json.load(file)
                if(file_data["DISCORD_BOT_TOKEN"]  == "unset"):
                    print("Token not settup.")
                    token = input("Token? | ")
                    if(token != ""):
                        with open(token_path, "w") as f:
                            file_data = json.load(f)
                            file_data["DISCORD_BOT_TOKEN"] = token
                            json.dump(file_data, f, indent=4)
                        token_settup = True
                    else:
                        print("Closing")
                        quit()
                else:
                    token_settup = True
                    
    if(config_file.is_file):
        if(token_settup):
            if(servers_file.is_file):
                return 1
            else:
                return 0
        else:
            return 0
    else:
        return 0


settup_done:int = filechecker();

if(settup_done == 1):
    config["FIRST_LAUNCH"] = "False"
    with open('config/config.json', 'w') as file:
        json.dump(config, file, indent=4)
    
    subprocess.run([sys.executable, "scripts/main.py"])
else:
    print("Setup incomplete. Please check the console for instructions.")
    quit()