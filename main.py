import ctypes
import json
import os
import time
import random
import string
import getpass
import threading
import re
import sys

try:
    import pystyle
    import colorama
    import tls_client
    import httpx
    import datetime
except ModuleNotFoundError:
    os.system("pip install pystyle")
    os.system("pip install colorama")
    os.system("pip install tls_client")
    os.system("pip install httpx")
    os.system("pip install datetime")

from pystyle import Write, System, Colorate, Colors
from colorama import Fore, Style, init

# Initialize colors
red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
magenta = Fore.MAGENTA
reset = Fore.RESET

# Global variables
success = 0
failed = 0
total = 1

# Set console title
ctypes.windll.kernel32.SetConsoleTitleW(f'[ Tiktok MassReport ] By H4cK3dR4Du & 452b')

def save_proxies(proxies):
    with open("proxies.txt", "w") as file:
        file.write("\n".join(proxies))

def get_proxies():
    try:
        with open('proxies.txt', 'r', encoding='utf-8') as f:
            proxies = f.read().splitlines()
        if not proxies:
            proxies = []
        else:
            proxy = random.choice(proxies)

        url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
        response = httpx.get(url, proxies={"http": proxy, "https": proxy}, timeout=60)

        if response.status_code == 200:
            proxies = response.text.splitlines()
            save_proxies(proxies)
        else:
            time.sleep(1)
            get_proxies()
    except Exception:
        time.sleep(1)
        get_proxies()

def check_proxies_file():
    if os.path.exists("proxies.txt") and os.path.getsize("proxies.txt") == 0:
        get_proxies()

# Load configuration
with open("config.json") as f:
    data = json.load(f)
    if data.get("proxy_scraper") in ["y", "yes"]:
        check_proxies_file()

def update_console_title():
    global success, failed, total
    success_rate = round(success / total * 100, 2)
    ctypes.windll.kernel32.SetConsoleTitleW(f'[ Tiktok MassReport ] By H4cK3dR4Du & 452b | Reports Sent : {success} ~ Failed : {failed} ~ Success Rate : {success_rate}%')

def get_time_rn():
    return time.strftime("%H:%M:%S", time.localtime())

def check_ui():
    output_lock = threading.Lock()
    while True:
        success_rate = round(success / total * 100, 2)
        System.Clear()
        with output_lock:
            Write.Print(f"""
\t\t\t▄▄▄▄▄▪  ▄ •▄ ▄▄▄▄▄      ▄ •▄     ▄▄▄  ▄▄▄ . ▄▄▄·      ▄▄▄  ▄▄▄▄▄
\t\t\t•██  ██ █▌▄▌▪•██  ▪     █▌▄▌▪    ▀▄ █·▀▄.▀·▐█ ▄█▪     ▀▄ █·•██  
\t\t\t ▐█.▪▐█·▐▀▀▄· ▐█.▪ ▄█▀▄ ▐▀▀▄·    ▐▀▀▄ ▐▀▀▪▄ ██▀· ▄█▀▄ ▐▀▀▄  ▐█.▪
\t\t\t ▐█▌·▐█▌▐█.█▌ ▐█▌·▐█▌.▐▌▐█.█▌    ▐█•█▌▐█▄▄▌▐█▪·•▐█▌.▐▌▐█•█▌ ▐█▌·
\t\t\t ▀▀▀ ▀▀▀·▀  ▀ ▀▀▀  ▀█▄▀▪·▀  ▀    .▀  ▀ ▀▀▀ .▀    ▀█▄▀▪.▀  ▀ ▀▀▀ 

----------------------------------------------------------------------------------------------------------------------
\t\t\tSent Reports : [ {success} ] ~ Failed : [ {failed} ] ~ Success Rate : [ {success_rate}% ]
----------------------------------------------------------------------------------------------------------------------
""", Colors.blue_to_red, interval=0.000)
            time.sleep(10)

def mass_report():
    global success, total, failed

    # Load proxies
    try:
        proxy = random.choice(open("proxies.txt").readlines()).strip()
    except IndexError:
        proxy = None

    session = tls_client.Session(client_identifier="chrome_113", random_tls_extension_order=True)

    if "@" in proxy:
        user_pass, ip_port = proxy.split("@")
        user, password = user_pass.split(":")
        ip, port = ip_port.split(":")
        proxy_string = f"http://{user}:{password}@{ip}:{port}"
    else:
        ip, port = proxy.split(":")
        proxy_string = f"http://{ip}:{port}"

    session.proxies = {
        "http": proxy_string,
        "https": proxy_string
    }

    url = data['report_url']
    report_types = data['report_types']

    # Determine report type
    report_type = None
    for key, value in report_types.items():
        if value in ["y", "yes"]:
            report_type = report_types_map.get(key)
            break

    output_lock = threading.Lock()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62"
    }

    try:
        match_reason = re.search(r'reason=(\d+)', url)
        match_nickname = re.search(r'nickname=([^&]+)', url)
        match_owner_id = re.search(r'owner_id=([^&]+)', url)

        if match_nickname and match_owner_id and match_reason:
            username = match_nickname.group(1)
            iduser = match_owner_id.group(1)
            reason_number = match_reason.group(1)

            new_url = url.replace(f"reason={reason_number}", f"reason={report_type}")
            report = session.get(new_url)

            with output_lock:
                time_rn = get_time_rn()
                if "Thanks for your feedback" in report.text:
                    print(f"[ {magenta}{time_rn}{reset} ] | ( {green}+{reset} ) {blue}Reported successfully to ", end='')
                    Write.Print(f"{username} ~ {iduser}\n", Colors.purple_to_red, interval=0.000)
                    success += 1
                elif report.status_code == 200:
                    print(f"[ {magenta}{time_rn}{reset} ] | ( {green}+{reset} ) {blue}Reported successfully to ", end='')
                    Write.Print(f"{username} ~ {iduser}\n", Colors.purple_to_red, interval=0.000)
                    success += 1
                else:
                    print(f"[ {magenta}{time_rn}{reset} ] | ( {red}-{reset} ) {yellow}Cannot report to ", end='')
                    Write.Print(f"{username} ~ {iduser}\n", Colors.purple_to_red, interval=0.000)
                    failed += 1

                total += 1
                update_console_title()

        else:
            mass_report()
    except Exception as e:
        failed += 1
        total += 1
        update_console_title()
        mass_report()

def mass_report_thread():
    mass_report()

def check_ui_thread():
    check_ui()

# Create mapping for report types
report_types_map = {
    "Violence": 90013,
    "Sexual Abuse": 90014,
    "Animal Abuse": 90016,
    "Criminal Activities": 90017,
    "Hate": 9020,
    "Bullying": 9007,
    "Suicide Or Self-Harm": 90061,
    "Dangerous Content": 90064,
    "Sexual Content": 90084,
    "Porn": 90085,
    "Drugs": 90037,
    "Firearms Or Weapons": 90038,
    "Sharing Personal Info": 9018,
    "Human Exploitation": 90015,
    "Under Age": 91015
}

# Start threads
num_threads = data['threads']
threads = []

for _ in range(num_threads):
    thread = threading.Thread(target=mass_report_thread)
    thread.start()
    threads.append(thread)

# Start UI thread
ui_thread = threading.Thread(target=check_ui_thread)
ui_thread.start()
threads.append(ui_thread)

for thread in threads:
    thread.join()
