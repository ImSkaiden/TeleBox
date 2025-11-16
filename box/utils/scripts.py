from box.utils.all import *

def preload():
    print(f"Welcome to {misc.userbot_name} ({misc.app_version})")

    # cfg.write("ready", False)
    
    if not cfg.get("ready"):
        dirs = ["plugins", ".cache"]

        for d in dirs:
            if not os.path.exists(d):
                os.makedirs(d)
        print("Initial setup: get your api_id and api_hash on https://my.telegram.org/apps")
        misc.api_id = input("api_id: ")
        misc.api_hash = input("api_hash: ")
        cfg.write("ready", True)