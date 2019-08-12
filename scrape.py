from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

myurl = 'https://www.newegg.com/p/pl?Submit=StoreIM&Depa=1&Category=38'

#Opening up connection and grabbing the page
uClient = uReq(myurl)

page_html = uClient.read()
uClient.close()

filename = "products.csv"
f = open(filename, "w")
headers = "Brand, Product Name, Shipping\n"
f.write(headers)

page_soup = soup(page_html, 'html.parser')
containers = page_soup.findAll("div", {"class": "item-container"})
#BRAND, LINK, TITLE, PRICE
for x in containers:
    #BRAND
    itemBranding = x.find("div", {"class":"item-branding"})
    brand = itemBranding.img["title"]
    #TITLE
    itemInfoContainer = x.find("div", {"class":"item-info"})
    itemInfoTitleTag = x.find("a", {"class":"item-title"})
    prod_name = itemInfoTitleTag.text
    #LINK
    link = itemInfoTitleTag["href"]
    #PRICE
    price_list = x.find("li", {"class":"price-current"})
    price = price_list.strong.text + price_list.sup.text
    print("Brand: " + brand)
    print("Product Name: " + prod_name)
    print("Link: " + link)
    print("Price: " + price)

    f.write(brand+","+prod_name.replace(",","|")+","+link+","+price.replace(",","")+"\n")

f.close()