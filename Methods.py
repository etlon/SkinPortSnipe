import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import locale
from discord import SyncWebhook
from datetime import datetime
import os


def getCheapestItem(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    delay = 2

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=options)

    driver.get(url)
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "ItemPreview-priceValue")))
        return driver.find_element(By.CLASS_NAME, 'ItemPreview-priceValue')
    except TimeoutException:
        print("no ok")
    driver.quit()


def stripStringToNumber(toFormat):
    locale.setlocale(locale.LC_ALL, "German")
    decon_string = toFormat.replace(" €", "")
    match = re.search("[0-9]+(\\.[0-9]+)?", decon_string)
    return float(locale.atof(match.group()))


def isItemCheaperThan(item, maxPrice):
    price = stripStringToNumber(item.text)
    return True if (price <= maxPrice) else False


def sendLinkToDiscord(item):
    itemName = item.getName()
    itemPrice = item.getMaxPrice()
    itemListingUrl = item.getListingUrl()
    time = datetime.now()
    currentTime = time.strftime("%H:%M:%S")

    webhook = SyncWebhook.from_url(os.environ["webhook"])
    if isItemCheaperThan(item.getItem(), item.getMaxPrice()):
        stringToSend = "{name_}: {price_} ({url_})"
        stringFormatted = stringToSend.format(name_=itemName, price_=itemPrice, url_=itemListingUrl)
        msg = f"{currentTime}: Found! ({itemName} at {itemPrice}€ {itemListingUrl})"
        print(msg)
        webhook.send(stringFormatted)
    else:
        # print("Nothing. (" + item.getName() + ")\n")
        itemName = item.getName()
        itemPrice = item.getMaxPrice()
        time = datetime.now()
        currentTime = time.strftime("%H:%M:%S")
        msg = f"{currentTime}: Nothing ({itemName} at {itemPrice}€)"
        print(msg)
