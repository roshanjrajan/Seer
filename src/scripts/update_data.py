import urllib.request, json, psycopg2
c_url="https://min-api.cryptocompare.com/data/histoday?fsym=BTC&tsym=USD&limit=10000"
with urllib.request.urlopen(c_url) as url:
    data = json.loads(url.read().decode())

print(data["Data"][0])
conn = psycopg2.connect("host=localhost dbname=crypto user=postgres")
cur = conn.cursor()
cur.execute("SHOW Databases")
#for item in data["Data"]:
    #Hello
