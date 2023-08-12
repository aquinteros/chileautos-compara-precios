import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.buy_me_a_coffee import button as buy_me_a_coffee
from streamlit_extras.mention import mention
import random
import time


def get_html(url):
	"""Get the html of a url"""
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ",
		"Accept": "application/json, text/javascript, */*; q=0.01",
		"method": "GET",
		"mode": "cors",
	}

	r = requests.get(url, headers=headers)

	if r.status_code != 200:
		print("Error en la petición")
		print(url)
		print(r.reason)
		print(r.text)

	return r.text


def convert_df(df):
	"""Convert a pandas dataframe into a csv file that can be downloaded"""
	return df.to_csv(index=False).encode("utf-8")


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

AnoInicio = st.text_input("Año Inicio")

AnoFin = st.text_input("Año Fin")

Combustible = st.selectbox(
	"Combustible",
	[
		"Bencina",
		"Diesel",
		"Diesel (petróleo)",
		"Eléctrico",
		"Gas",
		"Híbrido",
		"Otros",
		"TODOS",
	],
)

Transmision = st.selectbox("Transmisión", ["Automática", "Manual", "AMBAS"])

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

	result = pd.DataFrame(
		columns=["Link", "Modelo", "Precio", "KM", "Combustible", "Transmisión", "AT4"]
	)

	if Combustible == "TODOS" and Transmision == "AMBAS":
		url = f"https://www.chileautos.cl/vehiculos/?q=(And.Servicio.chileautos._.CarAll.keyword({Keyword})._.Ano.range({AnoInicio}..{AnoFin}).)&offset="
		color = "Combustible"
	if Combustible == "TODOS" and Transmision != "AMBAS":
		url = f"https://www.chileautos.cl/vehiculos/?q=(And.Servicio.chileautos._.CarAll.keyword({Keyword})._.Ano.range({AnoInicio}..{AnoFin})._.Transmisión.{Transmision}.)&offset="
		color = "Combustible"
	if Combustible != "TODOS" and Transmision == "AMBAS":
		url = f"https://www.chileautos.cl/vehiculos/?q=(And.Servicio.chileautos._.CarAll.keyword({Keyword})._.Ano.range({AnoInicio}..{AnoFin})._.Combustible.{Combustible}.)&offset="
		color = "Transmisión"
	if Combustible != "TODOS" and Transmision != "AMBAS":
		url = f"https://www.chileautos.cl/vehiculos/?q=(And.Servicio.chileautos._.CarAll.keyword({Keyword})._.Ano.range({AnoInicio}..{AnoFin})._.Combustible.{Combustible}._.Transmisión.{Transmision}.)&offset="
		color = None

	offsetlist = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 132, 144, 156]
	offsetlist = [0, 12]

	for ofs in offsetlist:
		url_final = url + str(ofs)

		html = get_html(url_final)
		soup = BeautifulSoup(html, "lxml")

		cards = soup.find_all("div", class_="card-body")

		for card in cards:
			link = "https://www.chileautos.cl" + card.find(
				"a", class_="js-encode-search"
			).get("href")

			text_list = []
			texto = card.find_all("a", class_="js-encode-search")
			for t in texto:
				text_list.append(t.text.strip())

			nombre_p = text_list[0]

			precio = float(text_list[1].replace("$", "").replace(",", ""))

			item_list = []
			items = card.find_all("li", class_="key-details__value")
			for i in items:
				item_list.append(i.text.strip())

			try:
				at1 = float(item_list[0].replace(" km", "").replace(",", ""))
			except:
				at1 = "N/A"
			try:
				at2 = item_list[1]
			except:
				at2 = "N/A"
			try:
				at3 = item_list[2]
			except:
				at3 = "N/A"
			try:
				at4 = item_list[3]
			except:
				at4 = "N/A"

			result = pd.concat(
				[
					result,
					pd.DataFrame(
						[[link, nombre_p, precio, at1, at2, at3, at4]],
						columns=[
							"Link",
							"Modelo",
							"Precio",
							"KM",
							"Transmisión",
							"Combustible",
							"AT4",
						],
					),
				],
				ignore_index=True,
			)

		progress_bar.progress(ofs / max(offsetlist))

		#  sleep for random amount of time between 4 and 7 seconds to avoid getting blocked
		#  import random

		sleeptime = random.randint(4, 7)
		time.sleep(sleeptime)

	px.defaults.template = "plotly_white"

	fig = px.scatter(
		data_frame=result,
		x="KM",
		y="Precio",
		color=color,
		hover_name="Modelo",
		title="Comparación de Precios de Autos en ChileAutos.cl",
	)

	st.plotly_chart(fig, use_container_width=True)

	st.download_button(
		label="Descargar CSV",
		data=convert_df(result),
		file_name="chileautos.csv",
		mime="text/csv",
	)
