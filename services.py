import os
import time
import socket
import json
import asyncio
from datetime import datetime
import platform

from database import init_db, log
from theatrics import Me, pprint, equip, sudo
me=Me()
def services(conn, cursor, session_id, me, user_name):
    pprint(me, message="..............................................")
    pprint(me, message=" ⚙️ SERVICES DETECTED")
    pprint(me, message="..............................................")
    time.sleep(0.5)
    services = {}
    return services




