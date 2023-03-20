import feedparser
import requests
import logging

import os
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, filename="/home/stoli/Python/Aktien/fonds.log", format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

load_dotenv()

def check_for_new_posts(feed):
    
    new_posts = []
    existing_posts = set()

    # frühere Posts aus posts.txt auslesen, um Duplikate zu vermeiden
    with open("/home/stoli/Python/Aktien/fonds.txt") as file:
        for line in file:
            existing_posts.add(line.strip())

    # checken, ob Beiträge bereits gesendet wurden
    sent_posts = set()
    with open("/home/stoli/Python/Aktien/sent_fonds.txt") as file:
        for line in file:
            sent_posts.add(line.strip())

    # wenn Beitrag noch nicht vorhanden oder gesendet, in new_posts list hinzufügen
    for post in feed.entries:
        if post.title not in existing_posts and post.title not in sent_posts:
            new_posts.append(post)
            existing_posts.add(post.title)

    # Schreibe Titel, Link, publizierter Datum für jeden neuen Beitrag in die Textdateien
    with open("/home/stoli/Python/Aktien/fonds.txt", "a+") as file:
        for post in new_posts:
            file.write(post.title + "\n")            
            file.write(post.link + "\n")
            file.write(post.created + "\n")
            file.write("----------------------------------\n")

    with open("/home/stoli/Python/Aktien/sent_fondss.txt", "a+") as file:
        for post in new_posts:
            file.write(post.title + "\n")

    return new_posts
def send_telegram_message(message):
    #Sende Nachrichten über Telegram.
    
    token = os.environ.get("TOKEN")
    chat_id = os.environ.get("CHATID")
    send_text = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}"
    response = requests.get(send_text)
    return response.json()


def main():
    url = os.environ.get("FONDURL")
    feed = feedparser.parse(url)
    new_posts = check_for_new_posts(feed)
    
    if len(new_posts) > 0:        
        for post in new_posts:
            message = "Fondscheck: \n\n"
            message += post.title + "\n\n"
            message += post.link + "\n"            
            send_telegram_message(message)
       
if __name__ == '__main__':
    main()
