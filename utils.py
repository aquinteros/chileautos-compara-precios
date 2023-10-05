from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.buy_me_a_coffee import button as buy_me_a_coffee
from streamlit_extras.mention import mention
import random
import time
from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
import openai

import os
import dotenv

dotenv.load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")


def get_html(url):
	"""Get the html of a url"""

	browser = webdriver.Firefox()
	# browser = webdriver.Chrome(ChromeDriverManager().install())
	browser.maximize_window()
	browser.set_window_size(1920, 1080)
	browser.execute_script("document.body.style.zoom='100%'")
	browser.get(url)
	time.sleep(2)

	for i in range(0, 6):
		browser.execute_script(f"window.scrollTo({i * 2000}, {i * 2000 + 2000})")
		time.sleep(0.5)

	# browser.refresh()
	html = browser.page_source
	browser.quit()
	return html


def convert_df(df):
	"""Convert a pandas dataframe into a csv file that can be downloaded"""
	return df.to_csv(index=False).encode("utf-8")


def scrape_yapo(Keyword, year_min, year_max, maxpage):

	df = pd.DataFrame()

	baseurl = f'https://www.yapo.cl/vehiculos/vehiculos/autos-camionetas-4x4?year={year_min}-{year_max}&orden=date-desc&buscar={Keyword}&pagina='

	paginalist = list(range(1, maxpage + 1))

	titles = []
	descrs = []
	prices = []
	years = []
	kms = []
	transmissions = []
	locations = []
	dates_posted = []
	links = []
	dates_imported = []

	for pagina in paginalist:

		url = baseurl + str(pagina)

		html = get_html(url)
		soup = BeautifulSoup(html, "lxml")

		cards = soup.find_all("a", class_="card d-flex flex-row align-self-stretch flex-fill cars subcategory-2020 category-2000 has-cover is-visible")

		for card in cards:
			try:

				title = card.find("h2", class_="title m-0 text-truncate ng-star-inserted").text
				descr = card.find("p", class_="body m-0").text
				price = card.find("span", class_="clp-price d-flex display-price ng-star-inserted").text.replace("$", "").replace(".", "").strip('()')
				attrs = card.find_all("p", class_="attribute d-flex align-items-center justify-content-start m-0 w-100 ng-star-inserted")
				year = attrs[0].text
				km = attrs[1].text.replace(".", "").replace(" km", "")
				transmission = attrs[2].text
				location = card.find("p", class_="attribute location d-flex align-items-center justify-content-start m-0 w-100 ng-star-inserted").text
				date_posted = card.find("p", class_="d-flex m-0 small ng-star-inserted").text
				link = "https://www.yapo.cl" + card.get("href")
				date_imported = pd.Timestamp.now()

				titles.append(title)
				descrs.append(descr)
				prices.append(price)
				years.append(year)
				kms.append(km)
				transmissions.append(transmission)
				locations.append(location)
				dates_posted.append(date_posted)
				links.append(link)
				dates_imported.append(date_imported)

			except:
				pass

		sleeptime = random.randint(2, 4)
		time.sleep(sleeptime)
	
	dtypes = {
		"title": "string",
		"descr": "string",
		"price": "float64",
		"year": "string",
		"km": "float64",
		"transmission": "string",
		"location": "string",
		"date_posted": "string",
		"link": "string",
		"date_imported": "datetime64[ns]",
	}

	df = pd.DataFrame(
		{
			"title": titles,
			"descr": descrs,
			"price": prices,
			"year": years,
			"km": kms,
			"transmission": transmissions,
			"location": locations,
			"date_posted": dates_posted,
			"link": links,
			"date_imported": dates_imported,
		}
	)

	df = df.astype(dtypes)

	return df


def get_completion(prompt, model="gpt-3.5-turbo-16k-0613", temperature=0, num_retries=3, sleep_time=15):
	"""Genera un texto en base a un prompt y un modelo de openai, reintenta por una cantidad de veces en caso de error"""
	messages = [{"role": "user", "content": prompt}]

	response = ""

	if temperature < 0 or temperature > 1:
		return {"status": "error", "message": "La temperatura debe ser un número entre 0 y 1"}

	for i in range(num_retries):
		try:
			response = openai.ChatCompletion.create(
				model=model,
				messages=messages,
				temperature=temperature,
				max_tokens=12000
			)
			break
		except Exception as e:
			print(f"Retry {i+1}/{num_retries} failed. Error: {e}")
			time.sleep(sleep_time)

	if response == '':
		return {"status": "error", "message": "Máximo de reintentos alcanzado"}
	else:
		return {"status": "success", "message": response.choices[0].message["content"]}