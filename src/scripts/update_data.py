import urllib.request, json, psycopg2
c_url="https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=USD&limit=100"
values = {'fsym': "BTC", "tsym" : "USD", "limit" : 100}
currency = ['BTC', 'ETH', 'LTC']
in_value = urllib.parse.urlencode(values).encode("ascii")
conn = psycopg2.connect("host=localhost dbname=crypto user=postgres")
cur = conn.cursor()


def get_data(curr_url):
    print(curr_url)
    req = urllib.request.Request(curr_url, in_value)
    with urllib.request.urlopen(req) as url:
        data = json.loads(url.read().decode())
        return data

def insert_db(data, currency):
    for item in data["Data"]:
        query =  "INSERT INTO bitcoin (CURRENCY, OPEN, CLOSE, HIGH, LOW, TIME, VOLUMETO, VOLUMEFROM) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        values = (currency, item["open"], item["close"], item["high"], item["low"], item["time"], item["volumeto"], item["volumefrom"])
        cur.execute(query, values)
    conn.commit()

def remove_zeros_and_dupes():
    query = "DELETE FROM bitcoin a USING ( SELECT MIN(ctid) as ctid, time, currency FROM bitcoin GROUP BY currency, time HAVING COUNT(*) > 1) b WHERE a.currency = b.currency AND a.time = b.time AND a.ctid <> b.ctid "
    cur.execute(query)
    
    query = "DELETE FROM bitcoin where open = 0 or close = 0 or high = 0 or low = 0 or volumeto = 0 or volumefrom = 0"
    cur.execute(query)
    
    conn.commit()

old = 'BTC'
for curr in currency:
    values['fsym'] = curr
    c_url = c_url.replace(old, curr) 
    old = curr
    data = get_data(c_url)
    insert_db(data, curr)
    
remove_zeros_and_dupes()

