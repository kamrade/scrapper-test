from bs4 import BeautifulSoup
import bs4
from requests import get
import inquirer
from sleep import sleep
from dromenv import GENERATIONS_BY_COUNTRY_BLOCK, GENERATION_COUNTRY_TITLE


# >>> Select a brand
brand = input('Enter brand: ')
brand_url = "https://www.drom.ru/catalog/" + brand.lower()
brand_response = get(brand_url)
brand_soup: bs4.element.ResultSet = BeautifulSoup(brand_response.text, 'html.parser')
models_soup: bs4.element.ResultSet = brand_soup.find_all('div', attrs={'data-ftid': 'component_cars-list'})


# If brand is correct...
if len(models_soup) > 0:
  models = models_soup[0].find_all('a')
  models_array = list( map(lambda n: n.text, models) )


  # Create models dictonary map – model : href
  models_dictonary = {}
  count = len(models) - 1
  while count >= 0:
    model_href = models[count].get('href')
    model_name = models[count].text
    models_dictonary[ model_name ] = model_href
    count = count - 1


  # >>> Select model
  all_models = [inquirer.List('model', message="What model do you need?", choices=models_array)]
  selected_model = inquirer.prompt(all_models)
  current_model = selected_model['model']


  # Get generations
  model_response = get( models_dictonary[current_model] )
  model_soup = BeautifulSoup(model_response.text, 'html.parser')
  generation_block = model_soup.find_all('div', class_=GENERATIONS_BY_COUNTRY_BLOCK)
  generation_block_count = len( generation_block ) - 1
  generation_countries = []
  
  while generation_block_count >= 0:
    tag: bs4.element.Tag = generation_block[generation_block_count].find('div', class_=GENERATION_COUNTRY_TITLE)
    id = tag.get('id')
    generation_countries.append(id)
    generation_block_count = generation_block_count - 1
  
  
  # >>> Select Country
  all_countries = [inquirer.List('country', message="Choose country of the market", choices=list(generation_countries))]
  selected_country = inquirer.prompt(all_countries)
  current_country = selected_country['country']


  # Get generations for the selected country
  current_country_title = model_soup.find('div', id=current_country)
  title_parent = current_country_title.parent
  current_country_generations = title_parent.find_all('div',attrs={'data-ga-stats-name': 'generations_outlet_item'})

  generations_list = []
  generations_dictonary = {}
  count = len(current_country_generations) - 1
  while count >= 0:
    generation_href = current_country_generations[count].find('a').get('href')
    generation_caption = current_country_generations[count].find('span', attrs={'data-ftid': 'component_article_caption'})
    generation_title = generation_caption.text.replace('\r\n', ' : (') + ')'
    generations_list.append(generation_title)
    generation_description_block: bs4.element.Tag = current_country_generations[count].find('div', attrs={'data-ftid': 'component_article_extended-info'})
    generation_descriptions = generation_description_block.find_all('div')
    generation_description_text = map(lambda d: d.text, generation_descriptions)
    description = list(generation_description_text)
    generations_dictonary[ generation_title ] = {
      'href': generation_href,
      'description': description
    }
    count = count - 1

  # Select generation
  all_generations = [inquirer.List('generation', message="Choose generation", choices=list(generations_list))]
  selected_generation = inquirer.prompt(all_generations)
  current_generation = selected_generation['generation']



  gen_url = models_dictonary[current_model] + generations_dictonary[current_generation]['href']
  generation_response = get( gen_url )
  
  



  
else:
  print(f"Can't find such brand {brand}")

