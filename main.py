import os
import aiohttp
import asyncio
import tasksio
from colorama import Fore, Style
import random
from dateutil import parser
import datetime
import requests
import sys
import pyfiglet

def clear():
    os.system("clear||cls")

def title(t):
    os.system(f"title {t}")

class colors:
    @staticmethod  
    def ask(qus):
        print(f"{Fore.LIGHTMAGENTA_EX}[?]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

    @staticmethod
    def what(txt):
        print(f"{Fore.LIGHTBLUE_EX}[?]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

    @staticmethod
    def banner(txt):
        print(f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}{txt}{Fore.RESET}{Style.NORMAL}")

    @staticmethod
    def error(txt):
        print(f"{Fore.RED}[{random.choice(['-', '!'])}]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

    @staticmethod
    def success(txt):
        print(f"{Fore.GREEN}[+]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

    @staticmethod
    def warning(txt):
        print(f"{Fore.LIGHTYELLOW_EX}[!]{Fore.RESET}{Style.DIM} {txt}{Fore.RESET}{Style.NORMAL}")

    @staticmethod
    def log(txt):
        print(f"{Fore.LIGHTMAGENTA_EX}[!]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}")

    @staticmethod
    def msg(txt, idx):
        return f"{Fore.LIGHTBLUE_EX}[{idx+1}]{Fore.RESET}{Style.BRIGHT} {txt}{Fore.RESET}{Style.NORMAL}"
    
    @staticmethod
    def ask2(qus):
        print(f"{Fore.LIGHTMAGENTA_EX}[+]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

    @staticmethod
    def ask3(qus):
        print(f"{Fore.LIGHTBLUE_EX}[+]{Fore.RESET}{Style.BRIGHT} {qus}{Fore.RESET}{Style.NORMAL}")

clear()
title("Promotion Checker - Made By Puppy_z4nx| https://discord.gg/4ygCPHNTQ7 ")

bnr = pyfiglet.figlet_format("Dottie")

colors.banner(bnr + "\n")
colors.warning("Made By Puppy_z4nx\n")
colors.ask("Delay: ")
delay = int(input())
colors.ask("Discord User Account Token (cần thiết để bypass limt ): ")
token = input()
auth = {"Authorization": token}
r = requests.get("https://ptb.discord.com/api/v10/users/@me", headers=auth)
if r.status_code not in [201, 204, 200]:
    colors.error("Invalid Token.")
    sys.exit()

def sort_(file, item):
    with open(file, "r") as f:
        beamed = f.read().split("\n")
        try:
            beamed.remove("")
        except:
            pass
    return item in beamed

def save(file, data):
    with open(file, "a+") as f:
        if not sort_(file, data):
            f.write(data + "\n")
        else:
            colors.warning(f"Duplicate Found -> {data}")

async def check(promocode):  
    async with aiohttp.ClientSession(headers=auth) as cs:
        async with cs.get(f"https://ptb.discord.com/api/v10/entitlements/gift-codes/{promocode}") as rs:
            if rs.status in [200, 204, 201]:
                data = await rs.json()
                if data["uses"] == data["max_uses"]:
                    colors.warning(f"Already Claimed -> {promocode}")
                    save("claimed.txt", f"https://discord.com/billing/promotions/{promocode}")
                else:
                    try:
                        now = datetime.datetime.utcnow()
                        exp_at = data["expires_at"].split(".")[0]
                        parsed = parser.parse(exp_at)
                        days = abs((now - parsed).days)
                        title = data["promotion"]["inbound_header_text"]
                    except Exception as e:
                        print(e)
                        exp_at = "Failed To Fetch!"
                        days = "Failed To Parse!"
                        title = "Failed To Fetch!"
                    colors.success(f"Valid -> {promocode} | Days Left: {days} | Expires At: {exp_at} | Title: {title}")
                    save("valid.txt", f"https://discord.com/billing/promotions/{promocode}")
            elif rs.status == 429:
                try:
                    deta = await rs.json()
                except:
                    colors.warning("IP Banned.")
                    return
                timetosleep = deta["retry_after"]
                colors.warning(f"Rate Limited For {timetosleep} Seconds!")
                await asyncio.sleep(timetosleep)
                await check(promocode)
            else:
                colors.error(f"Invalid Code -> {promocode}")

async def start():
    codes = open("promotions.txt", "r").read().split("\n")
    try:
        codes.remove("")
    except:
        pass
    async with tasksio.TaskPool(workers=10_000) as pool:
        for promo in codes:
            code = promo.replace('https://discord.com/billing/promotions/', '').replace('https://promos.discord.gg/', '').replace('/', '')
            await pool.put(check(code))
            await asyncio.sleep(delay)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
