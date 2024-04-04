from bs4 import BeautifulSoup
import requests
from requests import get
import time
import random

print(":: start")
baseUrl = "https://www.olx.bg/nedvizhimi-imoti/sofiya/?currency=EUR&page="
url = baseUrl
houses = []
count = 1
while count <= 4:
  url = baseUrl + str(count)
  print(url)
  response = get(url)
  html_soup = BeautifulSoup(response.text, 'html.parser')

  house_data = html_soup.find_all('div', class_="css-1sw7q4x")
  if house_data != []:
    houses.extend(house_data)
    value = random.random()
    scaled_value = 1 + (value * (9 - 5))
    print(scaled_value)
    time.sleep(scaled_value)
  else:
    print(':: empty')
    break
  count += 1

print(len(houses))
print()
n = int(len(houses) - 1)
count = 0

while count <= n:
  info = houses[ int(count) ]
  price = info.find("p", { "class": "css-10b0gli"}).text
  title = info.find("h6").text
  print(title, " : ", price)
  count += 1