import sqlite3
query="악뮤"
print("검색어:",query)

connection=sqlite3.connect("melon-20230906.sqlite3")
#파일 경로를 인자로 받아서 연결, 트랜잭션 관리 담당
cursor=connection.cursor()
#커서를 통해 쿼리 실행
connection.set_trace_callback(print)

param='%'+query+'%'
sql=f"SELECT * FROM songs WHERE 가수 LIKE ? OR 곡명 LIKE ?"
cursor.execute(sql,[param,param])
#select 쿼리 -> 요청만 전송되고(쿼리 실행) 아직 메모리에 가져온게 아님
column_names=[desc[0] for desc in cursor.description]
#메타데이터(데이터를 설명하는 데이터(데이터 구조,관계 등))를 가져옴
song_list=cursor.fetchall()
#전체행 가져오기 (파이썬 메모리로 가져오는 것)
#cursor.fetchone() -> 한 행만 가져오기
print("list size :",len(song_list))
for song_tuple in song_list:
    song_dict=dict(zip(column_names,song_tuple))
    #print(song_dict["곡명"],song_dict["가수"])
    print("{곡명}{가수}".format(**song_dict))
    #키, 값을 언팩해서 메소드에 전달, 키를 통해 값에 접근 가능
connection.close()