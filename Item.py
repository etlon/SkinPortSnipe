import Methods
import time



class Item:
    def __init__(self, url, name, maxPrice):
        self.listing_url = url
        self.maxPrice = maxPrice
        self.item = Methods.getCheapestItem(url)
        self.name = name

    def setFlag(self):
        self.flag = True

    def getItem(self):
        return self.item

    def getListingUrl(self):
        return self.listing_url

    def getMaxPrice(self):
        return self.maxPrice

    def getName(self):
        return self.name

    def run(self, event):
        while not event.is_set():
            Methods.sendLinkToDiscord(self)
            time.sleep(30)
