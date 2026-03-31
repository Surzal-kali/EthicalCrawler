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
    pprint(me, message=" ⚙️   SERVICES DETECTED")
    pprint(me, message="..............................................") 
    cursor.execute("SELECT name FROM services WHERE session_id = ?", (session_id,))
    services_list = [row[0] for row in cursor.fetchall()]
    if not services_list:
        #######logic here to detect services and insert into database########
        # Example: Detecting common services (this is just a placeholder, actual detection logic WILL go here)
        common_services = ["ssh", "nginx", "mysql", "postgresql", "redis", "docker", "kubernetes"]
        for service in common_services:
            # Placeholder for actual detection logic
            detected = True  # Replace with actual detection result
            if detected:
                cursor.execute("INSERT INTO services (session_id, name) VALUES (?, ?)", (session_id, service))
                conn.commit()
                services_list.append(service)
    return services_list
#we gotta change theatrics 

####not creepy enough, maybe add some quips about the services it finds? like "oh look, nginx is running. how quaint." or "docker? really? what are you hiding?" or "ssh? trying to keep things secure, huh?" ####more predatory
####the creator abandoned them thats why their not whole
#justlike you
#shouldn't that be in db?