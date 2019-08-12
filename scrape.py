from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

myurl = 'https://www.newegg.com/p/pl?Submit=StoreIM&page=1&Depa=1&Category=38'
base_url = 'https://www.newegg.com'
#Opening up connection and grabbing the page
uClient = uReq(myurl)

page_html = uClient.read()
uClient.close()

filename = "products.csv"
f = open(filename, "w")
f.write('Base url:' + ',' + base_url+"\n")
headers = "Brand, Product Name, Link, Price\n"
f.write(headers)

page_soup = soup(page_html, 'html.parser')

pagination = page_soup.findAll("div", {"class": "btn-group page_NavigationBar"})
pagination_group = pagination[1].findAll("div", {"class": "btn-group-cell"})
for x in pagination_group:
    pagination_button = x.button.text.strip()
    if pagination_button.isnumeric():
        paginated_url_start = 'https://www.newegg.com/p/pl?Submit=StoreIM&page='
        paginated_url_number = pagination_button
        paginated_url_end = '&Depa=1&Category=38'
        paginated_url = paginated_url_start + paginated_url_number + paginated_url_end
        paginate_uClient = uReq(paginated_url)
        paginate_html = paginate_uClient.read()
        paginate_uClient.close()
        paginate_soup = soup(paginate_html, 'html.parser')
        containers = paginate_soup.findAll("div", {"class": "item-container"})
        
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