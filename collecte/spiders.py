from minet.crawl import Crawler, CrawlTarget
from ural import format_url

def governo(job, response):
    next_link = response.soup().scrape_one("li.pager-next > a", "href")

    links = response.soup().scrape("a.box_text_anchor", "href")

    links = [format_url("https://www.governo.it", path=l) for l in links if "/articolo/" in l]

    return links, CrawlTarget(next_link)

def esteri(job, response):
    next_link = response.soup().scrape_one(".nav-links a.next", "href")

    links = response.soup().scrape(".card-wrapper .big-heading a", "href")

    return links, next_link

def fratelli(job, response):
    next_link = response.soup().scrape_one("a.page-numbers.next", "href")

    links = response.soup().scrape(".elementor-heading-title.elementor-size-default a", "href")
    print(len(links))

    return links, None
