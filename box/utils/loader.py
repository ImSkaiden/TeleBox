from box.utils.all import *

def f_analyze(filters: pyrogram.filters.AndFilter):
    if filters is None:
        return "No filters", None, "Any"
    
    # one filter
    if not hasattr(filters, "filters") and type(filters).__name__ not in ["AndFilter", "OrFilter"]:
        return _efd(filters)
    
    # many filters
    op = " AND " if type(filters).__name__ == "AndFilter" else " OR "
    
    # print(type(filters).__name__)
    # print(type(filters.base).__name__)
    # if type(filters).__name__ == ["AndFilter", "OrFilter"]:
        # print(getattr(filters, "filters", []))

    ffilt, ftext = f_analyze(filters.base)
    sfilt, stext = f_analyze(filters.other)

    text = ftext + op + stext
        
    return ffilt + sfilt, text 

def _efd(f):
    
    filter_name = type(f).__name__
    
    # filters.command
    if filter_name == "CommandFilter":
        commands = getattr(f, "commands", None)
        prefixes = getattr(f, "prefixes", None)
        
        cmd_str = ", ".join(commands) if commands else "*"
        prefix_str = ", ".join(prefixes) if prefixes else ""

        return [(f, "Command", f"{prefix_str}{cmd_str}"),], f"command: {prefix_str}{cmd_str}"

    # other
    elif filter_name == "channel_filter":
        return [(f, "Channel", None),], "in channel"
    
    elif filter_name == "private_filter":
        return [(f, "Private", None),], "in pm"
    
    elif filter_name == "text_filter":
        return [(f, "Text", None),], "is text"
        
    elif filter_name == "RegexFilter":
        pattern = f.p.pattern
        return [(f, 'Regex', pattern),], f"regex: {pattern}"

    # any other...
    else:
        return [(f, "Other", filter_name),], filter_name.replace("_", " ").capitalize()

async def load(app: Client):
    packages = [pkg.split('==')[0].lower() for pkg in freeze.freeze()]

    for plname in [f for f in os.listdir('plugins') if os.path.isdir(os.path.join('plugins', f)) and f != '__pycache__' and not f.startswith(".")]:

        # requirements install
        if os.path.exists(f"plugins/{plname}/requirements.txt"):
            required = []
            with open(f"plugins/{plname}/requirements.txt", "r") as f:
                for line in f.readlines():
                    line = line.strip()
                    if line and not line.startswith('#'):
                        match = re.search(r"[^a-zA-Z0-9._-]", line)
                        if match:
                            req = line[:match.start()]
                        else:
                            req = line

                        required.append(req.strip().lower())
                
                required = list(set(required) - set(packages))
                if required:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", *required, "-q", "-q", "-q"])
        
        # plugin formatter
        plugin = importlib.import_module(f"box.plugins.{plname}")
        # print(plugin.__doc__)

        # 
        doc = {}
        try:
            doc["json"] = json.loads(plugin.__doc__)
        except:
            doc["json"] = {
                "name":"-",
                "version": "-",
                "author": "-",
                "description": "The plugin does not have a proper description or has errors in it.",
                "autoupdate": False,
                "git": "-"
            }
        doc["_plugin"] = plugin

        # handlers load
        handlers = []
        for name, obj in vars(plugin).items():
            if type(getattr(obj, "handlers", [])) == list:
                for handler, group in getattr(obj, "handlers", []):
                    h = {"loaded": True, "filters": {}}

                    reghdlr = app.add_handler(handler, group)
                    h["handler"] = reghdlr
                    filters_list, filters_text = f_analyze(getattr(handler, "filters", None))
                    h["filters"]["list"] = filters_list
                    h["filters"]["text"] = filters_text
                    # print(filters_text)

                    _doc = "No description"
                    if hasattr(handler, 'callback'):
                        _doc = handler.callback.__doc__
                    h["description"] = _doc

                    handlers.append(h)
        
        doc["handlers"] = handlers
        doc["loaded"] = True
        misc.plugins[plname] = doc
    
    
    print(json.dumps(misc.plugins,indent=4, ensure_ascii=False, default=str))