from utils import *

def main():
	csv_list = [
		'CHANGAN.csv',
		'CHERY.csv',
		'CHEVROLET.csv',
		'CITROEN.csv',
		'FIAT.csv',
		'FORD.csv',
		'GREAT WALL.csv',
		'HAVAL.csv',
		'HONDA.csv',
		'HYUNDAI.csv',
		'JAC.csv',
		'JEEP.csv',
		'JMC.csv',
		'KIA.csv',
		'MAXUS.csv',
		'MAZDA.csv',
		'MG.csv',
		'MITSUBISHI.csv',
		'NISSAN.csv',
		'PEUGEOT.csv',
		'RAM.csv',
		'RENAULT.csv',
		'SSANGYONG.csv',
		'SUBARU.csv',
		'SUZUKI.csv',
		'TOYOTA.csv',
		'VOLKSWAGEN.csv'
	]

	df = pd.DataFrame()

	for csv in csv_list:
		df_csv = pd.read_csv(f'data/{csv}')
		df = pd.concat([df, df_csv], ignore_index=True)

	print(df.shape)
	print(df['link'].nunique())
	print(df['title'].nunique())
	print(df.head())

if __name__ == '__main__':
	main()
