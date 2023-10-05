
from utils import *

def main():
	st.set_page_config(
		page_title="Compara Precios de Autos en Yapo.cl",
		page_icon="🚗",
		initial_sidebar_state="expanded",
	)

	colored_header(
		"Comparador de precios",
		color_name="blue-70",
		description="Compara Precios de Autos en Yapo.cl",
	)

	buy_me_a_coffee(username="aquinteros", floating=False, width=221)


	st.sidebar.title("Acerca de")

	st.sidebar.write(
		"Esta aplicación web fue creada con el objetivo de comparar precios de autos en Yapo.cl"
	)
	st.sidebar.write(
		"El funcionamiento es simple, solo debes ingresar los filtros que deseas aplicar y presionar el botón 'Buscar'"
	)
	st.sidebar.write(
		"Los filtros están en formato texto, para evitar errores, se recomienda copiar y pegar los valores desde la página de Yapo.cl"
	)
	st.sidebar.write(
		"Al precionar el botón 'Buscar', se realizará una búsqueda en Yapo.cl de las primeras 14 páginas y se generará un gráfico de dispersión con los resultados."
	)
	st.sidebar.write("Puedes descargarlos para poder realizar un análisis más detallado.")
	st.sidebar.write(
		"('Esta aplicación web fue creada para fines educativos. No se recomienda usarla para tomar decisiones financieras.')"
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
			label="compara-precios-yapo",
			icon="github",
			url="https://github.com/aquinteros/compara-precios-yapo",
		)

	with st.form(key="formulario"):

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

		btn = st.form_submit_button(label="Buscar")

	if btn:
		
		df = scrape_yapo(Keyword, year_min, year_max, maxpage)

		st.dataframe(df)

		px.defaults.template = "plotly_white"

		fig = px.scatter(
			data_frame=df,
			x="km",
			y="price",
			color="transmission",
			hover_name="title",
			title="Comparación de Precios de Autos en Yapo.cl",
		)

		st.plotly_chart(fig, use_container_width=True)

		st.download_button(
			label="Descargar CSV",
			data=convert_df(df),
			file_name="yapo.csv",
			mime="text/csv",
		)

if __name__ == "__main__":
	main()