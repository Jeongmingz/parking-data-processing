import random
import mysql.connector
from datetime import datetime, timedelta

def generate_random_binary_list(length):
	binary_list = []
	for _ in range(length):
		binary_list.append(random.choice([0, 1]))
	return binary_list

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
query = "INSERT INTO parking_data_per_5min (day, date, parking_slot_1"
placeholders = "%s, %s, %s"
for i in range(2, 24):
	query += f", parking_slot_{i}"
	placeholders += ", %s"
query += f") VALUES ({placeholders})"

start_time = datetime.now()
start_time -= timedelta(minutes=40)
while 1:
	time_offset = timedelta(minutes=5)
	start_time += time_offset

	data = tuple([start_time.weekday()]+[start_time]+generate_random_binary_list(23))  # 리스트를 튜플로 변환하여 쿼리에 전달

	cursor.execute(query, data)

	conn.commit()

	if start_time.day == 27:
		break

# 연결 및 커서 닫기
cursor.close()
conn.close()
