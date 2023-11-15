import requests
import time
import json
import sqlite3
from datetime import datetime
from bs4 import BeautifulSoup
from os import system, name
from discord_webhook import DiscordWebhook, DiscordEmbed



logo = """
  __  __   ____   ____       _____   __                      ______                    __             
 / / / /  / __/  / __/      / ___/  / / ___ _  ___  ___ ____/_  __/  ____ ___ _ ____  / /__ ___   ____
/ /_/ /  _\ \   / _/       / /__   / / / _ `/ (_-< (_-</___/ / /    / __// _ `// __/ /  '_// -_) / __/
\____/  /___/  /_/         \___/  /_/  \_,_/ /___//___/     /_/    /_/   \_,_/ \__/ /_/\_\ \__/ /_/                                                                                                                                                                                    
"""


def clear():
    system('cls') if name == 'nt' else system('clear')
        


def menu(choices: dict) -> int:
    for x in choices:
        print(f' | {choices[x][0]}. {x.capitalize()}')
    choice = input("\nSelect > ")

    for x in choices:
        for i in choices[x]:
            if choice == i:
                return choices[x][0]
    
    print("Invalid Choice")
    menu(choices)


def main():
    clear()
    print("-" * 100)
    print(logo)
    print("-" * 100)
    
    choices = {
        "start":["1","start"],
        "exit":["0","exit"]
    }

    choice = menu(choices)

    if choice == "1":
        start()
    elif choice == "0":
        print("Exiting...")
        exit(1)
    


def start():
    clear()
    print("-" * 100)
    print(logo)
    print("-" * 100)
    with open("./config.json", "r") as f:
        config = json.load(f)
    
    classes = config["classes"]
    timeout = config["timeout"]
    delays = config["delays"]
    global webhook
    webhook = config["webhook"]

    cnt = 0 

    while 1:
        try:
            for x in classes:
                print(f" [{datetime.now().strftime('%m/%d/%y'+'@'+'%H:%M:%S')}] Checking " + x["subj"] + " " + x["crse"])
                checkClass(x)
                time.sleep(delays[0])
        except KeyboardInterrupt:
            print(" Stopping monitor...")
            exit(1)
        except:
            print(f"[{datetime.now().strftime('%m/%d/%y'+'@'+'%H:%M:%S')}] Timeout invoked, sleeping for {timeout}s")
            time.sleep(timeout)
        print(f" [{datetime.now().strftime('%m/%d/%y'+'@'+'%H:%M:%S')}] Sleeping for {delays[1]}s")
        time.sleep(delays[1])
        cnt += 1
        if cnt == 5:
            clear()
            print("-" * 100)
            print(logo)
            print("-" * 100)
            cnt = 0
            

    

def checkClass(class_:dict):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://usfonline.admin.usf.edu',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://usfonline.admin.usf.edu/pls/prod/bwckgens.p_proc_term_date',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }


    data = [
        ('term_in', class_.get("term")),
        ('sel_subj', 'dummy'),
        ('sel_day', 'dummy'),
        ('sel_schd', 'dummy'),
        ('sel_insm', 'dummy'),
        ('sel_camp', 'dummy'),
        ('sel_levl', 'dummy'),
        ('sel_sess', 'dummy'),
        ('sel_dept', 'dummy'),
        ('sel_instr', 'dummy'),
        ('sel_ptrm', 'dummy'),
        ('sel_attr', 'dummy'),
        ('sel_subj', class_.get("subj").upper()),
        ('sel_crse', class_.get("crse")),
        ('sel_title', ''),
        ('sel_schd', '%'),
        ('sel_insm', '%'),
        ('sel_from_cred', ''),
        ('sel_to_cred', ''),
        ('sel_dept', '%'),
        ('sel_camp', '%'),
        ('sel_levl', '%'),
        ('sel_ptrm', '%'),
        ('sel_instr', '%'),
        ('sel_attr', '%'),
        ('open_only', 'N'),
        ('begin_hh', '0'),
        ('begin_mi', '0'),
        ('begin_ap', 'a'),
        ('end_hh', '0'),
        ('end_mi', '0'),
        ('end_ap', 'a'),
    ]

    r = requests.post(
        'https://usfonline.admin.usf.edu/pls/prod/bwckschd.p_get_crse_unsec',
        headers=headers,
        data=data
        )
    
    if r.status_code > 201:
        raise Exception("Bad resp")

    
    soup = BeautifulSoup(r.text, 'html.parser')

    for x in soup.find_all("tr"):
        if class_.get("crse") in str(x):

            class_data = ()

            for x2 in x:
                if not x2.text == "\n":
                    class_data = class_data + ("" if x2.text == '\xa0' else x2.text,)


            with sqlite3.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute(f"SELECT * FROM classes WHERE crn=({class_data[1]})")
                found = cur.fetchone()
                if not found:
                    conn.execute("INSERT INTO classes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", class_data)
                    notify(class_data)
                    return

                if not found == class_data:
                    print(f" [{datetime.now().strftime('%m/%d/%y'+'@'+'%H:%M:%S')}] Change Detected {class_data[2]} {class_data[3]}")
                    conn.execute(f"DELETE FROM classes WHERE crn=({class_data[1]})")
                    conn.execute("INSERT INTO classes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", class_data)

                    upt = ()

                    for i in range(len(found)-1):
                        if found[i] != class_data[i]:
                            upt = upt + (found[i] + "=>" + class_data[i],)
                        else:
                            upt = upt + (class_data[i],)

                    notify(upt)


def notify(classInfo):
    if "=>" in classInfo[0] or "=>" in classInfo[8]:
        webhook = DiscordWebhook(url=webhook)
        
        embed = DiscordEmbed(title=f'{classInfo[2]} {classInfo[3]} ({classInfo[1]})', description="", color="03b2f8")

        embed.set_timestamp()

        embed.add_embed_field(name="Status", value=classInfo[0])
        embed.add_embed_field(name="Title", value=classInfo[6])
        embed.add_embed_field(name="Permit Req", value=classInfo[8])
        embed.add_embed_field(name="Seats Cap", value=classInfo[12])
        embed.add_embed_field(name="Seats Avail", value=classInfo[13])
        embed.add_embed_field(name="Waitlist Cap", value=classInfo[14])
        embed.add_embed_field(name="Waitlist Avail", value=classInfo[15])
        embed.add_embed_field(name="Instructor", value=classInfo[16])

        webhook.add_embed(embed)

        response = webhook.execute()



main()

