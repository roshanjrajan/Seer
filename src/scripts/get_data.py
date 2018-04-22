import urllib.request, json, psycopg2
c_url="https://min-api.cryptocompare.com/data/histohour?fsym=BTC&tsym=USD&limit=2000"
values = {'fsym': "BTC", "tsym" : "USD", "limit" : 2000}
in_value = urllib.parse.urlencode(values).encode("ascii")
conn = psycopg2.connect("host=localhost dbname=crypto user=postgres")
cur = conn.cursor()

def get_data(curr_url):
    print(curr_url)
    req = urllib.request.Request(curr_url, in_value)
    with urllib.request.urlopen(req) as url:
        data = json.loads(url.read().decode())
        return data

def get_timestamp(data):
    return data["Data"][0]["time"]

def insert_db(data):
    for item in data["Data"]:
        query =  "INSERT INTO bitcoin (CURRENCY, OPEN, CLOSE, HIGH, LOW, TIME, VOLUMETO, VOLUMEFROM) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        values = ("BTC", item["open"], item["close"], item["high"], item["low"], item["time"], item["volumeto"], item["volumefrom"])
        cur.execute(query, values)
    conn.commit()

def check_for_zero(data):
    for item in data["Data"]:
        if(item["open"] == 0):
            print (item["time"])
            return True


data = get_data(c_url)
start_timestamp = get_timestamp(data)

insert_db(data)

c_url +="&toTs={0}"

done = False
i = 0
while not done:
    new_url = c_url.format(start_timestamp)
    data = get_data(new_url)
    insert_db(data)
    start_timestamp = get_timestamp(data)
    done = check_for_zero(data)
    


