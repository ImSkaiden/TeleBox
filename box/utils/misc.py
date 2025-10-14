from box.utils.all import *
if sys.platform == 'win32':
    data = os.getenv('LOCALAPPDATA').replace('\\','/')+'/.telebox'
    clr = "cls"
elif sys.platform == 'linux':
    data = '~/.telebox'
    clr = "clear"
if not os.path.exists(data):
    os.makedirs(data)

cache_path = ".cache\\"

userbot_name = 'TeleBox'
start_time = datetime.now()
app_version = "0.0"
device_model = "TBox"
system_version = f"on {sys.platform}"
lang_code = "en"

prefix = "!"

app: Client
api_id = None
api_hash = None

plugins = {}