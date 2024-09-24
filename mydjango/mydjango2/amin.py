import sqlite3
query="악뮤"
print("검색어:",query)
connection=sqlite3.connect("melon-20230906.sqlite3")
cursor=connection.cursor()
cursor.execute("SELECT*FROM songs")
column_names=[desc[0] for desc in cursor.description]
song_list=cursor.fetchall()
for song_tuple in song_list:
    song_dict=dict(zip(column_names,song_tuple))
    #print(song_dict["곡명"],song_dict["가수"])
    print("{곡명}{가수}".format(**song_dict))
connection.close()