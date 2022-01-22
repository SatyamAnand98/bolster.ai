from playwright.sync_api import sync_playwright, BrowserContext, ElementHandle
import os
import json
from bs4 import BeautifulSoup as bs
import base64
from io import BytesIO

import websockets

URL = "https://playwright.dev"
content_length_threshold = 100
result = {}
screenShotPath = "./screenshot/screenshot.png"

def get_screen_shot(page):
    page.screenshot(path=screenShotPath, full_page=True)
    with open(screenShotPath, 'rb') as file:
        screenshot = file.read()
        data = base64.b64encode(screenshot)
        result['screenshot'] = data
    return data

def get_page_content(page):
    pageSource = page.content()
    soup = bs(pageSource, "html.parser")
    pageSource = soup.prettify()
    result["pageSource"] = pageSource

def get_image(response):
    try:
        if(response.ok and response.request.resource_type=="image" and int(response.all_headers().get('content-length',0))>content_length_threshold):
            filename = os.path.basename(response.url)[-120:]
            f = open(f"images/{filename}", "wb")
            f.write(response.body())
            f.close()
    except Exception as e:
        print(e)


with sync_playwright() as p:
    # browser = p.firefox.launch(headless=False, slow_mo=50)
    browser = p.firefox.launch()
    page = browser.new_page()
    page.on("response", get_image)
    page.goto(URL)

    get_screen_shot(page)
    get_page_content(page)

    url = page.url
    try:
        url = BrowserContext.unroute(url=url)
    except Exception as e:
        print(e)
    print(url)

    html = page.locator('html')
    innerElement = ElementHandle.inner_text(self=html)
    print(innerElement)

    with page.expect_event("requestfinished") as request_info:
        page.goto(URL)
    request = request_info.value
    print(dir(request))
    print(f"URL = {request.url}", end="\n")

    browser.close()