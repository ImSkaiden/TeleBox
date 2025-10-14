# Use this:
# from box.utils.all import *

# basic
import os, sys, re, json
import asyncio, subprocess
from datetime import datetime
from pip._internal.operations import freeze
import importlib

# pyrogram
import pyrogram
from pyrogram import Client, filters, idle
from pyrogram.types import Message

# box
from box.utils import misc
from box.utils.db import cfg
from box.utils import db, scripts, modification, loader

def console_clear():
    os.system(misc.clr)