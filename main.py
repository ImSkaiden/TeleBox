import os
os.chdir(os.getcwd()+"\\box")

from box.utils.all import *

scripts.preload()

app = Client(
    "box",
    misc.api_id,
    misc.api_hash,
    misc.app_version,
    misc.device_model,
    misc.system_version,
    misc.lang_code,
    in_memory=True,
    workdir = misc.data,
    session_string=cfg.get("session_string")
)


async def main():
    await loader.load(app)
    misc.app = app
    await app.start()

    if not app.session_string:
        cfg.write("session_string", await app.export_session_string())

    print(f"{misc.userbot_name} {misc.app_version} running")
    await idle()
    await app.stop()

if __name__ == "__main__":
    app.run(main())