from utils import * 

def main():

	modelos = pd.read_csv('modelos.csv', sep=';')

	marcas = modelos['Marca'].unique().tolist()

	ya_procesados = ['CHANGAN', 'FIAT', 'HYUNDAI', 'MAZDA', 'MG', 'PEUGEOT', 'RAM', 'VOLKSWAGEN', 'CHEVROLET']

	for marca in marcas:

		if marca in ya_procesados:
			print(f'La marca {marca} ya fue procesada.')
			continue

		print(f'Procesando marca {marca}...')

		df_marca = pd.DataFrame()

		modelos_marca = modelos[modelos['Marca'] == marca]

		for i, row in modelos_marca.iterrows():

			print(f'Procesando modelo {row["Modelo"]}...')
			
			Keyword = row['Marca'] + ' ' + row['Modelo']
			year_min = 2010
			year_max = 2023
			maxpage = 5

			df = scrape_yapo(Keyword, year_min, year_max, maxpage)

			df['Marca'] = row['Marca']
			df['Tipo'] = row['Tipo']
			df['Modelo'] = row['Modelo']

			df_marca = pd.concat([df_marca, df], ignore_index=True)

		df_marca.to_csv(f'data/{marca}.csv', index=False)

		print(f'Archivo {marca}.csv guardado en data, con {len(df_marca)} filas.')

if __name__ == '__main__':
	main()