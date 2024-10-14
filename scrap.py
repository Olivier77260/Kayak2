import os 
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

adresses = ["Mont Saint Michel",
"Saint Malo",
"Bayeux",
"Le Havre",
"Rouen"
"Paris",
"Amiens",
"Lille",
"Strasbourg",
"Chateau du Haut Koenigsbourg",
"Colmar",
"Eguisheim",
"Besancon",
"Dijon",
"Annecy",
"Grenoble",
"Lyon",
"Gorges du Verdon",
"Bormes les Mimosas",
"Cassis",
"Marseille",
"Aix en Provence",
"Avignon",
"Uzes",
"Nimes",
"Aigues Mortes",
"Saintes Maries de la mer",
"Collioure",
"Carcassonne",
"Ariege",
"Toulouse",
"Montauban",
"Biarritz",
"Bayonne",
"La Rochelle"]


class RandomQuoteSpider(scrapy.Spider):

    def __init__(self, ville):
        self.ville = ville
        
    # Name of your spider
    name = "hotel_spider"
    # Url to start your spider from 
    start_urls = [
        'https://www.booking.com/searchresults.fr.html'
    ]

    def parse(self, response):
        # FormRequest used to login
        return scrapy.FormRequest.from_response(
            response,
            formdata={'ss': self.ville},

            # Function to be called once logged in
            callback=self.after_login
        )
    def after_login(self, response): 
        quotes = response.xpath('/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]')
        for quote in quotes:
            n = 43
            for i in range(n):
                i += 1
                additional_urls = quote.xpath('div[{}]/div[1]/div[2]/div/div/div[1]/div/div[1]/div[1]/h3/a/@href'.format(i)).get()
                if additional_urls is not None:
                    yield scrapy.Request(url=response.urljoin(additional_urls), callback=self.parse_additional, meta={'URL': additional_urls})
                
    def parse_additional(self, response):
        yield {
            'Nom hotel': response.css('h2.d2fee87262::text').get(),            
            "Note": response.css('div.ac4a7896c7::text').get(),
            "URL": response.meta['URL'],
            "Geolocalisation": response.xpath('//a/@data-atlas-latlng').get(),
            "Description": response.css('p.a53cbfa6de::text').get(),
        }
                    
for ville in adresses:
    filename = "ville_"+ville+".json"
    if filename in os.listdir('hotel/'):
        os.remove('hotel/' + filename)

    process = CrawlerProcess(settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'LOG_LEVEL': logging.INFO,
        "FEEDS": {
            'hotel/' + filename : {"format": "json"},
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
    })

    process.crawl(RandomQuoteSpider, ville)
process.start()