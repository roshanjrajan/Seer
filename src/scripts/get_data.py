import urllib.request, json, psycopg2
c_url="https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=USD&limit=2000"
values = {'fsym': "BTC", "tsym" : "USD", "limit" : 2000}
currency = ['LTC']
in_value = urllib.parse.urlencode(values).encode("ascii")
conn = psycopg2.connect("host=localhost dbname=crypto user=postgres")
cur = conn.cursor()
db = 'litecoin'


def get_data(curr_url):
    print(curr_url)
    req = urllib.request.Request(curr_url, in_value)
    with urllib.request.urlopen(req) as url:
        data = json.loads(url.read().decode())
        return data

def get_timestamp(data):
    return data["Data"][0]["time"]

def insert_db(data, currency):
    for item in data["Data"]:
        query =  "INSERT INTO " + db +" (CURRENCY, OPEN, CLOSE, HIGH, LOW, TIME, VOLUMETO, VOLUMEFROM) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        values = (currency, item["open"], item["close"], item["high"], item["low"], item["time"], item["volumeto"], item["volumefrom"])
        cur.execute(query, values)
    conn.commit()

def remove_zeros_and_dupes():
    query = "DELETE FROM " + db + " a USING ( SELECT MIN(ctid) as ctid, time, currency FROM cryptocurrency GROUP BY currency, time HAVING COUNT(*) > 1) b WHERE a.currency = b.currency AND a.time = b.time AND a.ctid <> b.ctid "
    cur.execute(query)
    
    query = "DELETE FROM " + db + " where open = 0 or close = 0 or high = 0 or low = 0 or volumeto = 0 or volumefrom = 0"
    cur.execute(query)
    
    conn.commit()

def check_for_zero(data):
    for item in data["Data"]:
        if(item["open"] == 0):
            print (item["time"])
            return True






old = 'BTC'
for curr in currency:
    values['fsym'] = curr
    c_url = c_url.replace(old, curr) 
    old = curr
    print(c_url)
    print(values)
    data = get_data(c_url)
    start_timestamp = get_timestamp(data)
    insert_db(data, curr)
    nc_url = c_url +"&toTs={0}"
    done = False
    while not done:
        new_url = nc_url.format(start_timestamp)
        data = get_data(new_url)
        insert_db(data, curr)
        start_timestamp = get_timestamp(data)
        done = check_for_zero(data)
    
remove_zeros_and_dupes()

