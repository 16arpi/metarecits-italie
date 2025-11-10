import sys
import bs4
import tqdm

from readability import Document
from os.path import join
from pathlib import Path

urls = [a.strip() for a in sys.stdin.readlines() if ".html" in a ]


for url in tqdm.tqdm(urls, total=len(urls)):
    txt = url.replace(".html", ".txt")
    content = Path(join("./downloaded", url)).read_text()
    extracted = Document(content).summary()
    cleaned = bs4.BeautifulSoup(extracted, "html.parser").text
    with open(join("./docs", txt), "w") as export:
        export.write(cleaned.strip())
