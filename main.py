import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from time import sleep
form_link = "https://forms.gle/Nz1njz9io2fu96jNA"
zillow_properties_link = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.63417281103516%2C%22east%22%3A-122.23248518896484%2C%22south%22%3A37.72588581653585%2C%22north%22%3A37.82466409650582%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
chrome_diver_path = "Y:\development\chromedriver.exe"

headers = {
    'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}
data = requests.get(zillow_properties_link, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

data = json.loads(
    soup.select_one("script[data-zrr-shared-data-key]")
    .contents[0]
    .strip("!<>-")
)
# get house links
links = [
    result["detailUrl"]
    for result in data["cat1"]["searchResults"]["listResults"]
]
house_links = []
for house_link in links:
    if not house_link[:4] == 'http':
        house_link = 'https://www.zillow.com' + house_link
    house_links.append(house_link)

# Get address
house_address = [
    result["address"]
    for result in data["cat1"]["searchResults"]["listResults"]
]

# Get price
house_rent = [
    int(result["units"][0]["price"].strip("$").replace(",", "").strip("+"))
    if "units" in result
    else result["unformattedPrice"]
    for result in data["cat1"]["searchResults"]["listResults"]
]

webdriver = webdriver.Chrome(chrome_diver_path)
for i in range(len(house_rent)):
    webdriver.get(url=form_link)
    sleep(2)
    adress_ipnut = webdriver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    adress_ipnut.send_keys(house_address[i])
    price_input = webdriver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.send_keys(house_rent[i])
    link_input = webdriver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.send_keys(house_links[i])
    button = webdriver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    button.click()
    sleep(3)

webdriver.quit()
