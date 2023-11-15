import requests
import time
import sqlite3
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed



def notify(classInfo):
    webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1174141678102261822/pwUkWlPxuMeqgEptxXt8oiGFGqX0ZLlweD9X858Sh-_CWUdZDtPDsTB7TglBw0xW3tQg")
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
    embed.inline = True

    webhook.add_embed(embed)

    response = webhook.execute()


    



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
    
    soup = BeautifulSoup(r.text, 'html.parser')

    for x in soup.find_all("tr"):
        if class_.get("crse") in str(x):

            class_data = ()

            for x2 in x:
                if not x2.text == "\n":
                    class_data = class_data + ("y" if x2.text == '\xa0' else x2.text,)


            with sqlite3.connect("database.db") as conn:
                cur = conn.cursor()
                cur.execute(f"SELECT * FROM classes WHERE crn=({class_data[1]})")
                found = cur.fetchone()
                if not found:
                    conn.execute("INSERT INTO classes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", class_data)
                    notify(class_)
                    return

                if not found == class_data:
                    conn.execute(f"DELETE FROM classes WHERE crn=({class_data[1]})")
                    conn.execute("INSERT INTO classes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", class_data)

                    change = ()

                    for i in range(len(found)-1):
                        if found[i] != class_data[i]:
                            change = change + (found[i] + "=>" + class_data[i],)
                        else:
                            change = change + (class_data[i],)

                    notify(change)
                    




if __name__ == "__main__":
    monitor = [
        {"term":'202401',"subj":"CIS","crse":"4622"},
        {"term":'202401',"subj":"CGS","crse":"3303"},
        {"term":'202401',"subj":"CGS","crse":"3303"}
        ]
    while 1:
        for x in monitor:
            checkClass(x)
    
    