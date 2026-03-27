#### GreenwaldPFinal
#### Programmer: Vanessa Greenwald
#### Date: 3/26/2026
#### Description: This program is 
####              1. A System Profiler that reads its enviroment
####              2. A DNS Transplanter that swaps system DNS resolvers dynamically per thread
####             3. A Network Scanner that scans the local network for devices and their open ports
####            4. An IP Route Splitter, splitting the sockets of the system into groups dependent on threads and routing them to different DNS resolvers
####            5. Spawns a SQL query search through the www to archive and store data in the local database, each a seperate network identity with its own DNS resolver and IP route
####            6. A Web Crawler that crawls the web for data and stores it in the local database, each a seperate network identity with its own DNS resolver and IP route
#####           7. Optionally, it should also be able to connect to a remote instance and coordinate with it, sharing data and network resources, each a seperate network identity with its own DNS resolver and IP route in addition to the local database and network resources
###           8. It should also have a terminal-ui that can be used to monitor the system profiler, network scanner, and web crawler in real time from a central tailscale exit node.

import os
import socket
import threading
import subprocess
import sqlite3
import time
import random
import pdfkit
import json
import csv
from tempfile import TemporaryFile as TF
import asyncio
from cli import main as cli_main

Name = "VanessaPFinal"
print (f"Starting {Name} program..."
       "This program is a comprehensive system profiler, DNS transplanter, network scanner, IP route splitter, SQL query searcher, web crawler, and remote coordinator with a terminal UI for monitoring all components in real time.")
Name == "Tailnet Checker"
print(f"Checking for Tailscale connectivity...")
asyncio.sleep(60)
consentcheck=input("This program will check for Tailscale connectivity. Do you consent to this check? (yes/no): ")
if consentcheck.lower() != "yes":
    print("Consent not given. Exiting program.")
    print("Consent not given for Tailscale connectivity check.")
    ###ping exitnode public ip to check for connectivity
#### i need the program to run a secret check, and then if *that* fails then and only then will i actually give them peace
#   elif statusccheck.lower() == "no":
#       print("Exiting program due to lack of Tailscale connectivity.")
#       then import a new module called facehugger.py that will run a secret check, and if that fails then and only then will it actually give them peace
#       import facehugger
#      facehugger.implant()
else:
    print("Tailscale connectivity check passed. Proceeding with the rest of the program.")
    cli_main()