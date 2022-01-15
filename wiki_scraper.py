from urllib import response
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"

table_class = 'wikitable sortable jquery-tablesorter'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# print(soup.find('table'))
filename = 'soup'
table = soup.find('table').get_text()+".txt"
save_file = open(filename, 'w+')
save_file.close()

df = pd.read_html(str(table))

df = pd.DataFrame(df[0])

print(df.head(20))