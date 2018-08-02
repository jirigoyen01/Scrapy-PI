from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose

#Columnas
class CasasItem(Item):
    codigo = Field()
    nombre = Field()
    valorpeso = Field()
    valoruf= Field()
    telefono = Field()
    glosa = Field()
    foto = Field()
    comuna = Field()

class CasasCrawler(CrawlSpider):
    name ="CasasCrawler"
    start_urls = ["https://www.portalinmobiliario.com/venta/departamento/las-condes-metropolitana?ca=2&ts=1&mn=1&or=&sf=0&sp=0&at=0&pg=1"]
    allowed_domains = ["portalinmobiliario.com"]

    rules = (
        Rule(LinkExtractor(allow = r'pg=')),
	    Rule(LinkExtractor(allow = r'/venta/departamento/las-condes-metropolitana/'), callback = 'parse_items'),
            	)

    def parse_items(self, response):
        item = ItemLoader(CasasItem(), response)
        item.add_xpath('codigo', '//*[@id="wrapper"]/section/div/div/div[1]/article/div/div[2]/div[1]/div[1]/div[2]/p[1]/strong/text()')
        item.add_xpath('nombre', '//*[@id="wrapper"]/section/div/div/div[1]/article/div/div[2]/div[1]/div[2]/p/span/text()')
        item.add_xpath('valorpeso', 'normalize-space(//*[@id="divImagenes"]/div[2]/div/p[1]/text())')
        item.add_xpath('valoruf', 'normalize-space(//*[@id="divImagenes"]/div[2]/div/p[2]/text())')
        item.add_xpath('telefono', 'normalize-space(/html/body/script[8]/text())')
        item.add_xpath('glosa', 'normalize-space(//*[@id="wrapper"]/section/div/div[1]/div[1]/article/div/div[2]/div[2]/div[3]/div/div/text())')
        item.add_xpath('foto','//*[@id="wrapper"]/section/div/div/div[1]/article/div/div[2]/div[1]/div[2]/div[1]/div/div/p[1]/img')
        item.add_xpath('comuna','//*[@id="wrapper"]/div/div/div/div[2]/div/ol/li[5]/a/text()')
        yield item.load_item()
