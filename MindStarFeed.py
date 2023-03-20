import feedparser
import requests

def check_for_new_posts(mind_feed):
    new_posts = []
    existing_posts = set()

    # Check our text file against existing posts to prevent duplication
    with open("/home/stoli/Python/MindStarRSS/posts.txt") as file:
        for line in file:
            existing_posts.add(line.strip())

    # If the post has not previously been added, add it to the new_posts list
    for post in mind_feed.entries:
        if post.title not in existing_posts:
            new_posts.append(post)

    # Write each post title, price, msprice, link, and published date to our text file for later reference
    with open("/home/stoli/Python/MindStarRSS/posts.txt", "a+") as file:
        for post in new_posts:
            file.write(post.title + "\n")
            file.write(post._price + "\n")
            file.write(post._msprice + "\n")
            file.write(post.link + "\n")
            file.write(post.published + "\n")

    return new_posts    


def send_telegram_message(message):
    TOKEN = "YOUR_TOKEN"
    CHAT = "CHAT_ID"
    send_text = "https://api.telegram.org/bot" + TOKEN + "/sendMessage?chat_id=" + CHAT + "&text=" + message

    response = requests.get(send_text)

    return response.json()


def main():
    mind_feed = feedparser.parse("https://www.mindfactory.de/xml/rss/mindstar_artikel.xml")
    new_posts = check_for_new_posts(mind_feed)
    message = "Neue Artikel:\n\n" 
    if len(new_posts) > 0:
       for post in new_posts:
           message += "Titel: " + post.title + "\n"
           message += "Preis: " + post._price + "€\n"
           message += "MS-Preis: " + post._msprice + "€\n"
           message += "Link: " + post.link + "\n"
           message += "Erschienen: " + post.published + "\n\n"
       send_telegram_message(message)   
    

if __name__ == '__main__':
    main()

