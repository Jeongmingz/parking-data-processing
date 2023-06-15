import mysql.connector
import pandas as pd
import pickle
import os

pickle_file = "../data/parking_dataframe.pkl"
pd.set_option('display.max_columns', None)

# pickle 파일이 존재하는 경우에만 데이터프레임 로드
if os.path.exists(pickle_file):
	# 데이터프레임 로드
	df = pickle.load(open(pickle_file, "rb"))
	df['date'] = df["date"].dt.strftime("%Y-%m-%d %H")
	df['total_parking'] = df.iloc[:, 2:].sum(axis=1)
	df['date_hour'] = df['date'].str[-2:]
	df_grouped = df.groupby(['date_hour', 'day']).agg({'total_parking': 'mean'}).reset_index()

	result_dict = {}
	day_list = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
	for i, day in enumerate(df_grouped['day'].unique()):
		day_data = df_grouped[df_grouped['day'] == day]
		day_str = day_list[i]  # 요일을 문자열로 변환

		day_dict = {
			'date_hour': day_data['date_hour'].tolist(),
			'total_parking': day_data['total_parking'].tolist()
			}
		result_dict[day_str] = day_dict

	import json

	# Dump data to a JSON file
	filename = "../data/data.json"
	with open(filename, "w", encoding='utf-8') as file:
		json.dump(result_dict, file, ensure_ascii=False)
else:
	db_config = {
		'user': 'root',
		'password': '12345678',
		'host': 'daelimparking-mysql.ck1tpopwzpsw.ap-northeast-2.rds.amazonaws.com',
		'database': 'daelimparking'
		}

	# 데이터베이스 연결 생성
	conn = mysql.connector.connect(**db_config)

	# 커서 생성
	cursor = conn.cursor()
	query = "SELECT date, day"
	for i in range(1, 24):
		query += f", parking_slot_{i}"
	query += " FROM parking_data_per_5min"

	cursor.execute(query)

	# 결과 가져오기
	result = cursor.fetchall()
	cursor.close()
	conn.close()

	columns = ["date", "day"]
	columns += [f"parking_slot_{i}" for i in range(1, 24)]

	df = pd.DataFrame(result, columns=columns)

	pickle.dump(df, open("../data/parking_dataframe.pkl", "wb"))
