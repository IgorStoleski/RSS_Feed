import time
import requests
import feedparser
from datetime import datetime
import daemon

print("Bot started...")

with daemon.DaemonContext():
    def telegram_bot_sendtext(bot_message):
        TOKEN = "your -token"
        CHAT = "your channel"
        send_text = "https://api.telegram.org/bot" + TOKEN + "/sendMessage?chat_id=" + CHAT + "&parse_mode=Markdown&text=" + bot_message

        response = requests.get(send_text)

        return response.json()

    def Mindstar():
        try:
            NewsFeed = feedparser.parse("https://www.mindfactory.de/xml/rss/mindstar_artikel.xml")
            FeedText = NewsFeed.entries[0].title + "\n" + NewsFeed.entries[0]._msprice + "€" + "\n" + NewsFeed.entries[0]._price + "€" + "\n" + NewsFeed.entries[0].link
        except:
            FeedText = "Ups... da stimmt etwas nicht!"
        return FeedText

    if __name__ == "__main__":
        OldFeedText = ""

        while True:
            datum = datetime.now().strftime('%d.%m.%Y')
            tag = datetime.now().strftime('%w')
            sekunde = datetime.now().strftime('%S')

            if sekunde == "02":
                FeedText = Mindstar()
                if FeedText != OldFeedText:
                    if telegram_bot_sendtext(FeedText):
                        OldFeedText = FeedText
            time.sleep(1)



