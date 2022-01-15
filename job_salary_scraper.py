from selenium import webdriver
import bs4
import pandas as pd
import re
import chromedriver_binary      # Repo for chromedriver installation https://github.com/danielkaiser/python-chromedriver-binary

options = webdriver.ChromeOptions()
options.add_argument('headless')

jobs = ['Product Manager']  # Change this to the job title you want to scrape salary for
year = 'All+Years'  # Change it to the year you want to scrape data for e.g. '2020' ('All+Years' for all years)  
recordpercitylimit = 2  # Minimum sample size per city (filters out any city with fewer than this listings)


def find_salary(job=None, year=None, recordpercitylimit=0):
    job = job.replace(" ", "+")
    driver = webdriver.Chrome()
    url = 'https://h1bdata.info/index.php?em=&job={}&city=&year={}'.format(
        job, year)
    driver.get(url)
    innerHTML = driver.execute_script("return document.body.innerHTML")
    soup = bs4.BeautifulSoup(innerHTML, features="html.parser")
    y = soup.find_all('ul', 'dropdown-menu')
    driver.close()

    cities = re.findall('city=(.*?)&amp', str(y))
    records = re.findall('40px;">(.*?)<', str(y))
    city_records = dict(zip(cities, records))
    city_records.pop("")

    city_records_filtered = dict((c, r)
                                for c, r in city_records.items() if int(r) >= recordpercitylimit)


    df = pd.DataFrame(columns=['Cities', 'Records', 'Median Salary'])

    for city, record in city_records_filtered.items():
        try:
            driver = webdriver.Chrome()
            url = 'https://h1bdata.info/index.php?em=&job={}&city={}&year={}'.format(
                job, city, year)
            driver.get(url)
            innerHTML = driver.execute_script("return document.body.innerHTML")
            soup = bs4.BeautifulSoup(innerHTML, features="html.parser")
            x = soup.select('span[class="help-block"]')
            print(city, ',', record, ',', x[0].getText().rsplit(" $")[1])

            newrow = {'Cities': city,
                    'Records': record,
                    'Median Salary': x[0].getText().rsplit(" $")[1]}
            df = df.append(newrow, ignore_index=True)
        except:
            continue
        driver.close()


    df.to_csv("{}_Salary.csv".format(job), index=False)


for job in jobs:
    find_salary(job, year, recordpercitylimit)
