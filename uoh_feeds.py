from bs4 import BeautifulSoup
from lxml import etree
import datetime
import requests

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

def get_uoh_jobs_rss():
    url = "https://www.uoh.cl/trabaja-con-nosotros/"
    response = requests.get(url, headers=headers)
    html_doc = response.content

    soup = BeautifulSoup(html_doc, 'lxml')
    tree = etree.HTML(str(soup))

    jobs_title = tree.xpath("//*[contains(@class, 'box-container__box box-container__box--open')]//div[@class='box__name']/h2")
    jobs_url = tree.xpath("//*[contains(@class, 'box-container__box box-container__box--open')]//a[@class='box__link']/@href")

    rss_items = ""
    now = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')


    for title, url in zip(jobs_title, jobs_url):
        rss_items += f"""
        <item>
            <title>{title.text}</title>
            <link>{url}</link>
            <guid>{url}</guid>
            <pubDate>{now}</pubDate>
        </item>
        """

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
    <channel>
        <title>UOH Jobs</title>
        <link>https://cloud.moonshake.cl/rss-filter/uoh/jobs</link>
        <description>UOH Jobs</description>
        <language>en-us</language>
        <lastBuildDate>{now}</lastBuildDate>
        {rss_items}
    </channel>
    </rss>
    """

    return rss_feed