import sqlite3
import requests

con = sqlite3.connect('laftel.db')
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS anime (id text, name text)')
cur.execute('DELETE FROM anime')

header = {'laftel' : 'TeJava'}
base_url = f'https://laftel.net/api/search/v1/discover/'
response = requests.get(url=base_url, headers=header)
print("크롤링 시작")

while True:
    js = response.json()
    results = js["results"]

    data = []
    for r in results:
        index = r['id']
        name = r['name']
        data.append((index, name))

    cur.executemany("INSERT INTO anime(id, name) VALUES(?,?)", data)
    con.commit()
    url = js['next']

    try:
        response = requests.get(url=url, headers=header)
    except requests.exceptions.MissingSchema:
        print("크롤링 완료")
        break
con.close()