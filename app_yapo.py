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
from webdriver_manager.chrome import ChromeDriverManager

def get_html(url):
	"""Get the html of a url"""

	browser = webdriver.Chrome(ChromeDriverManager().install())
	browser.maximize_window()
	browser.set_window_size(1920, 1080)
	browser.execute_script("document.body.style.zoom='100%'")
	browser.get(url)
	time.sleep(2)
	# browser.execute_script(
	# 	"Object.defineProperty(navigator, 'userAgent', {value: 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46',writable: true,configurable: true});"
	# )
	# browser.refresh()

	for i in range(0, 20):
		browser.execute_script(f"window.scrollTo({i * 1000}, {i * 1000 + 1000})")
		time.sleep(0.5)

	# browser.refresh()
	html = browser.page_source
	browser.quit()
	return html


def convert_df(df):
	"""Convert a pandas dataframe into a csv file that can be downloaded"""
	return df.to_csv(index=False).encode("utf-8")


def main():
	st.set_page_config(
		page_title="Compara Precios de Autos en ChileAutos.cl",
		page_icon="🚗",
		initial_sidebar_state="expanded",
	)

	colored_header(
		"Comparador de precios",
		color_name="blue-70",
		description="Compara Precios de Autos en ChileAutos.cl",
	)

	buy_me_a_coffee(username="aquinteros", floating=False, width=221)


	st.sidebar.title("Acerca de")

	st.sidebar.write(
		"Esta aplicación web fue creada con el objetivo de comparar precios de autos en ChileAutos.cl."
	)
	st.sidebar.write(
		"El funcionamiento es simple, solo debes ingresar los filtros que deseas aplicar y presionar el botón 'Buscar'."
	)
	st.sidebar.write(
		"Los filtros están en formato texto, para evitar errores, se recomienda copiar y pegar los valores desde la página de ChileAutos.cl"
	)
	st.sidebar.write(
		"Al precionar el botón 'Buscar', se realizará una búsqueda en ChileAutos.cl de las primeras 14 páginas y se generará un gráfico de dispersión con los resultados."
	)
	st.sidebar.write("Puedes descargarlos para poder realizar un análisis más detallado.")
	st.sidebar.write(
		"('Esta aplicación web fue creada para fines educativos. No se recomienda usarla para tomar decisiones financieras.')"
	)

	Keyword = st.text_input("Keyword (modelo)")

	maxpage = st.select_slider(
		"Max Page",
		options=list(range(1, 16)),
		value=15,
	)

	year_min = st.number_input(
		"Year Min",
		min_value=2000,
		max_value=2030,
		value=2023,
		step=1,
	)

	year_max = st.number_input(
		"Year Max",
		min_value=2000,
		max_value=2030,
		value=2023,
		step=1,
	)

	st.sidebar.markdown(
		"""
		Preguntas? \n
		Envíame un correo: \n
		"""
	)

	with st.sidebar:
		mention(
			label="alvaro.quinteros.a@gmail.com",
			icon="📧",
			url="mailto:alvaro.quinteros.a@gmail.com",
		)

	st.sidebar.markdown(
		"""
		O abre un issue en el repositorio de GitHub: \n
		"""
	)

	with st.sidebar:
		mention(
			label="chileautos-compara-precios",
			icon="github",
			url="https://github.com/aquinteros/chileautos-compara-precios",
		)

	if st.button("Buscar"):
		progress_bar = st.progress(0)

		result = pd.DataFrame()

		baseurl = f'https://www.yapo.cl/vehiculos/vehiculos/autos-camionetas-4x4?year={year_min}-{year_max}&orden=date-desc&buscar={Keyword}&pagina='

		paginalist = list(range(1, maxpage + 1))

		for pagina in paginalist:

			url = baseurl + str(pagina)

			html = get_html(url)
			soup = BeautifulSoup(html, "lxml")

			cards = soup.find_all("a", class_="card d-flex flex-row align-self-stretch flex-fill cars subcategory-2020 category-2000 horizontal has-cover is-visible")

			for card in cards:
				try:
					title = card.find("h2", class_="title m-0 text-truncate pb-2").text
					descr = card.find("p", class_="body m-0 mb-2").text
					price = float(card.find("span", class_="clp-price d-flex display-price ng-star-inserted").text.replace("$", "").replace(".", "").strip('()'))
					attrs = card.find_all("span", class_="label value align-self-center")
					year = attrs[0].text
					km = float(attrs[1].text.replace(".", ""))
					transmission = attrs[2].text
					date_posted = card.find("p", class_="d-flex m-0 created col ng-star-inserted").text
					link = "https://www.yapo.cl" + card.get("href")

					result = pd.concat(
						[
							result,
							pd.DataFrame(
								[[title, descr, price, year, km, transmission, date_posted, link]],
								columns=[
									"title",
									"descr",
									"price",
									"year",
									"km",
									"transmission",
									"date_posted",
									"link",
								],
							),
						],
						ignore_index=True,
					)
				except:
					pass

			progress_bar.progress(pagina / len(paginalist))

			sleeptime = random.randint(3, 7)
			time.sleep(sleeptime)
			
		st.dataframe(result)

		px.defaults.template = "plotly_white"

		fig = px.scatter(
			data_frame=result,
			x="km",
			y="price",
			color="transmission",
			hover_name="title",
			title="Comparación de Precios de Autos en Yapo.cl",
		)

		st.plotly_chart(fig, use_container_width=True)

		st.download_button(
			label="Descargar CSV",
			data=convert_df(result),
			file_name="yapo.csv",
			mime="text/csv",
		)

if __name__ == "__main__":
	main()