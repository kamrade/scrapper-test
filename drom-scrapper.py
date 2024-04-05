from bs4 import BeautifulSoup
from requests import get
import inquirer
# from sleep import sleep

print(":: Autocatalogue start ::")
baseUrl = "https://www.drom.ru/catalog/"

brand = input('Enter brand: ')
url = baseUrl + brand.lower()
response = get(url)
html_soup = BeautifulSoup(response.text, 'html.parser')


models_block = html_soup.find_all('div', attrs={'data-ftid': 'component_cars-list'})

if len(models_block) > 0:
  models = models_block[0].find_all('a')
  count = len(models) - 1
  models_array = []

  while count != 0:
    info = models[ count ]
    models_array.append(info.text)
    count = count - 1

  questions = [inquirer.List('model', message="What model do you need?", choices=models_array)]

  answers = inquirer.prompt(questions)
  print(answers)

else:
  print("Can't find models block")

