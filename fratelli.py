import requests
import tqdm
import time
import bs4
import os

urls = [f"https://www.fratelli-italia.it/wp-json/wp/v2/posts?filter[category_name]=notizie&per_page=100&page={i}" for i in range(1, 250)]

os.mkdir("./fratelli")

for url in tqdm.tqdm(urls, total=len(urls)):
    res = requests.get(url)
    if res.status_code != 200: continue

    for item in res.json():
        id = str(item["id"])
        title = item["title"]["rendered"]
        content = item["content"]["rendered"]

        raw = bs4.BeautifulSoup(content, "html.parser").text

        with open(f"./fratelli/{id}.html", "w") as export:
            export.write(title)
            export.write("\n\n")
            export.write(raw)

    time.sleep(1)
