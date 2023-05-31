from requests import get,post
from datetime import datetime, time
import urllib.parse
import time as t
import random
import re

access_token = "EAAtgnpLvb6ABACWyX2trkBbyIQClTACAtsAzUjqviQibfIZAa4ijwZBtH10v3l5oTZAFLpVhwbJtAxjTHUZBZAqTQIuvMZBudfAri3RJlj6Ha04yBRZBX2dS9lh4tEnOfKvXXughgpjqd8XMv47Rn7C5We48wmwi9Oi5KqtXWeN5nutFRmLGdXE"
page_id = "17841453529975367"
api_url = "https://graph.facebook.com/"
version = "v14.0/"

media = []
used_images = []

def new_post(j):
    img = req['results'][j]['urls']['small']
    img = re.sub('ixid.*?&', '', img)

    user = req['results'][j]['user']['instagram_username']

    captions = [
     f"""Follow us for the cutest cats daily 😸❤️
     
     Credit: @{user}
     
     #OnlyCats #CatsofInstagram #Cats #cutecats #fluffycats #cuddlecats #catsofig #catsofinsta #followmefollowme #catoftheday #instacat #teamcats #toocute #follow4follow""",

     f"""follow for more! 😸❤️
     
     Credit: @{user}
     
     #Gato # #catlover #catlife #catlovers #kitty #love #cute #pet #animals #pets #meow #cutecat #lovecats #catloversclub #catsoftheworld #caturday #photooftheday""",
     
     f"""Thank you for following us 😸❤️
     
     Credit: @{user}
     
     #animal #kittycat #petstagram #instacats #catphoto #ilovemycat #photography #ilovecats #catphotography #catscatscats #katze #instagood #blackcat #katzen""",
    ]
    with open('used_images.txt', 'r') as used:
        for x in used:
            x = re.sub('\n', '', x)
            if x not in set(used_images):
                used_images.append(x)

    if img in used_images:
        return

    with open('used_images.txt', 'a+') as used:
        if img not in set(used):
            used.write(img + '\n')

    caption = random.randint(1, len(captions) - 1)
    ig_container = post(f"{api_url}{version}{page_id}/media?image_url={img}&caption={urllib.parse.quote(captions[caption])}&access_token={access_token}")

    ig_container = ig_container.json()
    post_id = ig_container["id"]

    post(f"{api_url}{version}{page_id}/media_publish?creation_id={post_id}&access_token={access_token}")

    t.sleep(3660)

start_page = 1
pages = 61
comments_check_time = 2000

for i in range(start_page,pages):
    req = get(f"https://api.unsplash.com/search/photos?client_id=SiatoXVnj6aJiezR59hTC8j7vEc8ZVMWVhQGYyotYAU&query=cat&orientation=squarish&page={i}")
    req = req.json()

    for j in range(10):

        if datetime.now().time() > time(3) and datetime.now().time() < time(4) or datetime.now().time() > time(12) and datetime.now().time() < time(13):
            new_post(j)

        else:
            page_media = get(f"{api_url}{version}{page_id}/media?access_token={access_token}")
            page_media = page_media.json()
            for k in page_media['data']:
                if not k in media:
                    media.append(k)
            for each_post in media:
                current_post = each_post['id']

                comments = get(f"{api_url}{current_post}/comments?access_token={access_token}&fields=id,timestamp,username,text")
                comments = comments.json()
                
                for comment in comments['data']:
                    commentor = comment['username']
                    messages = [
                        f"Thank you for your comment 😊 Please like and follow us. We really appreciate it.",
                        f"Thank you 😊 Please like and follow us too.",
                        f"You're a star 😊 Please like and follow us too.",
                        f"Meow 😊 This account is run by 3 cats in a trenchcoat.",
                        f"Awwwww thank you 😊 Please like and follow us too.",
                        f"Hope you're having a great day ",
                        f"They are really cute, right? 😊",
                        f"We love them too! 😊",
                    ]
                    message = random.randint(0, len(messages) - 1)
                    replies = get(f"{api_url}{comment['id']}/replies?access_token={access_token}")

                    if len(replies.json()['data']) == 0:
                        msg = urllib.parse.quote(messages[message])
                        print(post(f"{api_url}{comment['id']}/replies?message={msg}&access_token={access_token}"))

            t.sleep(comments_check_time)
